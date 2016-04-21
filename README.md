SublimeLinter-contrib-lslint
================================

[![Build Status](https://travis-ci.org/XenHat/SublimeLinter-contrib-lslint.svg?branch=master)](https://travis-ci.org/XenHat/SublimeLinter-contrib-lslint)

This linter plugin for [SublimeLinter][docs] provides an interface to [lslint][lslint-homepage]. It will be used with files that have the `lsl` and `ossl` syntax.

## Installation
SublimeLinter 3 must be installed in order to use this plugin. If SublimeLinter 3 is not installed, please follow the instructions [here][installation].

### Linter installation
Before using this plugin, you must ensure that the `sublime-text-lsl` plugin is installed as it provides both the lslint binary and the syntax definitions required for this linter to work.

* Refer to [Makopo/sublime-text-lsl](https://github.com/Makopo/sublime-text-lsl) and add the binary provided by the plugin to your path. Automatic configuration *may* happen in the future.

**Note** *This plugin requires* `lslint` __0.4.2__ *or later.*

### Linter configuration
In order for `lslint` to be executed by SublimeLinter, you must ensure that its path is available to SublimeLinter. Before going any further, please read and follow the steps in [“Finding a linter executable”](http://sublimelinter.readthedocs.org/en/latest/troubleshooting.html#finding-a-linter-executable) through “Validating your PATH” in the documentation.

Once you have installed and configured `lslint`, you can proceed to install the SublimeLinter-contrib-lslint plugin if it is not yet installed.

**Note** *An experimental binary pair is available at* [OciiDii-Works/lslint](https://github.com/Ociidii-Works/lslint) *which has been compiled with VS2015 and may eventually provide better, linter-friendly output.*

### Plugin installation

**Note** This package is not yet in the public repository. To use this linter immediately, please add this repository to the package manager as described in the [package manager user manual](https://packagecontrol.io/docs/usage).
Then, you can proceed to  the installation as usual:


Please use [Package Control][pc] to install the linter plugin. This will ensure that the plugin will be updated when new versions are available. If you want to install from source so you can modify the source code, you probably know what you are doing so we won't cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette][cmd] and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `lslint`. Among the entries you should see `SublimeLinter-contrib-lslint`. If that entry is not highlighted, use the keyboard or mouse to select it.

## Settings

No settings yet.

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
[lslint-homepage]: https://github.com/Makopo/lslint