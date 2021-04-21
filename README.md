A GUI program built with Python 3 and PySimpleGUI for developing [PKSM-Scripts](https://github.com/FlagBrew/PKSM-Scripts)


## Development
To run the source code, you need Python 3.6 or above as well as the `PySimpleGUI` package

```
pip install --upgrade PySimpleGUI
```

A note about PySimpleGUI's compatibility with Python versions (from [its own documentation](https://pysimplegui.readthedocs.io/en/latest/#hardware-and-os-support)):

> Warning - tkinter + Python 3.7.3 and later, including 3.8 has problems
>
> The version of tkinter that is being supplied with the 3.7.3 and later versions of Python is known to have a problem with table colors. Basically, they don't work. As a result, if you want to use the plain PySimpleGUI running on tkinter, you should be using 3.7.2 or less. 3.6 is the version PySimpleGUI has chosen as the recommended version for most users.


### To Do
- [ ] GUI
    - [ ] Save Research (container tab)
        - [x] Save file selection (column)
        - [ ] Actions (tab group)
            - [ ] Save file raw diff (tab)
            - [ ] Save file event diff (tab)
            - [ ] Save search (tab)
            - [ ] Dump data (tab)
    - [x] Script compilation (tab)
    - [x] PKSM Communication (tab)
- [ ] backend
    - [ ] Save Research
        - [ ] load save file(s)
        - [ ] save file raw diff
        - [ ] save file event diff
        - [ ] search save data for value
        - [ ] dump data
    - [ ] `.pksm` script compilation
    - [ ] script sending
