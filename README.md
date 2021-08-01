A GUI program built with Python 3 and PySimpleGUI for developing [PKSM-Scripts](https://github.com/FlagBrew/PKSM-Scripts)


## Development
To run the source code, you need Python 3.6 or above as well as the `PySimpleGUI` package

```
pip install --upgrade PySimpleGUI
```

After which the GUI can be started up with
```
py gui.py
```

### Compatibility Notes
A note about PySimpleGUI's compatibility with Python versions (from [its own documentation](https://pysimplegui.readthedocs.io/en/latest/#hardware-and-os-support)), which may or may not be out-of-date by now:

> Warning - tkinter + Python 3.7.3 and later, including 3.8 has problems
>
> The version of tkinter that is being supplied with the 3.7.3 and later versions of Python is known to have a problem with table colors. Basically, they don't work. As a result, if you want to use the plain PySimpleGUI running on tkinter, you should be using 3.7.2 or less. 3.6 is the version PySimpleGUI has chosen as the recommended version for most users.

\* - This table color bug seems to have been fixed, according to [this issue](https://github.com/PySimpleGUI/PySimpleGUI/issues/1286)

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
        - [x] file select
        - [x] 3DS IP
        - [x] alternate script name (optional alternate name for script to be sent to PKSM instead of file name)
- [ ] backend
    - [ ] Save Research
        - [ ] load save file(s)
        - [ ] save file raw diff
        - [ ] save file event diff
        - [ ] search save data for value
        - [ ] dump data
    - [x] `.pksm` script compilation
        - [x] argument validation
        - [x] warning/error reporting
        - [x] file creation
        - [x] move compiled script to output directory
    - [ ] script sending
        - [x] file selection
        - [x] IP input with validation
        - [ ] alternate script name
        - [ ] send script
            - [ ] send name size
            - [ ] send name
            - [ ] send file size
            - [ ] send file contents


## GUI Idea Notes
- Save Research
    - left-hand panel: Save Files
    - right-hand panel: tab groups
        1. Save Diff
            - table-like: differences in sets of save data
                - columns
                    - Offset
                    - Save 1
                    - ...
                    - Save N
                    - Meaning (optional)
            - button: Export Diff (write save diff to file a la current diff script)
        2. Event Diff
            - table-like: differences in Event Flags and Constants of sets of save data
            - button: Export Diff (write save diff to file a la current diff script)
        3. Search
            - radio: hex, decimal, string
            - dropdown-like: save file to search
            - dropdown-like: data size to search (byte, short, int, etc.)
            - button: Search save
            - textarea/output
        4. Dump
            - dropdown-like: save file to dump from
            - text input: offset to dump from
            - text input: length of data to dump
            - text input: name for new file


## Screenshots
![script compilation](https://cdn.discordapp.com/attachments/758286353439260733/841849300468498432/toolbox-compilation.png)
