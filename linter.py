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
import re

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


def look_for_linter(os_cmd):
    """Look in known subfolders for the linter binary."""

    sublime_platform = sublime.platform().strip()
    # print("sublime_platform: %s" % sublime.platform())
    binarypathfirst = os.path.join(sublime.packages_path(), 'LSL')
    try:
        # Makopo's 'LSL' package
        fullbinarypath = os.path.join(binarypathfirst, sublime_platform, os_cmd)
        if os.access(fullbinarypath, os.F_OK):
            return fullbinarypath
        # builder's brewery's 'LSL' package
        # print ('os_cmd: %s' % os_cmd)
        if sublime_platform == 'windows':
            arch = platform.architecture()[0][:-3]
            fullbinarypath = os.path.join(binarypathfirst,
                                          'bin',
                                          'lslint',
                                          sublime_platform + (arch if platform.release() is not 'XP' else None), os_cmd)
        else:
            fullbinarypath = os.path.join(binarypathfirst, 'bin', 'lslint', sublime_platform, os_cmd)

        # print("Trying %s" % fullbinarypath)
        if os.access(fullbinarypath, os.F_OK):
            return fullbinarypath
    except IOError as e:
            print('%s' % e)
    return None

def look_for_mcpp():
    """ Try to find mcpp preprocessor """
    mcpp_binary_name = 'mcpp' + '.exe' if os.name == 'nt' else None
    mcpp_binary_path = ospath_to_explicit(mcpp_binary_name)
    # print("DEBUG:: MCPP: %s" % mcpp_binary_path)
    if mcpp_binary_path is not None:
        if os.access(mcpp_binary_path, os.F_OK):
            return mcpp_binary_path
    return None


def ospath_to_explicit(program):
    """ From https://stackoverflow.com/a/377028/1570096 """
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def remove_line_directives(my_string):
    """ Not a good solution"""
    # return re.sub("^#line.*\n","",my_string)
    return re.sub(r'(?m)^\#line.*\n?', '', my_string)

class Lslint(Linter):
    """Main implementation of the linter interface."""

    syntax = ('lsl')
    executable = 'lslint'
    version_args = '-V'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 1.0.4'
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
    inline_settings = None
    inline_overrides = None
    comment_re = None

    @classmethod
    def cmd(self):
        """ Override cmd definition/function """
        print("DEBUG :: self.executable.path: %s" % self.executable_path)
        # TODO: Add user-configurable setting for these
        # return [self.executable_path, '-m','-l','-S','-#','-i','-u','-w', '-z']
        return [self.executable_path, '-m','-l','-S','-#','-i','-u','-w']

    @classmethod
    def which(cls, executable):
        """Find native lslint executable."""

        # Look in System path first, then search if not found
        lslint_binary_name = executable + '.exe' if os.name == 'nt' else executable
        lslint_binary_path = ospath_to_explicit(lslint_binary_name)
        if lslint_binary_path is None:
            lslint_binary_path = look_for_linter(lslint_binary_name)

        # print("DEBUG:: LSLINT: %s" % lslint_binary_path)
        # print("whet: %s" % communicate(self, mcpp_found, code))
        return lslint_binary_path

    @classmethod
    def run(self, cmd, code):
        """ Override the default run command to inject preprocessor step """
        # print("DEBUG:: CMD: %s" % cmd)
        mcpp_path = look_for_mcpp()
        linter_result = Linter.communicate(self,mcpp_path,Linter.communicate(self,cmd,code)) \
                    if mcpp_path is not None else Linter.communicate(self,cmd,code)
        # print("DEBUG:: output: %s" % linter_result)
        return linter_result
