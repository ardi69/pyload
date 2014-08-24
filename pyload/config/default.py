# -*- coding: utf-8 -*-

import os

from pyload.manager.JsEngine import ENGINES
from pyload.webui import SERVERS, THEME_DIR


"""
Configuration layout for default base config
"""

#@TODO: write tooltips and descriptions
#@TODO: use apis config related classes

def make_config(config=pycore.config):
    languages = "af;ar;bn;ca;cs;da;de;el;en;eo;es;fa;fi;fr;ga;gl;he;hi;hr;hu;id;it;ja;ko;ms;nl;no;pa;pl;pt;ro;ru;si;sq;sr;sv;te;tr;vi;zh"
    console_modes = "label;full"
    js_engines = "auto;" + ";".join(map(lambda x: x.NAME, ENGINES))
    webui_themes = ";".join(os.listdir(THEME_DIR))
    web_servers = "auto;builtin;" + ";".join(map(lambda x: x.NAME, SERVERS))
    proxy_protocols = "http;socks4;socks5"  #@TODO: add "https"

    config.addConfigSection("log", _("Log"), _("Description"), _("Long description"),
                            [
                                ("file_log", "bool", _("Save log to file"), True),
                                ("log_size", "int", _("File Size (in KB)"), 100),
                                ("log_folder", "folder", _("Folder"), "Logs"),
                                ("log_rotate", "bool", _("Rotate"), True),
                                ("log_count", "int", _("Count"), 5),
                            ])

    config.addConfigSection("permission", _("Permissions"), _("Description"), _("Long description"),
                            [
                                ("group", "str", _("Groupname"), "users"),
                                ("change_dl", "bool", _("Change Group and User of Downloads"), False),
                                ("change_file", "bool", _("Change file mode of downloads"), False),
                                ("user", "str", _("Username"), "user"),
                                ("file", "str", _("Filemode for Downloads"), "0644"),
                                ("change_group", "bool", _("Change group of running process"), False),
                                ("folder", "str", _("Folder Permission mode"), "0755"),
                                ("change_user", "bool", _("Change user of running process"), False),
                            ])

    config.addConfigSection("general", _("General"), _("Description"), _("Long description"),
                            [
                                ("language", languages, _("Language"), "EN"),
                                ("download_folder", "folder", _("Download Folder"), "Downloads"),
                                ("folder_per_package", "bool", _("Create Folder for each package"), True),
                                ("min_free_space", "int", _("Min Free Space to continue downloading (in MB)"), 512),
                                ("renice", "int", _("CPU Priority (nice notation)"), 0),
                                ("color_console", "bool", _("Colorize Console"), True),
                                ("color_mode", console_modes, _("Console Color Mode"), "label"),
                                ("jsengine", js_engines, _("JS Engine"), "auto"),
                                ("debug", "bool", _("Debug Mode"), False),
                            ])

    config.addConfigSection("ssl", _("SSL"), _("Description"), _("Long description"),
                            [
                                ("cert", "file", _("SSL Certificate"), "ssl.crt"),
                                ("key", "file", _("SSL Key"), "ssl.key"),
                            ])

    config.addConfigSection("webui", _("WebUI"), _("Description"), _("Long description"),
                            [
                                ("theme", webui_themes, _("UI Theme"), "default"),
                                ("server", web_servers, _("Web Server"), "auto"),
                                ("ssl", "bool", _("Use SSL (HTTPS)"), False),
                                ("host", "ip", _("IP Address"), "0.0.0.0"),
                                ("port", "int", _("IP Port"), 8001),
                                ("max_connections", "int", _("Max server connections"), 6),
                                ("debug", "bool", _("Debug Mode"), False),
                            ])

    config.addConfigSection("proxy", _("Proxy"), _("Description"), _("Long description"),
                            [
                                ("activated", "bool", _("Use Proxy"), False),
                                ("type", proxy_protocols, _("Protocol"), "http"),
                                ("host", "str", _("IP Address"), "localhost"),
                                ("port", "int", _("IP Port"), 7070),
                                ("username", "str", _("Username"), ""),
                                ("password", "password", _("Password"), ""),
                            ])

    config.addConfigSection("reconnect", _("Reconnect"), _("Description"), _("Long description"),
                            [
                                ("activated", "bool", _("Use Reconnect Script"), False),
                                ("method", "str", _("Script"), "reconnect.sh"),
                                ("start_time", "time", _("Start Time"), "0:00"),
                                ("end_time", "time", _("End Time"), "0:00"),
                            ])

    config.addConfigSection("download", _("Download"), _("Description"), _("Long description"),
                            [
                                ("max_downloads", "int", _("Max parallel downloads"), 3),
                                ("chunks", "int", _("Max connections for one download"), 3),
                                ("max_speed", "int", _("Max download speed (KB/s)"), -1),
                                ("limit_speed", "bool", _("Limit download speed"), False),
                                ("interface", "str", _("Download interface to bind (IP or name)"), ""),
                                ("skip_existing", "bool", _("Skip already existing files"), True),
                                ("ipv6", "bool", _("Allow IPv6"), False),
                                ("start_time", "time", _("Start Time"), "0:00"),
                                ("end_time", "time", _("End Time"), "0:00"),
                            ])

    config.addConfigSection("remote", _("Remote"), _("Description"), _("Long description"),
                            [
                                ("activated", "bool", _("Allow remote access"), False),
                                ("ssl", "bool", _("Use SSL"), False),
                                ("port", "int", _("IP Port"), 7227),
                                ("host", "ip", _("IP Address"), "0.0.0.0"),
                                ("nolocalauth", "bool", _("No authentication request by LAN access"), True),
                            ])
