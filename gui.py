import os
import shutil

import PySimpleGUI as sg

import PKSMScript as ps


########################
# Support
########################

print_fmt = {
    "error": {
        "text_color": "yellow",
        "background_color": "red",
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
}

########################
# Layout
########################

sg.theme("DarkAmber")

save_types = (
    ("Pokemon save", "*.sav;*.dsv;main;*.main;savedata.bin"), ("ALL Files", "*.*"))
save_inputs = 1
save_inputs_active = 1
script_inputs = 1
script_inputs_active = 1


def add_save():
    window.extend_layout(window["-SAVE_LIST-"], [[
        sg.Column([[
            sg.Button(
                "-", key=f"-SAVE_REMOVE_{save_inputs_active}-", size=(2, 1)),
            sg.Text(f"{save_inputs_active+1}."),
            sg.Input(key=f"-SAVE_FILE_{save_inputs_active}-"),
            sg.FileBrowse(file_types=save_types,
                          target=f"-SAVE_FILE_{save_inputs_active}-"),
        ]], key=f"-SAVE_{save_inputs_active}-"),
    ]])


def add_script_input():
    window.extend_layout(window["-COMPILE_GROUPS-"], [[
        sg.Column([[
            sg.Button("-", size=(2, 1),
                      key=f"-COMPILE_REMOVE_{script_inputs_active}-"),
            sg.Input(s=(10, 1), pad=(10, None), metadata="validate:hex",
                     key=f"-COMPILE_OFFSET_{script_inputs_active}-"),
            sg.Input(s=(10, 1), pad=(10, None), metadata="validate:hex",
                     key=f"-COMPILE_LENGTH_{script_inputs_active}-"),
            sg.Input(s=(10, 1), pad=(10, None), metadata="validate:hex",
                     key=f"-COMPILE_REPEAT_{script_inputs_active}-"),
            sg.Combo(("Value", "File"), default_value="Value", enable_events=True,
                     key=f"-COMPILE_DATA_TYPE_{script_inputs_active}-"),
            sg.Input(
                s=(30, 1), key=f"-COMPILE_DATA_{script_inputs_active}-", pad=(0, None)),
            sg.FileBrowse(
                disabled=True, key=f"-COMPILE_FILE_{script_inputs_active}-"),
        ]], key=f"-COMPILE_{script_inputs_active}-"),
    ]])


file_list_column = [
    [sg.Text("TODO: Save file selection GUI")],
    [sg.Button("Add save file", key="-ADD_SAVE-")],
    [
        sg.Column([[
            sg.Column([[
                sg.Button("-", disabled=True,
                          key="-SAVE_REMOVE_0-", size=(2, 1)),
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
    # TODO: information output element (not necessarily a sg.Output)
    [sg.Text("TODO: Simple script creation and compilation GUI")],
    [
        sg.Column([
            [
                sg.Column([[
                    sg.Text("Scripts folder:"),
                    sg.Input(k="-COMPILE_DEST-"),
                    sg.FolderBrowse(target="-COMPILE_DEST-"),
                ]]),
            ],
            [sg.Column([
                [sg.Button("Compile Script", key="-COMPILE_START-",
                           disabled=True)]
            ], justification="center")],
            [sg.HorizontalSeparator()],
            [
                sg.Column([
                    [sg.Text("Script name:", pad=(0, 5))],
                    [sg.Text("Subdirectory (optional):", pad=(0, 5))],
                ], element_justification="right"),
                sg.Column([
                    [sg.Input(k="-COMPILE_NAME-", pad=(0, 5))],
                    [sg.Input(k="-COMPILE_SUBDIR-", pad=(0, 5))],
                ]),
            ],
        ]),
        sg.Column([
            [sg.Multiline(size=(50, 10), autoscroll=True, write_only=True,
                          key=f"-COMPILE_OUTPUT_{sg.WRITE_ONLY_KEY}", disabled=True,
                          background_color="#333333", pad=(5, 5), border_width=0)],
        ]),
    ],
    [sg.Frame("Input Groups", [
        [
            sg.Column([[
                sg.Button("Add", size=(3, 1), key="-COMPILE_ADD-"),
                sg.Text("Offset", s=(10, 1)),
                sg.Text("Data Length", s=(10, 1)),
                sg.Text("Data Repeat", s=(10, 1)),
                sg.Text("Data", pad=(50, None)),
            ]]),
        ],
        [
            sg.Column([[
                sg.Button("-", size=(2, 1),
                          key="-COMPILE_REMOVE_0-", disabled=True),
                sg.Input(s=(10, 1), pad=(10, None), key="-COMPILE_OFFSET_0-", metadata="validate:hex"),
                sg.Input(s=(10, 1), pad=(10, None), key="-COMPILE_LENGTH_0-", metadata="validate:hex"),
                sg.Input(s=(10, 1), pad=(10, None), key="-COMPILE_REPEAT_0-", metadata="validate:hex"),
                sg.Combo(("Value", "File"), default_value="Value",
                         enable_events=True, key="-COMPILE_DATA_TYPE_0-"),
                sg.Input(s=(30, 1), key="-COMPILE_DATA_0-", pad=(0, None)),
                sg.FileBrowse(disabled=True, key="-COMPILE_FILE_0-"),
            ]], key="-COMPILE_0-"),
        ],
    ], key="-COMPILE_GROUPS-", pad=(20, 10))],
]

send_layout = [
    [sg.Text("TODO: PKSM communication GUI")],
    [
        sg.Column([
            [sg.Text("Script to send:", pad=((5, 0), 5))],
            [sg.Text("Subdirectory (optional):", pad=((5, 0), 5))],
            [sg.Text("Change script name? (optional)", pad=((5, 0), 5))],
            [sg.Text("3DS IP Address:", pad=((5, 0), 5))],
        ], pad=(0, 5), element_justification="right"),
        sg.Column([
            [sg.Input(k="-SEND_FILE-", pad=((0, 5), 5)), sg.FileBrowse(file_types=(
                ("PKSM Scripts", "*.pksm;*.c"),), target="-SEND_FILE-", pad=(0, 5))],
            [sg.Input(k="-SEND_SUBDIR-", pad=(0, 5))],
            [sg.Checkbox("", key="-SEND_CHANGE-", enable_events=True), sg.Column(
                [[sg.Input(key="-SEND_NAME-")]], key="-CHANGE_NAME-", visible=False, pad=(0, 0))],
            [sg.Input(size=(15, 1), k="-SEND_IP-", pad=(0, 5), metadata="validate:ip")],
        ], pad=((0, 5), 5)),
    ],
    [sg.Column([[sg.Button("Send to PKSM", key="-SEND_START-",
               disabled=True)]], justification="center")],
]

layout = [[
    sg.TabGroup([[
        sg.Tab("Save Research", layout=research_layout),
        sg.Tab("Send to PKSM", layout=send_layout),
        sg.Tab("Compile Script", layout=compile_layout),
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
    if event != sg.TIMEOUT_EVENT:
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
    elif event == "-ADD_SAVE-":
        if save_inputs > save_inputs_active:
            window[f"-SAVE_FILE_{save_inputs_active}-"].unhide_row()
        else:
            add_save()
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
    elif event == "-COMPILE_ADD-":
        if script_inputs > script_inputs_active:
            window[f"-COMPILE_OFFSET_{script_inputs_active}-"].unhide_row()
        else:
            add_script_input()
            script_inputs += 1
        window[f"-COMPILE_OFFSET_{script_inputs_active}-"].set_focus()
        script_inputs_active += 1
        window["-COMPILE_REMOVE_0-"].update(disabled=False)
    elif event.startswith("-COMPILE_REMOVE_"):
        input_id = int(event[16:-1])
        if input_id < script_inputs_active - 1:
            for i in range(input_id, script_inputs_active - 1):
                for s in ("OFFSET", "LENGTH", "DATA_TYPE", "DATA"):
                    window[f"-COMPILE_{s}_{i}-"].update(
                        value=values[f"-COMPILE_{s}_{i+1}-"])
                    window[f"-COMPILE_{s}_{i+1}-"].update(
                        value="Value" if s == "DATA_TYPE" else "")
                window[f"-COMPILE_FILE_{i}-"].update(
                    disabled=values[f"-COMPILE_DATA_TYPE_{i+1}-"] != "File")
        window[f"-COMPILE_OFFSET_{script_inputs_active-1}-"].hide_row()
        script_inputs_active -= 1
        if script_inputs_active == 1:
            window["-COMPILE_REMOVE_0-"].update(disabled=True)
    elif event.startswith("-COMPILE_DATA_TYPE_"):
        input_id = int(event[19:-1])
        window[f"-COMPILE_FILE_{input_id}-"].update(
            disabled=values[f"-COMPILE_DATA_TYPE_{input_id}-"] != "File")
    elif event == "-SEND_CHANGE-":
        window["-CHANGE_NAME-"].update(visible=values["-SEND_CHANGE-"])
        if values["-SEND_CHANGE-"]:
            window["-SEND_NAME-"].set_focus()
    elif event == "-COMPILE_START-":
        out = window[f"-COMPILE_OUTPUT_{sg.WRITE_ONLY_KEY}"]
        compile_args = []
        file_name = values["-COMPILE_NAME-"]
        if file_name[-5:] == ".pksm":
            file_name = file_name[:-5]
        compile_args.append(file_name)
        file_name = compiled_name = f"{file_name}.pksm"
        subdir = values["-COMPILE_SUBDIR-"]
        if subdir:
            compile_args.extend(["-d", subdir])
            file_name = os.path.join(subdir, file_name)
            compiled_name = os.path.join("build", file_name)

        # gather and validate compilation args
        out.print("\nGathering script input...")
        complete_groups = 0
        compile_arg_types = ("OFFSET", "LENGTH", "DATA", "REPEAT")
        warnings = []
        for i in range(script_inputs_active):
            group = [values[f"-COMPILE_{itm}_{i}-"]
                     for itm in compile_arg_types]
            new_warns = False
            for t in ("OFFSET", "LENGTH", "REPEAT"):
                try:
                    # catch invalid input before it gets passed to compilation
                    int(values[f"-COMPILE_{t}_{i}-"], 0)
                except ValueError:
                    new_warns = True
                    warnings.append(f"  Input group {i+1}'s {t} is not a valid value")
            if values[f"-COMPILE_DATA_TYPE_{i}-"] == "File":
                # confirm file exists
                if not os.path.exists(group[2]) or not os.path.isfile(group[2]):
                    new_warns = True
                    warnings.append(f"  Input file {i+1} does not exist or is not a file")
            elif values[f"-COMPILE_DATA_TYPE_{i}-"] == "Value":
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
            dest = values["-COMPILE_DEST-"]
            if dest or subdir:
                os.makedirs(os.path.join(dest, subdir), exist_ok=True)
                shutil.move(compiled_name, os.path.join(dest, file_name))
                # TODO: print location of new file
                out.print(f"Script saved to '{os.path.join(dest, file_name)}'")
        else:
            out.print("ERROR:", **print_fmt["error"])
            out.print(" No suitable inputs were found. Script failed to compile")

    # Conditional button enable/disable
    if values["-SEND_FILE-"] and values["-SEND_IP-"]:
        window["-SEND_START-"].update(disabled=False)
    else:
        window["-SEND_START-"].update(disabled=True)
    if values["-COMPILE_NAME-"]:
        window["-COMPILE_START-"].update(disabled=False)
    else:
        window["-COMPILE_START-"].update(disabled=True)

window.close()
