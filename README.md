# SublimeLinter-contrib-lslint

[![Build Status](https://travis-ci.org/XenHat/SublimeLinter-contrib-lslint.svg?branch=master)](https://travis-ci.org/XenHat/SublimeLinter-contrib-lslint)
[![Packagecontrol total downloads](https://img.shields.io/packagecontrol/dt/SublimeLinter-contrib-lslint.svg?style=flat-square)](https://packagecontrol.io/packages/SublimeLinter-contrib-lslint/)
[![GitHub license](https://img.shields.io/github/license/XenHat/SublimeLinter-contrib-lslint.svg?style=flat-square)](https://github.com/XenHat/SublimeLinter-contrib-lslint/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/XenHat/SublimeLinter-contrib-lslint.svg?style=flat-square)](https://github.com/XenHat/SublimeLinter-contrib-lslint/issues?utf8=✓&q=is%3Aissue+is%3Aopen)

This [SublimeLinter 3](https://github.com/sublimelinter/sublimelinter3) plugin provides an interface to lslint ([pclewis/lslint](https://github.com/pclewis/lslint), [makopo/lslint](https://github.com/makopo/lslint), [ociidii-works/lslint](https://github.com/ociidii-works/lslint)).
This plugin applies linting to files that have the `lsl` and `ossl` syntax.
If you do not know what a linter is or are new to SublimeLinter, please refer to the [SublimeLinter documentation](http://www.sublimelinter.com/en/latest).

## Quick start

You're advised to install [Will Bond](https://wbond.net)'s [Package Control](https://packagecontrol.io) (see the [installation](https://packagecontrol.io/installation) page there) for [Sublime Text](https://www.sublimetext.com), which makes finding, installing and **keeping packages up-to-date** much easier.

### Requirements

* [Sublime Text](https://www.sublimetext.com)
* [SublimeLinter 3](https://github.com/sublimelinter/sublimelinter3) (see [installation](http://sublimelinter.readthedocs.org/en/latest/installation.html))
* `Sublimelinter-contrib-lslint` looks for the generic `lslint` executable by name, so you can use any derivative version of pclewis's original lslint you desire as long as its version is **0.4.2 or higher**:
  * [pclewis/lslint](https://github.com/pclewis/lslint)
  * [makopo/lslint](https://github.com/makopo/lslint)
  * [Ociidii-works/sublimelinter-contrib-lslint-bin](https://github.com/Ociidii-Works/sublimelinter-contrib-lslint-bin)
* for syntax highlighting and autocompletion of `lsl` and `ossl` syntax use:
  * [makopo/sublime-text-lsl](https://github.com/makopo/sublime-text-lsl) (also available on Package Control as `LSL`)
  * see `LSL` subfolder of [buildersbrewery/linden-scripting-language](https://github.com/buildersbrewery/linden-scripting-language)
* Windows users are recommended to use [cmderdev/cmder](https://github.com/cmderdev/cmder)
  * with lslint binary for windows in `cmder/bin/lslint.exe`
  * with ST3 dev **Portable** installed to `cmder/vendor/sublime`
  * with `subl="%CMDER_ROOT%\vendor\sublime\sublime_text.exe" $*` added to `cmder/config/aliases`

## Installation

In Sublime Text select from the menu `Tools > Command Palette` (see also [Command Palette](http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html)), select `Package Control: Install Package` and hit <kbd>Enter ↩</kbd>, then select `SublimeLinter-contrib-lslint` and hit <kbd>Enter ↩</kbd>.

## About linter executables

Please read the sections [`How linter executables are located`](http://sublimelinter.readthedocs.io/en/latest/usage.html#how-linter-executables-are-located) and [`Finding a linter executable`](http://sublimelinter.readthedocs.org/en/latest/troubleshooting.html#finding-a-linter-executable) in the SublimeLinter 3 documentation.

## Contributing

Please see [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md).

## Special thanks

* [@pclewis](https://github.com/pclewis) creating and/or providing lslint to the community
* [@makopo](https://github.com/makopo) for [makopo/sublime-text-lsl](https://github.com/makopo/sublime-text-lsl) and lslint improvements
