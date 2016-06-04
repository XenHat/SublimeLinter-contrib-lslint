SublimeLinter-contrib-lslint [![Build Status](https://travis-ci.org/XenHat/SublimeLinter-contrib-lslint.svg?branch=master)](https://travis-ci.org/XenHat/SublimeLinter-contrib-lslint)
================================

This linter plugin for [SublimeLinter][docs] provides an interface to `lslint`.
It will be used with files that have the `lsl` and `ossl` syntax.

If you do not know what a linter is or are new to SublimeLinter, please refer to the [SublimeLinter][docs] documentation.

## 1. Requirements and dependencies

You need to provide a `lslint` binary for this linter to function.

#### Quick Start:

* Install [SublimeLinter 3][installation]
* Download/clone [my standalone binaries repo][ocdlslint] and [augment your path](https://sublimelinter.readthedocs.io/en/latest/troubleshooting.html#finding-a-linter-executable) with them.

Continue to Step 2.

##### Advanced users:

`Sublimelinter-contrib-lslint` looks for the generic `lslint` executable by name, so you can use any derivative version of [pclewis's lslint](https://github.com/pclewis/lslint) you desire, as long as its version is **0.4.2 or higher**.

Beside my own, common repository/packages including `lslint` are:
 * [Sublime-text-lsl][makopo-subl-lsl] Package (Available in Package Control)
 * [pclewis's original lslint][pclewis]
 * [Builder's Brewery LSL](https://github.com/buildersbrewery/linden-scripting-language)

## 2. Installing the linter

Please use [Package Control][pc] to install the linter plugin. This will ensure that the plugin will be updated when new versions are available. If you want to install from source so you can modify the source code, you probably know what you are doing so we won't cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette][cmd] and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `lslint`. Among the entries you should see `SublimeLinter-contrib-lslint`. If that entry is not highlighted, use the keyboard or mouse to select it.

## Settings

No settings yet. It Just Works.

## Contributing
If you would like to contribute enhancements or fixes, please do the following:

1. Fork the plugin repository.
1. Hack on a separate topic branch created from the latest `master`.
1. Commit and push the topic branch.
1. Make a pull request.
1. Be patient.  ;-)

Please note that modifications should follow these coding guidelines:

- Indent is 4 spaces.
- Code should pass flake8 and pep257 linters.
- Vertical whitespace helps readability, don’t be afraid to use it.
- Please use descriptive variable names, no abbreviations unless they are very well known.

Thank you for helping out!

## Special Thanks

* [Makopo][makopo-subl-lsl] for Sublime-Text-LSL and lslint improvements
* [pclewis][pclewis] for creating and/or providing lslint to the community

[cmd]: http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html
[docs]: https://sublimelinter.readthedocs.io/en/latest/
[installation]: https://sublimelinter.readthedocs.io/en/latest/installation.html
[linter-settings]: https://sublimelinter.readthedocs.io/en/latest/linter_settings.html
[locating-executables]: https://sublimelinter.readthedocs.io/en/latest/usage.html#how-linter-executables-are-located
[makopo-lslint]: https://github.com/Makopo/lslint
[makopo-subl-lsl]: https://github.com/Makopo/sublime-text-lsl
[ocdlslint]: https://github.com/Ociidii-Works/sublimelinter-contrib-lslint-bin
[pc]: https://sublime.wbond.net/installation
[pclewis]: https://github.com/pclewis/lslint
