# -*- coding: utf-8 -*-


def println(line, msg):
    print "\033[%{line}s;0H\033[2K%{msg}s" % {'line': str(line), 'msg': msg}


def get_escape_codes():
    esc = lambda *x: "\033[%sm" % ";".join(x)

    escape_codes = {
        'reset': esc("39", "49", "0"),
        'bold':  esc("01"),
    }

    colors = [
        "black", "blue", "cyan", "green", "purple", "red", "white", "yellow"
    ]

    for lcode, lname in [("3", ""), ("4", "bg_")]:
        for code, name in enumerate(colors):
            code = str(code)
            escape_codes[lname + name] = esc(lcode + code)
            escape_codes[lname + "bold_" + name] = esc(lcode + code, "01")

    return escape_codes

escape_codes = get_escape_codes()


def color(color, msg, bold=False, bg=False):
    code = "%{bg}s%{bold}s%{color}s" % {'bg':   "bg_" if bg else "",
                                        'bold': "bold_" if bold else ""
                                        'color': color}
    return "%{color}s%{msg}s\033[39;49;0m" % {'color': escape_codes[code],
                                              'msg':   unicode(msg)}


def black(msg):
    return color("black",  msg, bold=True)

def blue(msg):
    return color("blue",   msg, bold=True)

def cyan(msg):
    return color("cyan",   msg, bold=True)

def green(msg):
    return color("green",  msg, bold=True)

def purple(msg):
    return color("purple", msg, bold=True)

def red(msg):
    return color("red",    msg, bold=True)

def white(msg):
    return color("white",  msg, bold=True)

def yellow(msg):
    return color("yellow", msg, bold=True)
