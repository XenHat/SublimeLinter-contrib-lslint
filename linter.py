# Linter for the Linden Scripting Language
# using SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by XenHat
# Copyright (c) 2016-2017 XenHat
#
# License: MIT


import sublime
from SublimeLinter.lint import Linter, util
import os


LSL_PACKAGE = 'LSL'
PKGCTRL_SETTINGS = 'Package Control.sublime-settings'

LINTER_PACKAGE = 'SublimeLinter-contrib-lslint'

MSG = '''\
<div id="lsl-pkg-installer">
  <style>
    #lsl-pkg-installer {{
      padding: 1rem;
      line-height: 1.5;
    }}
    #lsl-pkg-installer code {{
      background-color: color(var(--background) blend(var(--foreground) 80%));
      line-height: 1;
      padding: 0.25rem;
    }}
    #lsl-pkg-installer a {{
      padding: 0;
      margin: 0;
    }}
  </style>

  {} requires <code>LSL</code> package for enhanced<br>support of
  the Linden Scripting Language.
  <br><br>Would you like to install it?<br>
  <br><a href="install">Install</a> <a href="cancel">Cancel</a>
</div>
'''.format(LINTER_PACKAGE)


def is_installed():
    pkgctrl_settings = sublime.load_settings(PKGCTRL_SETTINGS)
    return LSL_PACKAGE in set(pkgctrl_settings.get('installed_packages', []))


def on_navigate(href):
    if href.startswith('install'):
        install()
    else:
        hide()


def install():
    print('Installing `{}` ...'.format(LSL_PACKAGE))
    sublime.active_window().run_command(
        'advanced_install_package', {'packages': LSL_PACKAGE}
    )
    hide()


def hide():
    sublime.active_window().active_view().hide_popup()


def plugin_loaded():
        try:
            from package_control import events
            if events.install(LINTER_PACKAGE) and not is_installed() and int(sublime.version()) >= 3124:
                window = sublime.active_window()
                view = window.active_view()
                window.focus_view(view)
                row = int(view.rowcol(view.visible_region().a)[0] + 1)
                view.show_popup(
                    MSG,
                    location=view.text_point(row, 5),
                    max_width=800,
                    max_height=800,
                    on_navigate=on_navigate
                )
        except Exception as e:
            raise e


class Lslint(Linter):
    syntax = ('lsl', 'ossl')
    cmd = 'lslint'
    executable = 'lslint'
    version_args = '-V'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 0.4.2'
    regex = r'''(?xi)
    ((?P<warning> WARN)|(?P<error>ERROR))
    \:\:\s\(\s*(?P<line>\d+),\s*(?P<col>\d+)
    \)\:\s(?P<message>.*)
    '''
    multiline = True
    line_col_base = (1, 1)
    tempfile_suffix = 'lsl'
    error_stream = util.STREAM_BOTH
    selectors = {}
    word_re = None
    defaults = {}
    inline_settings = None
    inline_overrides = None
    comment_re = None

    @classmethod
    def which(cls, cmd):
        if not is_installed():
            # we assume the 'lslint' executable is in our PATH
            return None
        elif sublime.platform() == 'linux':
            return os.path.join(sublime.packages_path(), 'LSL', 'linux', 'lslint')
        elif sublime.platform() == 'osx':
            return os.path.join(sublime.packages_path(), 'LSL', 'osx', 'lslint')
        else:
            return os.path.join(sublime.packages_path(), 'LSL', 'windows', 'lslint.exe')
