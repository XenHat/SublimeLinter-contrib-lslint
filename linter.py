#!/usr/bin/env python
# coding: utf-8
#
# Linter for the Linden Scripting Language
# using SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by XenHat
# Copyright (c) 2016-2017 XenHat
#
# License: MIT

"""Provide an interface between lslint and SublimeLinter."""

import sublime
from SublimeLinter.lint import Linter, util
import os
import platform

'''
SublimeLinter Installer
'''

SUBL_LINTER_PKG = 'SublimeLinter'
PKGCTRL_SETTINGS = 'Package Control.sublime-settings'

PKG_NAME = os.path.splitext(
    os.path.basename(os.path.dirname(__file__))
)[0]

MSG = '''\
<div id="SublimeLinter-installer">
  <style>
    #SublimeLinter-installer {{
      padding: 1rem;
      line-height: 1.5;
    }}
    #SublimeLinter-installer code {{
      background-color: color(var(--background) blend(var(--foreground) 80%));
      line-height: 1;
      padding: 0.25rem;
    }}
    #SublimeLinter-installer a {{
      padding: 0;
      margin: 0;
    }}
  </style>

  {} requires <code>SublimeLinter</code> package.
  <br><br>Would you like to install it?<br>
  <br><a href="install">Install</a> <a href="cancel">Cancel</a>
</div>
'''.format(PKG_NAME)


def is_installed():
    """Check if the LSL package is installed."""
    pkgctrl_settings = sublime.load_settings(PKGCTRL_SETTINGS)

    return SUBL_LINTER_PKG in set(pkgctrl_settings.get('installed_packages', []))


def on_navigate(href):
    """Intermediary logic to install the package or hide the popup."""
    if href.startswith('install'):
        install()
    else:
        hide()


def install():
    """Install the LSL package from package control."""
    print('Installing "{}" ...'.format(SUBL_LINTER_PKG))
    sublime.active_window().run_command(
        'advanced_install_package', {'packages': SUBL_LINTER_PKG}
    )
    hide()


def hide():
    """Hide the install popup."""
    sublime.active_window().active_view().hide_popup()


def plugin_loaded():
    """Show a popup to the user to propose the installation of the LSL package."""
    from package_control import events

    if events.install(PKG_NAME) and not is_installed():
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


def look_for_linter(platform_and_binary):
    """Look in known subfolders for the linter binary."""

    binarypathfirst = os.path.join(sublime.packages_path(), 'LSL')
    # print("platform_and_binary: %s" % platform_and_binary)
    try:
        # sublime-text-lsl's 'LSL' package
        makopopath = os.path.join(binarypathfirst, platform_and_binary)
        if os.access(makopopath, os.F_OK):
            return makopopath
        # builder's brewery's 'LSL' package
        bbpath = os.path.join(binarypathfirst, 'bin', 'lslint', platform_and_binary)
        if os.access(bbpath, os.F_OK):
            return bbpath
    except IOError as e:
            print('%s' % e)
    return None


class Lslint(Linter):
    """Main implementation of the linter interface."""

    syntax = ('lsl')
    cmd = 'lslint -i'
    executable = 'lslint'
    version_args = '-V'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 0.4.2'
    regex = r'''(?xi)
        (?:(?P<warning> WARN)|(?P<error>ERROR))\:\:\s
        \(\s*(?P<line>\d+),\s*(?P<col>\d+)\)\:\s
        (?P<message>.*)
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
    def which(cls, executable):
        """Find native lslint executable."""

        os_cmd = executable + '.exe' if os.name == 'nt' else executable
        sublime_platform = sublime.platform()
        # print("platform: %s" % sublime_platform)
        if sublime_platform == 'windows':
            # bitness = platform.architecture()[0][:-3]
            # print("bitness: %s" % bitness)
            fullbinarypath = look_for_linter(os.path.join(
                sublime_platform if platform.release() == 'XP' else
                'windows' + platform.architecture()[0][:-3], os_cmd)
            )
        else:
            fullbinarypath = look_for_linter(os.path.join(sublime_platform, os_cmd))

        # print("Binary: %s" % fullbinarypath)
        if fullbinarypath is not None:
            return fullbinarypath
        return os_cmd
