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
import os
import platform
import re
from SublimeLinter.lint import Linter, util
from collections import namedtuple

'''
SublimeLinter Installer
'''


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
            binpath = winpath(st_pf, parfhalf, os_cmd)
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


def smart_bin_name(name):
    """Return the proper binary name on all platforms."""
    return name + ('.exe' if os.name == 'nt' else '')


def find_mcpp():
        """Try to find mcpp preprocessor."""
        mcpp_binary_name = smart_bin_name('mcpp')
        mcpp_binary_path = fullpath(mcpp_binary_name)
        if mcpp_binary_path is not None:
            if os.access(mcpp_binary_path, os.F_OK):
                return mcpp_binary_path
        return None


def getLastOffset(tuples_list, inlined_line):
    """Yeah."""
    result = 0  # Fallback if there is no directives.
    line = 0
    filename = '"<stdin>"'
    for this_tuple in tuples_list:
        if int(this_tuple.mcpp_in_line) >= inlined_line - 1:
            # We reached a #line directive further than the one
            # we are looking for; Do not store this instance and
            # return the previous one instead. This assumes a few things.
            break
        line += 1
        result = this_tuple.mcpp_in_line - this_tuple.orig_line + 2
        filename = this_tuple.file

    # print('result: {0},{1}'.format(result, filename))
    # This will return 0 if there is no #line found
    return (result, filename)


def getLastStdin(tuples_list, inlined_line):
    """Return the last line containing <stdin> up to an line number."""
    # print("inlined_line: {0}".format(inlined_line))
    result = -1  # Fallback if there is no directives.
    for index in range(len(tuples_list)):
        this_tuple = tuples_list[index]
        if int(this_tuple.mcpp_in_line) >= inlined_line - 1:
            break
        if this_tuple.file == '"<stdin>"':
            result = index

    # print("Last stdin: {0}".format(result))
    return result


def getLastLine(tuples_list, inlined_line):
    """Yeah."""
    # print("inlined_line2: {0}".format(inlined_line))
    result = 0  # Fallback if there is no directives.
    line = 0
    for this_tuple in tuples_list:
        if int(this_tuple.mcpp_in_line) > inlined_line + 2:
            # We reached a #line directive further than the one
            # we are looking for; Do not store this instance and
            # return the previous one instead. This assumes a few things.
            break
        # print("[{1}] line: '{0}'".format(this_tuple.file, line))
        if this_tuple.file != '"<stdin>"':
            result = line
        line += 1

    # print("Last line: {0}".format(result))
    # This will return 0 if there is no #line found
    return result


def get_auto_padding(number):
    """Automatically pad the number ."""
    if(number < 10):
        return str(number) + "   "
    if(number < 100):
        return str(number) + "  "
    if(number < 1000):
        return str(number) + " "
    return str(number)


class Lslint(Linter):
    """Main implementation of the linter interface."""

    syntax = ('lsl', 'ossl')
    executable = 'lslint'
    version_args = '--version'
    version_requirement = '>= 1.0.6'
    regex = r'''(?xi)(?:(?P<warning>\sWARN)|(?P<error>ERROR))\:\:\s\(\s*(?P<line>\d+),\s*(?P<col>\d+)\)\:\s(?P<message>.*)'''  # noqa: E501
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
        return [self.executable_path, '-m', '-w', '-z', '-i']

    @classmethod
    def which(cls, executable):
        """Find native lslint executable."""

        # Look in System path first, then search if not found
        lslint_binary_name = smart_bin_name(executable)
        lslint_binary_path = fullpath(lslint_binary_name)
        if lslint_binary_path is None:
            lslint_binary_path = find_linter(lslint_binary_name)
        return lslint_binary_path

    @classmethod
    def run(self, cmd, code):
        """Override the default run command to inject preprocessor step."""
        # print('=== BEGIN LINTER DEBUG ===')
        # print('ORIGINAL_CODE:')
        # o_lines = code.splitlines(False)
        # o_n = 0
        # for o_l in o_lines:
        #     print('{0} |{1}'.format(get_auto_padding(o_n), o_l))
        #     o_n += 1

        mcpp_path = find_mcpp()
        # if mcpp_path is not None else Linter.communicate(self,cmd,code)
        if mcpp_path is not None:
            opt = '-W0'
            mcpp_output = Linter.communicate(self, (mcpp_path, opt), code)
            lines = mcpp_output.splitlines(False)
            line_number = 0
            OutputTuple = namedtuple('OutputTuple', 'mcpp_in_line\
                                                     orig_line\
                                                     file')
            MCPPMessage = namedtuple('MCPPMessage', 'source\
                                                     line\
                                                     message')
            preproc_bank = []
            # print('MCPP Output:')
            mcpp_messages = []
            for line in lines:
                # print('{0} |{1}'.format(get_auto_padding(line_number), line))
                if(line.startswith('#line')):
                    message = line.split(' ')
                    # print('message:{0}'.format(message))
                    preproc_bank.append(OutputTuple(mcpp_in_line=line_number,
                                                    orig_line=int(message[1]),
                                                    file=message[2]))

                elif(line.startswith('<stdin>:')):
                    # Capture mcpp output and store into a variable
                    message = line.split(':')
                    mcpp_messages.append(MCPPMessage(
                        source=message[0],
                        line=message[1],
                        message=message[3]))
                line_number += 1
            # print("DEBUG:: preproc_bank: {0}".format(preproc_bank[0]))
            linter_result = Linter.communicate(self, cmd, mcpp_output)
            # print("DEBUG:: LINTER_OUT output:\n{0}".format(linter_result))

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
            p = re.compile('^\s*(ERROR|\sWARN)\:\:\s\(\s*(\d*)\.*$')
            for iter_line in linter_output_lines:
                # print('LINE:[{0}]'.format(iter_line))
                if iter_line.startswith("TOTAL::") is False:
                    tokens = iter_line.split(',')
                    # print('Tokens:[{0}]'.format(tokens))
                    rres = p.match(tokens[0])
                    if rres is not None:
                        number = int(rres.group(2))
                        # print("number: '{0}'".format(number))
                        result = getLastOffset(preproc_bank, number)
                        offset = result[0]
                        # print("Offset: {0}".format(offset))
                        # tokminoff = str(number - int(offset))
                        tokminoff = str(number - int(offset))
                        new_line = re.sub(str(number), tokminoff, iter_line)
                        # print("result[1]="+result[1])
                        if result[1] != '"<stdin>"':
                            index = getLastStdin(preproc_bank, number)
                            new_number = preproc_bank[index + 1].mcpp_in_line + 1
                            offset = getLastOffset(preproc_bank, new_number)[0]
                            tokminoff = str(new_number - int(offset))
                            token_match = rres.group(1)
                            new_line = '{0}:: ({1:>3},  1): in file {2}: {3}'\
                                .format(token_match,
                                    tokminoff,
                                    result[1],
                                    new_line)
                        fixed_output_lines.append(new_line)
                    else:
                            continue 
                    continue
                else:
                    fixed_output_lines.append(iter_line)

            # print("New Lines: {0}".format(fixed_output_lines))
            # Transform back into a string
            # Add messages from MCPP first
            mcpp_msg_out = ""
            for this_tuple in mcpp_messages:
                mcpp_msg_out += "ERROR:: ({0},1): {1}\n".format(
                    this_tuple.line, this_tuple.message)
            print("MCPP:\n"+mcpp_msg_out)
            linter_result = mcpp_msg_out
            linter_result += "".join(str(x) + "\n" for x in fixed_output_lines)

            print("LINTER:\n"+linter_result)
        else:
            linter_result = Linter.communicate(self, cmd, code)

        # print("DEBUG:: Linter output: {0}".format(linter_result))
        # print('=== END LINTER DEBUG ===')
        return linter_result
