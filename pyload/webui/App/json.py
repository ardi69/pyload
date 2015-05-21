# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import shutil
import traceback

import bottle

from pyload.utils import decode, format_size
from pyload.webui import PYLOAD
from pyload.webui.App.utils import decode, login_required, render_to_response, toDict


def format_time(seconds):
    seconds = int(seconds)

    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return "%.2i:%.2i:%.2i" % (hours, minutes, seconds)


def get_sort_key(item):
    return item['order']


@bottle.route('/json/status')
@bottle.route('/json/status', method='POST')
@login_required('LIST')
def status():
    try:
        status = toDict(PYLOAD.statusServer())
        status['captcha'] = PYLOAD.isCaptchaWaiting()
        return status
    except Exception:
        return bottle.HTTPError()


@bottle.route('/json/links')
@bottle.route('/json/links', method='POST')
@login_required('LIST')
def links():
    try:
        links = [toDict(x) for x in PYLOAD.statusDownloads()]
        ids = []
        for link in links:
            ids.append(link['fid'])

            if link['status'] == 12:
                link['info'] = "%s @ %s/s" % (link['format_eta'], format_size(link['speed']))
            elif link['status'] == 5:
                link['percent'] = 0
                link['size'] = 0
                link['bleft'] = 0
                link['info'] = _("waiting %s") % link['format_wait']
            else:
                link['info'] = ""

        data = {'links': links, 'ids': ids}
        return data
    except Exception, e:
        traceback.print_exc()
        return bottle.HTTPError()


@bottle.route('/json/packages')
@login_required('LIST')
def packages():
    print "/json/packages"
    try:
        data = PYLOAD.getQueue()

        for package in data:
            package['links'] = []
            for file in PYLOAD.get_package_files(package['id']):
                package['links'].append(PYLOAD.get_file_info(file))

        return data

    except Exception:
        return bottle.HTTPError()


@bottle.route('/json/package/<id:int>')
@login_required('LIST')
def package(id):
    try:
        data = toDict(PYLOAD.getPackageData(id))
        data['links'] = [toDict(x) for x in data['links']]

        for pyfile in data['links']:
            if pyfile['status'] == 0:
                pyfile['icon'] = "status_finished.png"
            elif pyfile['status'] in (2, 3):
                pyfile['icon'] = "status_queue.png"
            elif pyfile['status'] in (9, 1):
                pyfile['icon'] = "status_offline.png"
            elif pyfile['status'] == 5:
                pyfile['icon'] = "status_waiting.png"
            elif pyfile['status'] == 8:
                pyfile['icon'] = "status_failed.png"
            elif pyfile['status'] == 4:
                pyfile['icon'] = "arrow_right.png"
            elif pyfile['status'] in (11, 13):
                pyfile['icon'] = "status_proc.png"
            else:
                pyfile['icon'] = "status_downloading.png"

        tmp = data['links']
        tmp.sort(key=get_sort_key)
        data['links'] = tmp
        return data

    except Exception:
        traceback.print_exc()
        return bottle.HTTPError()


@bottle.route('/json/package_order/<ids>')
@login_required('ADD')
def package_order(ids):
    try:
        pid, pos = ids.split("|")
        PYLOAD.orderPackage(int(pid), int(pos))
        return {"response": "success"}
    except Exception:
        return bottle.HTTPError()


@bottle.route('/json/abort_link/<id:int>')
@login_required('DELETE')
def abort_link(id):
    try:
        PYLOAD.stopDownloads([id])
        return {"response": "success"}
    except Exception:
        return bottle.HTTPError()


@bottle.route('/json/link_order/<ids>')
@login_required('ADD')
def link_order(ids):
    try:
        pid, pos = ids.split("|")
        PYLOAD.orderFile(int(pid), int(pos))
        return {"response": "success"}
    except Exception:
        return bottle.HTTPError()


@bottle.route('/json/add_package')
@bottle.route('/json/add_package', method='POST')
@login_required('ADD')
def add_package():
    name = bottle.request.forms.get("add_name", "New Package").strip()
    queue = int(bottle.request.forms['add_dest'])
    links = decode(bottle.request.forms['add_links'])
    links = links.split("\n")
    pw = bottle.request.forms.get("add_password", "").strip("\n\r")

    try:
        f = bottle.request.files['add_file']

        if not name or name == "New Package":
            name = f.name

        fpath = os.path.join(PYLOAD.getConfigValue("general", "download_folder"), "tmp_" + f.filename)
        with open(fpath, 'wb') as destination:
            shutil.copyfileobj(f.file, destination)
        links.insert(0, fpath)
    except Exception:
        pass

    name = decode(name)

    links = map(lambda x: x.strip(), links)
    links = filter(lambda x: x != "", links)

    pack = PYLOAD.addPackage(name, links, queue)
    if pw:
        data = {"password": decode(pw)}
        PYLOAD.setPackageData(pack, data)


@bottle.route('/json/move_package/<dest:int>/<id:int>')
@login_required('MODIFY')
def move_package(dest, id):
    try:
        PYLOAD.movePackage(dest, id)
        return {"response": "success"}
    except Exception:
        return bottle.HTTPError()


@bottle.route('/json/edit_package', method='POST')
@login_required('MODIFY')
def edit_package():
    try:
        id = int(bottle.request.forms.get("pack_id"))
        data = {"name"    : decode(bottle.request.forms.get("pack_name")),
                "folder"  : decode(bottle.request.forms.get("pack_folder")),
                "password": decode(bottle.request.forms.get("pack_pws"))}

        PYLOAD.setPackageData(id, data)
        return {"response": "success"}

    except Exception:
        return bottle.HTTPError()


@bottle.route('/json/set_captcha')
@bottle.route('/json/set_captcha', method='POST')
@login_required('ADD')
def set_captcha():
    if bottle.request.environ.get('REQUEST_METHOD', "GET") == "POST":
        try:
            PYLOAD.setCaptchaResult(bottle.request.forms['cap_id'], bottle.request.forms['cap_result'])
        except Exception:
            pass

    task = PYLOAD.getCaptchaTask()

    if task.tid >= 0:
        src = "data:image/%s;base64,%s" % (task.type, task.data)

        return {'captcha': True, 'id': task.tid, 'src': src, 'result_type': task.resultType}
    else:
        return {'captcha': False}


@bottle.route('/json/load_config/<category>/<section>')
@login_required("SETTINGS")
def load_config(category, section):
    conf = None
    if category == "general":
        conf = PYLOAD.getConfigDict()
    elif category == "plugin":
        conf = PYLOAD.getPluginConfigDict()

    for key, option in conf[section].iteritems():
        if key in ("desc", "outline"):
            continue

        if ";" in option['type']:
            option['list'] = option['type'].split(";")

        option['value'] = decode(option['value'])

    return render_to_response("settings_item.html", {"sorted_conf": lambda c: sorted(c.items(), key=lambda i: i[1]['idx'] if i[0] not in ("desc", "outline") else 0),
                                                     "skey": section, "section": conf[section]})


@bottle.route('/json/save_config/<category>', method='POST')
@login_required("SETTINGS")
def save_config(category):
    for key, value in bottle.request.POST.iteritems():
        try:
            section, option = key.split("|")
        except Exception:
            continue

        if category == "general": category = "core"

        PYLOAD.setConfigValue(section, option, decode(value), category)


@bottle.route('/json/add_account', method='POST')
@login_required("ACCOUNTS")
def add_account():
    login = bottle.request.POST['account_login']
    password = bottle.request.POST['account_password']
    type = bottle.request.POST['account_type']

    PYLOAD.updateAccount(type, login, password)


@bottle.route('/json/update_accounts', method='POST')
@login_required("ACCOUNTS")
def update_accounts():
    deleted = []  #: dont update deleted accs or they will be created again

    for name, value in bottle.request.POST.iteritems():
        value = value.strip()
        if not value:
            continue

        tmp, user = name.split(";")
        plugin, action = tmp.split("|")

        if (plugin, user) in deleted:
            continue

        if action == "password":
            PYLOAD.updateAccount(plugin, user, value)
        elif action == "time" and "-" in value:
            PYLOAD.updateAccount(plugin, user, options={"time": [value]})
        elif action == "limitdl" and value.isdigit():
            PYLOAD.updateAccount(plugin, user, options={"limitDL": [value]})
        elif action == "delete":
            deleted.append((plugin, user))
            PYLOAD.removeAccount(plugin, user)


@bottle.route('/json/change_password', method='POST')
def change_password():
    user = bottle.request.POST['user_login']
    oldpw = bottle.request.POST['login_current_password']
    newpw = bottle.request.POST['login_new_password']

    if not PYLOAD.changePassword(user, oldpw, newpw):
        print "Wrong password"
        return bottle.HTTPError()
