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
        - [x] feedback
            - [x] `Sending '{file_name}' as '{script_name}'`
            - [x] send stages
                - [x] Name length
                - [x] Name
                - [x] File size
                - [x] File contents
                - [x] Completion (success or fail)
                - [ ] Failure reason
            - [x] stage attempt countdown (progress bar)
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
    - [x] script sending
        - [x] file selection
        - [x] IP input with validation
        - [x] alternate script name
        - [x] send script
            - [x] verify file
            - [x] catch errors
            - [x] threading (so GUI remains responsive during send process)
                - [x] work through send operations
                - [x] allow user to abort
                - [x] cancel out on user abort
            - [x] send data via `socket`
            - [x] feedback
                - [x] attempts countdown
                - [x] send stage
                - [x] send success / failure
                - [ ] send failure reason


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
            - button: Export Diff (like [current CLI diff script](https://github.com/FlagBrew/PKSM-Scripts/blob/e37719fd8d6a1ecc3b18c5838dedd7bc6d251ad0/dev/python/diff.py))
        2. Event Diff
            - table-like: differences in Event Flags and Constants of sets of save data
            - button: Export Diff (like current CLI diff script)
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
- Focus-based contextual help
    - implementation
        - include some kind of a textual element (Text, Multiline, etc.) to display Help text
        - check element with focus
        - change out content of Help text based on focused element
    - alternative(s)
        - second window containing the Help text element
- Research + Compilation integration
    - envisioned process
        1. click offset in Research
        2. switch to Compile tab
        3. fill an empty row with offset
            1. if offset has known length, fill row's length input too
        4. focus row's next empty input ("Data Length" or "Data Repeat")
- Work sharing
    - button to trigger building of a shareable `.zip` of work (to be posted in Discord or a PKSM-Scripts issue)
    - `.zip` contains any of the following applicable files:
        - `/data/**/*` -- any data files used in creating large `.pksm` scripts
        - `/src/scripts*.txt` -- command string(s) to be passed to `PKSMScript.py` to generate `.pksm` scripts
        - `/docs/**/*.json` -- offset documentation JSON files; additional requirements
            - Research + Compilation integration
            - script uses previously undefined offset(s)
            - user-defined meaning(s) for offset(s) used


## Screenshots
![script compilation](https://cdn.discordapp.com/attachments/576085115910881282/883826635319681054/toolbox-compilation.png)
![script sending](https://cdn.discordapp.com/attachments/758286353439260733/883571768898498581/toolbox-sending.png)
