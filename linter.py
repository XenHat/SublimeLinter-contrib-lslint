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


class Lslint(Linter):
    """Main implementation of the linter interface."""

    syntax = ('lsl')
    cmd = 'lslint'
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
    def which(cls, cmd):
        """Find native lslint executable in Operating System path."""

        # NOTE to Windows users: At the time of writing, there are 3 possible lslint
        # executables:
        #   'lslint_v1.0.5_win.zip', for 32-bit Windows XP
        #   'lslint_v1.0.5_win32.zip' for 32-bit modern Windows
        #   'lslint_v1.0.5_win64.zip' for 64-bit modern Windows
        #
        # For simplity's sake, this autoconfigure script will only look inside
        #   'Packages/LSL/windows', which is the provided directory
        # until the need to suppor ta very roamy installation across machines
        # that cannot unify their operating systems.
        binarypathfirst = os.path.join(sublime.packages_path(), 'LSL')
        if os.name == 'nt':
            cmd += '.exe'
        binarypathlast = os.path.join(sublime.platform(), cmd)
        # if (os.access(binarypath, os.F_OK)):
        try:
            logprefix = 'SublimeLinter: lslint'
            # Binary in path
            # Does not appear to work yet
            # print(logprefix, "Testing [%s]" % cmd)
            # if os.access(cmd, os.F_OK):
            #     print(logprefix, 'Auto-configured lslint binary: [%s]' % cmd)
            #     return cmd
            # sublime-text-lsl's 'LSL' package
            # print(logprefix, "Testing [%s]" % combinedpath)
            combinedpath = os.path.join(binarypathfirst, binarypathlast)
            if os.access(combinedpath, os.F_OK):
                print(logprefix, 'Auto-configured lslint binary: [%s]' % combinedpath)
                return combinedpath
            # builder's brewery's 'LSL' package
            bbpath = os.path.join(binarypathfirst, 'bin', 'lslint', binarypathlast)
            # print(logprefix, "Testing [%s]" % bbpath)
            if os.access(bbpath, os.F_OK):
                print(logprefix, 'Auto-configured lslint binary: [%s]' % bbpath)
                return bbpath
        except IOError as e:
            print(logprefix, 'Could not find a binary to use! (%s)' % e)

        return None
