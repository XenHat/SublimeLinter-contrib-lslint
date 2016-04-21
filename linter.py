#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by xenhat
# Copyright (c) 2016 xenhat
#
# License: MIT
#

"""This module exports the Lslint plugin class."""

from SublimeLinter.lint import Linter, util


class Lslint(Linter):
    """Provides an interface to lslint."""

    syntax = ('lsl', 'ossl')
    cmd = 'lslint'
    executable = None
    version_args = '-V'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 0.4.2'
    regex = r'''(?xi)
    ((?P<warning> WARN)|(?P<error>ERROR))
    \:\:\s\(\s+(?P<line>\d+),\s+(?P<col>\d+)
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
