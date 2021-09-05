import os
import re
import shutil
import socket
import struct
import sys
import threading
import time

import PySimpleGUI as sg

import PKSMScript as ps


############################################################
#  Misc Constants and Support Variables
############################################################

print_fmt = {
    "error": {
        "text_color": "yellow",
        "background_color": "red",
        "sep": "\n",
        # "end": "",
    },
    "warning": {
        "text_color": "black",
        "background_color": "yellow",
        # "end": "",
    },
    "success": {
        "text_color": "white",
        "background_color": "green",
        "end": "",
    },
}

validators = {
    "hex": "0x123456789abcdefABCDEF",
    "ip": "0.123456789",
    "digit": "0123456789",
}

save_types = (
    ("Pokemon save", "*.sav;*.dsv;main;*.main;savedata.bin"), ("ALL Files", "*.*"))

############################################################
#  GUI Creation Functions
############################################################


def add_save(window: sg.Window, active_inputs: int):
    window.extend_layout(window["-SAVE_LIST-"], [[
        sg.Column([[
            sg.Button("-", key=f"-SAVE_REMOVE_{active_inputs}-", size=(2, 1)),
            sg.Text(f"{active_inputs+1}."),
            sg.Input(key=f"-SAVE_FILE_{active_inputs}-"),
            sg.FileBrowse(file_types=save_types, target=f"-SAVE_FILE_{active_inputs}-"),
        ]], key=f"-SAVE_{active_inputs}-"),
    ]])


def add_script_input(window: sg.Window, active_inputs: int):
    window.extend_layout(window[("COMPILE", "GROUPS")], [[
        sg.Column([[
            sg.Button("-", size=(2, 1), key=("COMPILE", "REMOVE", active_inputs)),
            sg.Input(s=(10, 1), pad=(10, None), metadata="validate:hex",
                     key=("COMPILE", "OFFSET", active_inputs)),
            sg.Input(s=(10, 1), pad=(10, None), metadata="validate:hex",
                     key=("COMPILE", "LENGTH", active_inputs)),
            sg.Input(s=(10, 1), pad=(10, None), metadata="validate:hex",
                     key=("COMPILE", "REPEAT", active_inputs)),
            sg.Combo(("Value", "File"), default_value="Value", enable_events=True,
                     key=("COMPILE", "DATA_TYPE", active_inputs)),
            sg.Input(s=(30, 1), key=("COMPILE", "DATA", active_inputs), pad=(0, None)),
            sg.FileBrowse(disabled=True, key=("COMPILE", "FILE", active_inputs)),
        ]], key=("COMPILE", active_inputs)),
    ]])


def collapsible(layout, key, visible: bool):
    return sg.pin(sg.Column(layout, key=key, visible=visible))


############################################################
#  PKSM Communication Functions
############################################################


def send(address: tuple, data: bytes, abort: threading.Event, window: sg.Window, delay: int = 5, attempts: int = 5):
    for attempt in range(1, attempts + 1):
        # delay to let user interact with PKSM screens
        # ???: delay before each connection attempt or just the first?
        for _ in range(delay * 2):
            time.sleep(0.5)
            if abort.is_set():
                # shortcut out on user abort
                raise
        try:
            # Error handling test code
            # if len(data) > 4:
            #     raise ZeroDivisionError
            # window.write_event_value(("SEND", "WARNING"), "TODO: socket operation")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(address)
                s.sendall(data)
        except ConnectionRefusedError:
            window.write_event_value(("SEND", "PROGRESS"), attempt)
            if attempt < attempts:
                window.write_event_value(("SEND", "WARNING"), f"Send attempt {attempt} failed to connect. Retrying in {delay} seconds")
        except:
            # error while connected
            window.write_event_value(("SEND", "ERROR"), sys.exc_info())
            break
        else:
            # send succeeded
            return
    if attempt == attempts:
        window.write_event_value(("SEND", "ERROR"), (f"Failed to connect in {attempts} tries", ""))
        abort.set()
    raise


def send_thread(window: sg.Window, abort: threading.Event, file_name: str, ip: str, script_name: str = "", delay: int = 5, attempts: int = 5):
    address = (ip, 34567)
    window.write_event_value(("SEND", "STAGE"), "Preparing to send script to PKSM")
    name = file_name.encode()
    if script_name:
        name = script_name.encode()

    try:
        with open(file_name, "rb") as f:
            data = f.read()

        window.write_event_value(("SEND", "STAGE"), "Sending length of script name")
        send(address, struct.pack("i", len(name)), abort, window, delay, attempts)
        window.write_event_value(("SEND", "STAGE"), "Sending script name")
        send(address, name, abort, window, delay, attempts)
        window.write_event_value(("SEND", "STAGE"), "Sending size of file")
        send(address, struct.pack("i", len(data)), abort, window, delay, attempts)
        window.write_event_value(("SEND", "STAGE"), "Sending file contents")
        send(address, data, abort, window, delay, attempts)
        window.write_event_value(("SEND", "END"), ("Script sent successfully!\n", "success"))
    except OSError:
        window.write_event_value(("SEND", "ERROR"), f"An error occurred while reading '{file_name}'.\nSending failed")
        window.write_event_value(("SEND", "END"), ("Sending failed", "error"))
    except:
        if abort.is_set():
            # shortcut out if user aborted sending or
            # connection attempts failed enough times
            window.write_event_value(("SEND", "END"), ("Sending was aborted", "warning"))
        else:
            # other socket related error
            err = ["Sending encountered an error", *sys.exc_info()]
            window.write_event_value(("SEND", "ERROR"), err)
            window.write_event_value(("SEND", "END"), ("Sending failed", "error"))


############################################################
#  Event Handling Functions
############################################################


def send_event(event, values, window: sg.Window, abort: threading.Event, msg: str) -> str:
    out = window[("SEND", "FEEDBACK", sg.WRITE_ONLY_KEY)]
    attempts = int(values[("SEND", "ATTEMPTS")])

    # starting and stopping send
    if event[1] == "START":
        if os.path.isfile(values[("SEND", "FILE")]):
            send_name = values[("SEND", "NAME")]
            if not send_name or "/" in send_name or "\\" in send_name:
                # PKSM's script-receiver.c does not support nonexistant subdirectories
                send_name = os.path.basename(values[("SEND", "FILE")])
            window[("SEND", "HEADER")].update(f"Sending '{os.path.basename(values[('SEND', 'FILE')])}' as '{send_name}'")
            threading.Thread(target=send_thread, kwargs={
                "window": window,
                "abort": abort,
                "file_name": values[("SEND", "FILE")],
                "ip": values[("SEND", "IP")],
                "script_name": send_name,
                "delay": int(values[("SEND", "DELAY")]),
                "attempts": attempts,
            }, daemon=True).start()
            window[("SEND", "ABORT")].update(disabled=False)
            window[("SEND", "PROGRESS", "TEXT")].update(f"{attempts} / {attempts}")
            window[("SEND", "PROGRESS", "BAR")].update(attempts, max=attempts)
            return "Preparing to send script to PKSM"
        out.print(f"'{values[('SEND', 'FILE')]}' does not exist or is not a file")
    elif event[1] == "ABORT":
        abort.set()
    elif event[1] == "END":
        out.print(values[event][0], **print_fmt[values[event][1]])
        out.print("")
        file_name = os.path.basename(values[("SEND", "FILE")])
        send_name = values[("SEND", "NAME")]
        if not send_name or "/" in send_name or "\\" in send_name:
            # PKSM's script-receiver.c does not support nonexistant subdirectories
            send_name = file_name
        if abort.is_set():
            window[("SEND", "HEADER")].update(f"Failed to send '{file_name}' to PKSM")
        else:
            window[("SEND", "HEADER")].update(f"Sent '{file_name}' as '{send_name}'")
        window[("SEND", "ACTIVITY")].update(values[event][0])
        window[("SEND", "PROGRESS", "TEXT")].update("- / -")
        window[("SEND", "PROGRESS", "BAR")].update(0)
        window[("SEND", "ABORT")].update(disabled=True)
        abort.clear()
        return ""
    # Send progress
    elif event[1] == "STAGE":
        window[("SEND", "ACTIVITY")].update(values[event])
        out.print(values[event])
        return values[event]
    elif event[1] == "PROGRESS":
        window[("SEND", "PROGRESS", "TEXT")].update(f"{attempts - values[('SEND', 'PROGRESS')]} / {attempts}")
        window[("SEND", "PROGRESS", "BAR")].update(attempts - values[("SEND", "PROGRESS")])
    elif event[1] == "WARNING":
        out.print(values[event], **print_fmt["warning"])
    # Toggle visibility of delay and attempts controls
    elif event[1] == "TOGGLE":
        window[("SEND", event[2])].update(visible=values[event])
    # Debug and Error printing
    elif event[1] == "ERROR":
        out.print(*values[event], **print_fmt["error"])
    elif event[1] == "DEBUG":
        print(f"{event}: {values[event]}")
    return msg


def compile_event(event, values, window: sg.Window, inputs: int, active: int) -> tuple:
    if event[1] == "ADD":
        if inputs > active:
            window[("COMPILE", "OFFSET", active)].unhide_row()
        else:
            add_script_input(window, active)
            inputs += 1
        window[("COMPILE", "OFFSET", active)].set_focus()
        active += 1
        window[("COMPILE", "REMOVE", 0)].update(disabled=False)
    elif event[1] == "REMOVE":
        input_id = event[2]
        if input_id < active - 1:
            for i in range(input_id, active - 1):
                for s in ("OFFSET", "LENGTH", "REPEAT", "DATA_TYPE", "DATA"):
                    window[("COMPILE", s, i)].update(value=values[("COMPILE", s, i+1)])
                    window[("COMPILE", s, i+1)].update(value="Value" if s == "DATA_TYPE" else "")
                window[("COMPILE", "FILE", i)].update(disabled=values[("COMPILE", "DATA_TYPE", i+1)] != "File")
        for s in ("OFFSET", "LENGTH", "REPEAT", "DATA_TYPE", "DATA"):
            window[("COMPILE", s, input_id)].update(value="Value" if s == "DATA_TYPE" else "")
        window[("COMPILE", "FILE", input_id)].update(disabled=values[("COMPILE", "DATA_TYPE", input_id)] != "File")
        window[("COMPILE", "OFFSET", active-1)].hide_row()
        active -= 1
        if active == 1:
            window[("COMPILE", "REMOVE", 0)].update(disabled=True)
    elif event[1] == "DATE_TYPE":
        input_id = event[2]
        window[("COMPILE", "FILE", input_id)].update(disabled=values[("COMPILE", "DATA_TYPE", input_id)] != "FILE")
    elif event[1] == "START":
        out = window[("COMPILE", "OUTPUT", sg.WRITE_ONLY_KEY)]
        compile_args = []
        file_name = values[("COMPILE", "NAME")]
        if file_name[-5:] == ".pksm":
            file_name = file_name[:-5]
        compile_args.append(file_name)
        file_name = compiled_name = f"{file_name}.pksm"
        subdir = values[("COMPILE", "SUBDIR")]
        if subdir:
            compile_args.extend(["-d", subdir])
            file_name = os.path.join(subdir, file_name)
            compiled_name = os.path.join("build", file_name)

        # gather and validate compilation args
        out.print("\nGathering script input...")
        compile_arg_types = ("OFFSET", "LENGTH", "DATA", "REPEAT")
        warnings = []
        for i in range(active):
            group = [values[("COMPILE", itm, i)] for itm in compile_arg_types]
            new_warns = False
            for t in ("OFFSET", "LENGTH", "REPEAT"):
                try:
                    # catch invalid input before it gets passed to compilation
                    int(values[("COMPILE", t, i)], 0)
                except ValueError:
                    new_warns = True
                    warnings.append(f"  Input group {i+1}'s {t} is not a valid value")
            if values[("COMPILE", "DATA_TYPE", i)] == "File":
                # confirm file exists
                if not os.path.isfile(group[2]):
                    new_warns = True
                    warnings.append(f"  Input file {i+1} does not exist or is not a file")
            elif values[("COMPILE", "DATA_TYPE", i)] == "Value":
                try:
                    int(group[2], 0)
                except ValueError:
                    new_warns = True
                    warnings.append(f"  Input group {i+1}'s DATA is not a valid value")
            else:
                new_warns = True
                warnings.append(f"  Input group {i+1}'s DATA_TYPE is not a recognized value")
            if not new_warns:
                compile_args.extend(["-i", *group])

        if warnings:
            out.print("WARNING(s):", **print_fmt["warning"])
            for warn in warnings:
                out.print(warn)

        # compile result
        if len(compile_args) > 3:
            script_args = ps.parser.parse_args(compile_args)
            ps.main(script_args)
            out.print("SUCCESS:", **print_fmt["success"])
            out.print(" Script compiled successfully!")
            dest = values[("COMPILE", "DEST")]
            if dest or subdir:
                os.makedirs(os.path.join(dest, subdir), exist_ok=True)
                shutil.move(compiled_name, os.path.join(dest, file_name))
                out.print(f"Script saved to '{os.path.join(dest, file_name)}'")
                # TODO: provide PKSMScript compile command
        else:
            out.print("ERROR:", **print_fmt["error"])
            out.print(" No suitable inputs were found. Script failed to compile")

    return inputs, active


def main():
    save_inputs = 1
    save_inputs_active = 1
    script_inputs = 1
    script_inputs_active = 1

    RE_IP = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$"
    sending = ""
    abort = threading.Event()

    sg.theme("DarkAmber")

    # Layouts
    file_list_column = [
        [sg.Text("TODO: Save file selection GUI")],
        [sg.Button("Add save file", key="-ADD_SAVE-")],
        [
            sg.Column([[
                sg.Column([[
                    sg.Button("-", disabled=True, key="-SAVE_REMOVE_0-", size=(2, 1)),
                    sg.Text("1."),
                    sg.Input(key="-SAVE_FILE_0-"),
                    sg.FileBrowse(file_types=save_types, target=f"-SAVE_FILE_0-"),
                ]], key="-SAVE_0-"),
            ]], k="-SAVE_LIST-"),
        ],
    ]

    save_diff_raw_layout = [
        [sg.Text("TODO: Save file raw diff GUI")],
    ]

    save_diff_event_layout = [
        [sg.Text("TODO: Save file event diff GUI")],
    ]

    save_search_layout = [
        [sg.Text("TODO: Save search GUI")],
    ]

    save_dump_layout = [
        [sg.Text("TODO: Save dump GUI")],
    ]

    research_layout = [[
        sg.Column(layout=file_list_column, vertical_alignment="top"),
        sg.Column([[sg.TabGroup([[
            sg.Tab("Raw Diff", layout=save_diff_raw_layout),
            sg.Tab("Event Diff", layout=save_diff_event_layout),
            sg.Tab("Search", layout=save_search_layout),
            sg.Tab("Dump", layout=save_dump_layout),
        ]])]], vertical_alignment="top"),
    ]]

    compile_layout = [
        [
            sg.Column([
                [
                    sg.Column([[
                        sg.Text("Scripts folder:"),
                        sg.Input(k=("COMPILE", "DEST")),
                        sg.FolderBrowse(target=(sg.ThisRow, -1)),
                    ]]),
                ],
                [sg.Column([
                    [sg.Button("Compile Script", key=("COMPILE", "START"),
                               disabled=True)]
                ], justification="center")],
                [sg.HorizontalSeparator()],
                [
                    sg.Column([
                        [sg.Text("Script name:", pad=(0, 5))],
                        [sg.Text("Subdirectory (optional):", pad=(0, 5))],
                    ], element_justification="right"),
                    sg.Column([
                        [sg.Input(k=("COMPILE", "NAME"), pad=(0, 5))],
                        [sg.Input(k=("COMPILE", "SUBDIR"), pad=(0, 5))],
                    ]),
                ],
            ]),
            sg.Column([
                [sg.Multiline(size=(50, 10), autoscroll=True, write_only=True,
                              key=("COMPILE", "OUTPUT", sg.WRITE_ONLY_KEY), disabled=True,
                              background_color=sg.theme_input_background_color(),
                              pad=(5, 5), border_width=0)],
            ]),
        ],
        [sg.Frame("Input Groups", [
            [
                sg.Column([[
                    sg.Button("Add", size=(3, 1), key=("COMPILE", "ADD")),
                    sg.Text("Offset", s=(10, 1)),
                    sg.Text("Data Length", s=(10, 1)),
                    sg.Text("Data Repeat", s=(10, 1)),
                    sg.Text("Data", pad=(50, None)),
                ]]),
            ],
            [
                sg.Column([[
                    sg.Button("-", size=(2, 1),
                              key=("COMPILE", "REMOVE", 0), disabled=True),
                    sg.Input(s=(10, 1), pad=(10, None), key=("COMPILE", "OFFSET", 0), metadata="validate:hex"),
                    sg.Input(s=(10, 1), pad=(10, None), key=("COMPILE", "LENGTH", 0), metadata="validate:hex"),
                    sg.Input(s=(10, 1), pad=(10, None), key=("COMPILE", "REPEAT", 0), metadata="validate:hex"),
                    sg.Combo(("Value", "File"), default_value="Value",
                             enable_events=True, key=("COMPILE", "DATA_TYPE", 0)),
                    sg.Input(s=(30, 1), key=("COMPILE", "DATA", 0), pad=(0, None)),
                    sg.FileBrowse(disabled=True, key=("COMPILE", "FILE", 0)),
                ]], key=("COMPILE", 0)),
            ],
        ], key=("COMPILE", "GROUPS"), pad=(20, 10))],
    ]

    send_config_layout = [
        [
            sg.Column([
                [sg.Text("Delay (in seconds):")],
                [sg.Text("Number of Attempts:")],
            ], element_justification="right"),
            sg.Column([
                [sg.Input("5", key=("SEND", "DELAY"), size=(5, 1), justification="right", metadata="validate:digit")],
                [sg.Input("5", key=("SEND", "ATTEMPTS"), size=(5, 1), justification="right", metadata="validate:digit")],
            ], element_justification="left"),
        ],
    ]
    send_layout = [
        [
            sg.Column([
                [
                    sg.Column([
                        [sg.Text("File to send:", pad=((5, 0), 5))],
                        # [sg.Text("Subdirectory (optional):", pad=((5, 0), 5))],
                        [sg.Text("Script name (optional):", pad=((5, 0), 5))],
                        [sg.Text("3DS IP Address:", pad=((5, 0), 5))],
                    ], pad=(0, 5), element_justification="right", vertical_alignment="top"),
                    sg.Column([
                        [sg.Input(k=("SEND", "FILE")), sg.FileBrowse(file_types=(
                            ("PKSM Scripts", "*.pksm;*.c"),), target=(sg.ThisRow, -1))],
                        # [sg.Input(k=("SEND", "SUBDIR"), disabled=True)],
                        [sg.Input(key=("SEND", "NAME"))],
                        [sg.Input(size=(15, 1), k=("SEND", "IP"),
                                metadata="validate:ip")],
                    ], pad=((0, 5), 5), vertical_alignment="top"),
                ],
                [sg.Column([[
                    sg.Button("Send to PKSM", key=("SEND", "START"), disabled=True),
                    sg.Button("Abort", key=("SEND", "ABORT"), disabled=True),
                ]], justification="center")],
                [sg.HorizontalSeparator()],
                [sg.Checkbox("Advanced socket configuration", key=("SEND", "TOGGLE", "CONFIG"), enable_events=True)],
                [collapsible(send_config_layout, key=("SEND", "CONFIG"), visible=False)],
            ], vertical_alignment="top"),
            sg.Column([
                [
                    sg.Text(" ", size=(35, 1), key=("SEND", "HEADER"), font=("_", 15, "bold")),
                ],
                [
                    sg.Text("Remaining Attempts:"),
                    sg.Text("- / -", key=("SEND", "PROGRESS", "TEXT"), size=(5, 1), justification="center"),
                    sg.ProgressBar(5, "horizontal", key=(
                        "SEND", "PROGRESS", "BAR"), size=(18, 15)),
                ],
                [
                    sg.Input("--", key=("SEND", "ACTIVITY"), disabled=True,
                            size=(50, 1), border_width=0,
                            disabled_readonly_background_color=sg.theme_background_color(),
                            disabled_readonly_text_color=sg.theme_text_color())
                ],
                [sg.Checkbox("Show log", key=("SEND", "TOGGLE", "LOG"), enable_events=True)],
                [
                    collapsible([[
                        sg.Multiline(key=("SEND", "FEEDBACK", sg.WRITE_ONLY_KEY),
                                write_only=True, auto_refresh=True, size=(50, 10),
                                disabled=True, autoscroll=True),
                    ]], key=("SEND", "LOG"), visible=False),
                ],
            ], vertical_alignment="top"),
        ],
    ]

    layout = [[
        sg.TabGroup([[
            sg.Tab("Send to PKSM", layout=send_layout),
            sg.Tab("Compile Script", layout=compile_layout),
            # sg.Tab("Save Research", layout=research_layout),
        ]]),
    ]]

    window = sg.Window("PKSM-Scripts Toolbox", layout=layout, finalize=True,
                       resizable=True, return_keyboard_events=True)

    # Event Loop
    while True:
        event, values = window.read(timeout=500)

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        try:
            focused = window.find_element_with_focus()
        except KeyError as e:
            # ComboBox dropdown doesn't like find_element_with_focus
            # print("KeyError:", e)
            focused = None
        if event != sg.TIMEOUT_EVENT and event[0] not in ("SEND", ""):
            # development logging
            print(event, values)
            if focused:
                print(f"Focused element: {focused.Key}")

        # Input validation
        if focused and focused.metadata:
            if event != sg.TIMEOUT_EVENT:
                print(f"Element.metadata: {focused.metadata}")
            func, validator = focused.metadata.split(":")
            if func == "validate":
                legal = validators[validator]
                for i, v in enumerate(values[focused.Key]):
                    if v not in legal:
                        window[focused.Key].update(values[focused.Key][:i])
                        break

        if event == "\r":
            if focused and focused.Type == sg.ELEM_TYPE_BUTTON:
                focused.click()
        elif event[0] == "SEND":
            sending = send_event(event, values, window=window, abort=abort, msg=sending)
        elif event[0] == "COMPILE":
            script_inputs, script_inputs_active = compile_event(event, values, window, inputs=script_inputs, active=script_inputs_active)
        # TODO: refactor: convert keys to tuples
        elif event == "-ADD_SAVE-":
            if save_inputs > save_inputs_active:
                window[f"-SAVE_FILE_{save_inputs_active}-"].unhide_row()
            else:
                add_save(window, save_inputs_active)
                save_inputs += 1
            window[f"-SAVE_FILE_{save_inputs_active}-"].set_focus()
            save_inputs_active += 1
            window["-SAVE_REMOVE_0-"].update(disabled=False)
        elif event.startswith("-SAVE_REMOVE_"):
            # get ID of save being removed
            save_id = int(event[13:-1])
            # bubble up saves if ID not last
            if save_id < save_inputs_active - 1:
                for i in range(save_id, save_inputs_active-1):
                    window[f"-SAVE_FILE_{i}-"].update(values[f"-SAVE_FILE_{i+1}-"])
            window[f"-SAVE_FILE_{save_inputs_active-1}-"].update(value="")
            # cannot remove elements from GUI, so hide it
            window[f"-SAVE_FILE_{save_inputs_active-1}-"].hide_row()
            save_inputs_active -= 1
            if save_inputs_active == 1:
                window["-SAVE_REMOVE_0-"].update(disabled=True)

        # Conditional widget state manipulation
        if sending != "":
            if sending[-3:] == "...":
                sending = sending[:-3]
            else:
                sending = f"{sending}."
            window[("SEND", "ACTIVITY")].update(sending)
        if values[("SEND", "FILE")] and re.match(RE_IP, values[("SEND", "IP")]) and sending == "":
            window[("SEND", "START")].update(disabled=False)
        else:
            window[("SEND", "START")].update(disabled=True)
        if values[("COMPILE", "NAME")]:
            window[("COMPILE", "START")].update(disabled=False)
        else:
            window[("COMPILE", "START")].update(disabled=True)

    window.close()


if __name__ == "__main__":
    main()
