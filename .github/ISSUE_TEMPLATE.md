# Description 
Optional, remove me if none

### Offending code
```lsl
// Your Code Here
default {
    state_entry() {
        wat
    }
}
```

## Linter output
```
// Replace this block of text with the similar output from Sublime Text's Console (View->Show Console)
SublimeLinter: lslint output:
TOTAL:: Errors: 0  Warnings: 0 
```

### Similar Code without the issue
```lsl
// Your Code Here
default {
    state_entry() {
        integer wat = "";
    }
}
```

## My environment

* Operating system: `...`
* Sublime Text Build `...` on branch `stable`
* lslint version `...` from `release`
* SublimeLinter version `...`
* SublimeLinter-contrib-lslint version `...`
