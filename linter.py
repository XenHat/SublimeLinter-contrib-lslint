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

from collections import namedtuple

'''
SublimeLinter Installer
'''

PKG_NAME = __package__.split('.')[0]
PKGCTRL_SETTINGS = 'Package Control.sublime-settings'
SUBLINTER_PKG = 'SublimeLinter'


def plugin_loaded():
    """Do something when the plugin is loaded."""
    try:
        from package_control import events
        packagecontrol_settings = sublime.load_settings(PKGCTRL_SETTINGS)
        sublinter_installed = (SUBLINTER_PKG in
                               set(packagecontrol_settings.get(
                                   'installed_packages', [])))
        if events.install(PKG_NAME) and not sublinter_installed:
            sublime.active_window().run_command('advanced_install_package',
                                                {'packages': SUBLINTER_PKG})
    except Exception as e:
        print('%s' % (str(e)))


class Lslint(Linter):
    """Main implementation of the linter interface."""

    syntax = ('lsl', 'ossl')
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

    def winpath(pf, firstp, cmd):
        """Get conditional path for Microsoft(R) Windows OS."""
        arch = platform.architecture()[0][:-3]
        w = pf + (arch if platform.release() is not 'XP' else None)
        return os.path.join(firstp, 'bin', 'lslint', w, cmd)

    def find_linter(os_cmd):
        """Look in known subfolders for the linter binary."""
        st_pf = sublime.platform().strip()
        parfhalf = os.path.join(sublime.packages_path(), 'LSL')
        try:
            # Makopo's 'LSL' package
            binpath = os.path.join(parfhalf,
                                   st_pf, os_cmd)
            if os.access(binpath, os.F_OK):
                return binpath
            # builder's brewery's 'LSL' package
            if st_pf == 'windows':
                binpath = Lslint.winpath(st_pf, parfhalf, os_cmd)
            else:
                binpath = os.path.join(parfhalf,
                                       'bin',
                                       'lslint',
                                       st_pf,
                                       os_cmd)

            if os.access(binpath, os.F_OK):
                return binpath
        except IOError as e:
            print('ERROR: {0}'.format(e))
        return None

    def fullpath(program):
        """From https://stackoverflow.com/a/377028/1570096."""
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

    def find_mcpp():
        """Try to find mcpp preprocessor."""
        mcpp_binary_name = 'mcpp' + '.exe' if os.name == 'nt' else None
        mcpp_binary_path = Lslint.fullpath(mcpp_binary_name)
        if mcpp_binary_path is not None:
            if os.access(mcpp_binary_path, os.F_OK):
                return mcpp_binary_path
        return None

    def remove_line_directives(my_string):
        """Not a good solution."""
        # return re.sub("^#line.*\n","",my_string)
        return re.sub(r'(?m)^\#line.*\n?', '', my_string)

    def getLastOffset(T, inlined_line):
        """Yeah."""
        result = 0
        for rest in T:
            for line in rest.pline:
                if int(rest.pline) >= inlined_line:
                    # Woah, use last result
                    break
                result = rest.pline
        return result

    @classmethod
    def cmd(self):
        """Override cmd definition/function."""
        # TODO: Add user-configurable setting for these
        # return [self.executable_path, '-m',
        #                               '-l',
        #                               '-S',
        #                               '-#',
        #                               '-i',
        #                               '-u',
        #                               '-w',
        #                               '-z']
        return [self.executable_path, '-m', '-i']

    @classmethod
    def which(cls, executable):
        """Find native lslint executable."""

        # Look in System path first, then search if not found
        lslint_binary_name = executable + ('.exe' if os.name == 'nt'
                                           else executable)
        lslint_binary_path = Lslint.fullpath(lslint_binary_name)
        if lslint_binary_path is None:
            lslint_binary_path = Lslint.find_linter(lslint_binary_name)
        return lslint_binary_path

    @classmethod
    def run(self, cmd, code):
        """Override the default run command to inject preprocessor step."""
        mcpp_path = Lslint.find_mcpp()
        # if mcpp_path is not None else Linter.communicate(self,cmd,code)
        if mcpp_path is not None:
            # Capture mcpp output and store into a variable
            mcpp_output = Linter.communicate(self, mcpp_path, code)
            lines = mcpp_output.splitlines(False)
            lc = 0
            OutputTuple = namedtuple('OutputTuple', 'pline tline file')
            preproc_bank = []
            for line in lines:
                if(line.startswith('#line')):
                    message = line.split(' ')
                    # print('message:{0}'.format(message))
                    preproc_bank.append(OutputTuple(pline=str(lc),
                                                    tline=message[1],
                                                    file=message[2]))
                lc += 1
            code = mcpp_output
            # print("DEBUG:: preproc_bank: {0}".format(preproc_bank[2]))

        linter_result = Linter.communicate(self, cmd, code)
        # print("DEBUG:: Linter output: {0}".format(linter_result))
        if mcpp_path is not None:
            # Go through every error and replace the line number (from the
            # inlined file) with the one from the script we fed the
            # precompiler, to restore the link between the error and the code
            # inside the editor so that we can properly show linting visual
            # hints.
            linter_output_lines = linter_result.splitlines(False)
            # print('LINTER_OUT:{0}'.format(linter_output_lines))
            # Get line at which the current file was inserted
            # TODO: make sure multi-include works
            fixed_output_lines = []
            for lint_line in linter_output_lines:
                if lint_line.startswith("TOTAL::") is False:
                    # print('LINE:[{0}]'.format(lint_line))
                    tokens = lint_line.split(',')
                    # print('Tokens:[{0}]'.format(tokens))
                    token = tokens[0]
                    # print("Token:{0}".format(token))
                    token = token.replace("ERROR:: (", "")
                    token = token.replace("WARN:: (", "")
                    # print("Token:{0}".format(token))
                    number = token.strip()
                    n_int = int(number)
                    # print("String attempt:{0}".format(number))
                    offset = Lslint.getLastOffset(preproc_bank, n_int)
                    # print("Offset: {0}".format(offset))
                    something = n_int - int(offset)
                    new_line = lint_line.replace(number, str(something))
                    # print("Something: {0}".format(something))
                    # print("New Line: {0}".format(new_line))
                    fixed_output_lines.append(new_line)
                    continue
                else:
                    fixed_output_lines.append(lint_line)

            # print("New Lines: {0}".format(fixed_output_lines))
            # Transform back into a string
            linter_result = "".join(str(x) for x in fixed_output_lines)

        # print("DEBUG:: Linter output: {0}".format(linter_result))
        return linter_result
