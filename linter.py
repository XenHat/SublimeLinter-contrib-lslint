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
import subprocess
import os

'''
SublimeLinter Installer
'''

import os
import sublime

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
    def which(cls, executable):
        """Find native lslint executable in Operating System path."""
        # 64 if windows64, otherwise nothing, will be appended to platform name below
        os_arch = ''
        if os.name == 'nt':
            output = subprocess.check_output(['wmic', 'os', 'get', 'OSArchitecture'])
            # extract number only and reverse automatic conversion to binary
            os_arch = output.split()[1][:2].decode('utf-8')
        lslpackagepath = os.path.join(sublime.packages_path(), 'LSL',sublime.platform()+os_arch,'lslint')
        print('SublimeLinter-contrib-lslint: Attempting to auto-configure lslint executable from LSL package at %s' % lslpackagepath)
        if os.name == 'nt':
            if os.access(lslpackagepath, os.F_OK):
                return lslpackagepath
            else:
                lslpackagepath = os.path.join(sublime.packages_path(), 'LSL',sublime.platform(),'lslint') # Attempt to fallback to 32-bit windows binary
                print('SublimeLinter-contrib-lslint: Attempting to auto-configure lslint executable from LSL package at %s' % lslpackagepath)

        return lslpackagepath
