# SublimeLinter-contrib-lslint

[![Build Status](https://travis-ci.org/XenHat/SublimeLinter-contrib-lslint.svg?branch=master)](https://travis-ci.org/XenHat/SublimeLinter-contrib-lslint)
[![Packagecontrol total downloads](https://img.shields.io/packagecontrol/dt/SublimeLinter-contrib-lslint.svg?style=flat-square)](https://packagecontrol.io/packages/SublimeLinter-contrib-lslint/)
[![GitHub license](https://img.shields.io/github/license/XenHat/SublimeLinter-contrib-lslint.svg?style=flat-square)](https://github.com/XenHat/SublimeLinter-contrib-lslint/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/XenHat/SublimeLinter-contrib-lslint.svg?style=flat-square)](https://github.com/XenHat/SublimeLinter-contrib-lslint/issues?utf8=✓&q=is%3Aissue+is%3Aopen)

This [SublimeLinter 3](https://github.com/sublimelinter/sublimelinter3) plugin provides an interface to lslint.
This plugin applies linting to files that have the `lsl` and `ossl` syntax.
If you do not know what a linter is or are new to SublimeLinter, please refer to the [SublimeLinter documentation](http://www.sublimelinter.com/en/latest).

## Quick start

You're advised to install [Will Bond](https://wbond.net)'s [Package Control](https://packagecontrol.io) (see the [installation](https://packagecontrol.io/installation) page there) for [Sublime Text](https://www.sublimetext.com), which makes finding, installing and **keeping packages up-to-date** much easier.

### Requirements

* [Sublime Text](https://www.sublimetext.com)
* [SublimeLinter 3](https://github.com/sublimelinter/sublimelinter3) (see [installation](http://sublimelinter.readthedocs.org/en/latest/installation.html))

## Linter executable

`Sublimelinter-contrib-lslint` looks for the generic `lslint` executable by name, therefore is compatible with most derivative versions of pclewis's original lslint. *Note: This linter plugin is configured to support version **0.4.2 or higher**.*

The plugin will propose to install the [LSL](https://github.com/Makopo/sublime-text-lsl) package if it cannot detect `lslint` in your path.

A more frequently updated version of `lslint` is available at [makopo/lslint](https://github.com/makopo/lslint), and is fully compatible with this linter.

## Installation

In Sublime Text select from the menu `Tools > Command Palette` (see also [Command Palette](http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html)), select `Package Control: Install Package` and hit <kbd>Enter ↩</kbd>, then select `SublimeLinter-contrib-lslint` and hit <kbd>Enter ↩</kbd>.

## Contributing

Please see [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md).

## Special thanks

* [@pclewis](https://github.com/pclewis) creating and/or providing lslint to the community
* [@makopo](https://github.com/makopo) for [makopo/sublime-text-lsl](https://github.com/makopo/sublime-text-lsl) and lslint improvements
* [@buildersbrewery](https://github.com/buildersbrewery) for care, feeding and additional tips
