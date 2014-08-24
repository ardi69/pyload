# -*- coding: utf-8 -*-

from datetime import datetime
from operator import itemgetter, attrgetter

import os
import sys
import time

from os import listdir, path
from urllib import unquote

from bottle import route, static_file, request, response, redirect, HTTPError, error

from pyload.utils import formatSize, safe_join, fs_encode, fs_decode
from pyload.webui import API, ENV, THEME, THEME_DIR
from pyload.webui.app.utils import render_to_response, parse_permissions, parse_userdata, \
                                   login_required, get_permission, set_permission, \
                                   permlist, toDict, set_session
from pyload.webui.filters import unquotepath


# Helper
def pre_processor():
    s = request.environ.get('beaker.session')
    user = parse_userdata(s)
    perms = parse_permissions(s)
    status = {}
    captcha = False
    update = False
    plugins = False
    if user['is_authenticated']:
        status = API.statusServer()
        info = API.getInfoByPlugin("UpdateManager")
        captcha = API.isCaptchaWaiting()

        # check if update check is available
        if info:
            if info['pyload'] == "True":
                update = info['version']
            if info['plugins'] == "True":
                plugins = True


    return {'user': user,
            'status': status,
            'captcha': captcha,
            'perms': perms,
            'url': request.url,
            'update': update,
            'plugins': plugins}


def base(messages):
    return render_to_response('base.html', {'messages': messages}, [pre_processor])


## Views
@error(500)
def error500(error):
    print "An error occured while processing the request."
    if error.traceback:
        print error.traceback

    return base(["An Error occured, please enable debug mode to get more details.", error,
                 error.traceback.replace("\n", "<br>") if error.traceback else "No Traceback"])

# render js
@route('/<tml>/js/<file:path>')
def js_dynamic(tml, file):
    response.headers['Expires'] = time.strftime("%a, %d %b %Y %H:%M:%S GMT",
                                                time.gmtime(time.time() + 60 * 60 * 24 * 2))
    response.headers['Cache-control'] = "public"
    response.headers['Content-Type'] = "text/javascript; charset=UTF-8"

    try:
        # static files are not rendered
        if ".static" not in file:
            filename = "%s/js/%s" % (THEME, file)
            return ENV.get_template(filename).render()
        else:
            return static_file(file, root=path.join(THEME_DIR, tml, "js"))
    except:
        return HTTPError(404, "Not Found")

@route('/<tml>/<type>/<file:path>')
def server_static(tml, type, file):
    response.headers['Expires'] = time.strftime("%a, %d %b %Y %H:%M:%S GMT",
                                                time.gmtime(time.time() + 60 * 60 * 24 * 7))
    response.headers['Cache-control'] = "public"
    return static_file(file, root=path.join(THEME_DIR, tml, type))

@route('/favicon.ico')
def favicon():
    return static_file("icon.ico", root=path.join(pypath, "docs", "resources"))


@route('/login', method="GET")
def login():
    return render_to_response("login.html", proc=[pre_processor])


@route('/nopermission')
def nopermission():
    return base([_("You dont have permission to access this page.")])


@route('/login', method='POST')
def login_post():
    user = request.forms.get("username")
    password = request.forms.get("password")

    info = API.checkAuth(user, password)

    if not info:
        return render_to_response("login.html", {'errors': True}, [pre_processor])

    set_session(request, info)
    return redirect("/")


@route('/logout')
def logout():
    s = request.environ.get('beaker.session')
    s.delete()
    return render_to_response("logout.html", proc=[pre_processor])


@route('/')
@route('/home')
@login_required("LIST")
def home():
    try:
        res = [toDict(x) for x in API.statusDownloads()]
    except:
        s = request.environ.get('beaker.session')
        s.delete()
        return redirect("/login")

    for link in res:
        if link['status'] == 12:
            link['information'] = "%s kB @ %s kB/s" % (link['size'] - link['bleft'], link['speed'])

    return render_to_response("home.html", {'res': res}, [pre_processor])


@route('/queue')
@login_required("LIST")
def queue():
    queue = API.getQueue()

    queue.sort(key=attrgetter("order"))

    return render_to_response('queue.html', {'content': queue, 'target': 1}, [pre_processor])


@route('/collector')
@login_required('LIST')
def collector():
    queue = API.getCollector()

    queue.sort(key=attrgetter("order"))

    return render_to_response('queue.html', {'content': queue, 'target': 0}, [pre_processor])


@route('/downloads')
@login_required('DOWNLOAD')
def downloads():
    root = API.getConfigValue("general", "download_folder")

    if not path.isdir(root):
        return base([_('Download directory not found.')])
    data = {
        'folder': [],
        'files': []
    }

    items = listdir(fs_encode(root))

    for item in sorted([fs_decode(x) for x in items]):
        if path.isdir(safe_join(root, item)):
            folder = {
                'name': item,
                'path': item,
                'files': []
            }
            files = listdir(safe_join(root, item))
            for file in sorted([fs_decode(x) for x in files]):
                try:
                    if path.isfile(safe_join(root, item, file)):
                        folder['files'].append(file)
                except:
                    pass

            data['folder'].append(folder)
        elif path.isfile(path.join(root, item)):
            data['files'].append(item)

    return render_to_response('downloads.html', {'files': data}, [pre_processor])


@route('/downloads/get/<path:path>')
@login_required("DOWNLOAD")
def get_download(filename):
    filename = unquote(path).decode("utf8")
    #@TODO: some files can not be downloaded

    root = API.getConfigValue("general", "download_folder")

    filename = path.replace("..", "")

    try:
        return static_file(fs_encode(filename), fs_encode(root))
    except Exception, e:
        print e
        return HTTPError(404, "File not Found.")



@route('/settings')
@login_required('SETTINGS')
def config():
    conf = API.getConfig()
    plugin = API.getPluginConfig()

    conf_menu = []
    plugin_menu = []

    for entry in sorted(conf.keys()):
        conf_menu.append((entry, conf[entry].description))

    for entry in sorted(plugin.keys()):
        plugin_menu.append((entry, plugin[entry].description))

    accs = API.getAccounts(False)

    for data in accs:
        if data.trafficleft == -1:
            data.trafficleft = _("unlimited")
        elif not data.trafficleft:
            data.trafficleft = _("not available")
        else:
            data.trafficleft = formatSize(data.trafficleft * 1024)

        if data.validuntil == -1:
            data.validuntil  = _("unlimited")
        elif not data.validuntil :
            data.validuntil  = _("not available")
        else:
            t = time.localtime(data.validuntil)
            data.validuntil  = time.strftime("%d.%m.%Y - %H:%M:%S", t)

        try:
            data.options['time'] = data.options['time'][0]
        except:
            data.options['time'] = "0:00-0:00"

        if "limitDL" in data.options:
            data.options['limitdl'] = data.options['limitDL'][0]
        else:
            data.options['limitdl'] = "0"

    return render_to_response('settings.html',
            {'conf': {'plugin': plugin_menu, 'general': conf_menu, 'accs': accs}, 'types': API.getAccountTypes()},
        [pre_processor])


@route('/filechooser')
@route('/pathchooser')
@route('/filechooser/<file:path>')
@route('/pathchooser/<item:path>')
@login_required('STATUS')
def path(file="", item=""):  #@TODO: rewrite all!
    type = "file" if file else "folder"
    item = path.normpath(unquotepath(item))

    if path.isfile(item):
        oldfile = item
        item = path.dirname(item)
    else:
        oldfile = ''

    abs = False

    if path.isdir(item):
        if path.isabs(item):
            cwd = path.abspath(item)
            abs = True
        else:
            cwd = path.relpath(item)
    else:
        cwd = os.getcwd()

    try:
        cwd = cwd.encode("utf8")
    except:
        pass

    cwd = path.normpath(path.abspath(cwd))
    parentdir = path.dirname(cwd)
    if not abs:
        if path.abspath(cwd) == "/":
            cwd = path.relpath(cwd)
        else:
            cwd = path.relpath(cwd) + path.sep
        parentdir = path.relpath(parentdir) + path.sep

    if path.abspath(cwd) == "/":
        parentdir = ""

    try:
        folders = os.listdir(cwd)
    except:
        folders = []

    files = []

    for f in folders:
        try:
            f = f.decode(sys.getfilesystemencoding())
            data = {'name': f, 'fullpath': path.join(cwd, f)}
            data['sort'] = data['fullpath'].lower()
            data['modified'] = datetime.fromtimestamp(int(path.getmtime(path.join(cwd, f))))
            data['ext'] = path.splitext(f)[1]
        except:
            continue

        if path.isdir(path.join(cwd, f)):
            data['type'] = 'dir'
        else:
            data['type'] = 'file'

        if path.isfile(path.join(cwd, f)):
            data['size'] = path.getsize(path.join(cwd, f))

            power = 0
            while (data['size'] / 1024) > 0.3:
                power += 1
                data['size'] /= 1024.
            units = ('', 'K', 'M', 'G', 'T')
            data['unit'] = units[power] + 'Byte'
        else:
            data['size'] = ''

        files.append(data)

    files = sorted(files, key=itemgetter('type', 'sort'))

    return render_to_response('pathchooser.html',
            {'cwd': cwd, 'files': files, 'parentdir': parentdir, 'type': type, 'oldfile': oldfile,
             'absolute': abs}, [])


@route('/logs')
@route('/logs', method='POST')
@route('/logs/<item>')
@route('/logs/<item>', method='POST')
@login_required('LOGS')
def logs(item=-1):
    s = request.environ.get('beaker.session')

    perpage = s.get('perpage', 34)
    reversed = s.get('reversed', False)

    warning = ""
    conf = API.getConfigValue("log", "file_log")
    if not conf:
        warning = "Warning: File log is disabled, see settings page."

    perpage_p = ((20, 20), (34, 34), (40, 40), (100, 100), (0, 'all'))
    fro = None

    if request.environ.get('REQUEST_METHOD', "GET") == "POST":
        try:
            fro = datetime.strptime(request.forms['from'], '%d.%m.%Y %H:%M:%S')
        except:
            pass
        try:
            perpage = int(request.forms['perpage'])
            s['perpage'] = perpage

            reversed = bool(request.forms.get('reversed', False))
            s['reversed'] = reversed
        except:
            pass

        s.save()

    try:
        item = int(item)
    except:
        pass

    log = API.getLog()
    if not perpage:
        item = 0

    if item < 1 or type(item) is not int:
        item = 1 if len(log) - perpage + 1 < 1 else len(log) - perpage + 1

    if type(fro) is datetime: # we will search for datetime
        item = -1

    data = []
    counter = 0
    perpagecheck = 0
    for l in log:
        counter += 1

        if counter >= item:
            try:
                date, time, level, message = l.decode("utf8", "ignore").split(" ", 3)
                dtime = datetime.strptime(date + ' ' + time, '%d.%m.%Y %H:%M:%S')
            except:
                dtime = None
                date = '?'
                time = ' '
                level = '?'
                message = l
            if item == -1 and dtime is not None and fro <= dtime:
                item = counter #found our datetime
            if item >= 0:
                data.append({'line': counter, 'date': date + " " + time, 'level': level, 'message': message})
                perpagecheck += 1
                if fro is None and dtime is not None: #if fro not set set it to first showed line
                    fro = dtime
            if perpagecheck >= perpage > 0:
                break

    if fro is None: #still not set, empty log?
        fro = datetime.now()
    if reversed:
        data.reverse()
    return render_to_response('logs.html', {'warning': warning, 'log': data, 'from': fro.strftime('%d.%m.%Y %H:%M:%S'),
                                            'reversed': reversed, 'perpage': perpage, 'perpage_p': sorted(perpage_p),
                                            'iprev': 1 if item - perpage < 1 else item - perpage,
                                            'inext': (item + perpage) if item + perpage < len(log) else item},
        [pre_processor])


@route('/admin')
@route('/admin', method='POST')
@login_required("ADMIN")
def admin():
    # convert to dict
    user = dict([(name, toDict(y)) for name, y in API.getAllUserData().iteritems()])
    perms = permlist()

    for data in user.itervalues():
        data['perms'] = {}
        get_permission(data['perms'], data['permission'])
        data['perms']['admin'] = True if data['role'] is 0 else False


    s = request.environ.get('beaker.session')
    if request.environ.get('REQUEST_METHOD', "GET") == "POST":
        for name in user:
            if request.POST.get("%s|admin" % name, False):
                user[name]['role'] = 0
                user[name]['perms']['admin'] = True
            elif name != s['name']:
                user[name]['role'] = 1
                user[name]['perms']['admin'] = False

            # set all perms to false
            for perm in perms:
                user[name]['perms'][perm] = False

            for perm in request.POST.getall("%s|perms" % name):
                user[name]['perms'][perm] = True

            user[name]['permission'] = set_permission(user[name]['perms'])

            API.setUserPermission(name, user[name]['permission'], user[name]['role'])

    return render_to_response("admin.html", {'users': user, 'permlist': perms}, [pre_processor])


@route('/info')
def info():
    conf = API.getConfigDict()

    if hasattr(os, "uname"):
        extra = os.uname()
    else:
        extra = tuple()

    data = {'python': sys.version,
            'os': " ".join((os.name, sys.platform) + extra),
            'version': API.getServerVersion(),
            'folder': pypath,
            'config': owd,
            'download': path.abspath(conf['general']['download_folder']['value']),
            'freespace': formatSize(API.freeSpace()),
            'remote': conf['remote']['port']['value'],
            'webif': conf['webui']['port']['value'],
            'language': conf['general']['language']['value']}

    return render_to_response("info.html", data, [pre_processor])
