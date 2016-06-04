SublimeLinter-contrib-lslint [![Build Status](https://travis-ci.org/XenHat/SublimeLinter-contrib-lslint.svg?branch=master)](https://travis-ci.org/XenHat/SublimeLinter-contrib-lslint)
================================

This linter plugin for [SublimeLinter][docs] provides an interface to [lslint][makopo-lslint]. It will be used with files that have the `lsl` and `ossl` syntax.
If you do not know what a linter is or are new to SublimeLinter, please refer to the [SublimeLinter][docs] documentation.

Note: This plugin's packaging and installation process is still very much in it'ss infancy and not considered "final". Be aware that the edges are rough, may cut, and the author aknowledges them as not user-friendly. This is intented to be resolved.

## Requirements and dependencies

### Short version / Quick start:

Install [SublimeLinter 3][installation] and the [Sublime-text-lsl][makopo-subl-lsl] plugin and add the binaries provided by Sublime-text-lsl to your path.

### Long version / Advanced users:

#### SublimeLinter

SublimeLinter 3 must be installed in order to use this plugin. If SublimeLinter 3 is not installed, please follow the instructions [here][installation].

#### Sublime-Text-LSL

Currently, `sublimelinter-contrib-lslint` was developed as a companion to the [Sublime-text-lsl][makopo-subl-lsl] plugin. You are free to use the LSL/OSSL definition files and lslint binary of your choice, however compatibility can only be guaranteed with the [pclewis's lslint](https://github.com/pclewis/lslint) binary and their derivatives, including [Builder's Brewery's](https://github.com/buildersbrewery/linden-scripting-language) syntax files.

Bottom line: You need a linter executable and LSL/OSSL syntax definition files.

Before going any further, please read and follow the steps in [“Finding a linter executable”](http://sublimelinter.readthedocs.org/en/latest/troubleshooting.html#finding-a-linter-executable) through “Validating your PATH” in the documentation to ensure the linter is working properly with Sublime Text.

*Note: This plugin currently has a hard requirement of* `lslint` __0.4.2__ *or later.*

*Note 2: An experimental `lslint` binary pair is available at* [OciiDii-Works/lslint](https://github.com/Ociidii-Works/lslint) *which has been compiled with Microsoft Visual C++ 14/Visual Studio 2015 by me.*

## SublimeLinter-contrib-lsl installation

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

[docs]: http://sublimelinter.readthedocs.org
[installation]: http://sublimelinter.readthedocs.org/en/latest/installation.html
[locating-executables]: http://sublimelinter.readthedocs.org/en/latest/usage.html#how-linter-executables-are-located
[pc]: https://sublime.wbond.net/installation
[cmd]: http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html
[settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html
[linter-settings]: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html
[inline-settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html#inline-settings
[makopo-lslint]: https://github.com/Makopo/lslint
[makopo-subl-lsl]: https://github.com/Makopo/sublime-text-lsl

