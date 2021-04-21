import PySimpleGUI as sg


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
            sg.Input(s=(10, 1), pad=(10, None),
                     key=f"-COMPILE_OFFSET_{script_inputs_active}-"),
            sg.Input(s=(10, 1), pad=(10, None),
                     key=f"-COMPILE_LENGTH_{script_inputs_active}-"),
            sg.Input(s=(10, 1), pad=(10, None),
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
    [sg.Text("TODO: Simple script creation and compilation GUI")],
    [
        sg.Column([
            [sg.Text("Script name:")],
            [sg.Text("Subdirectory (optional):")],
        ], element_justification="right"),
        sg.Column([
            [sg.Input(k="-COMPILE_NAME-")],
            [sg.Input(k="-COMPILE_SUBDIR-")],
        ]),
    ],
    [sg.Column([[
        sg.Button("Add Input Group", key="-COMPILE_ADD-"),
        sg.Button("Compile Script", key="-COMPILE_START-"),
    ]], justification="center")],
    [sg.Frame("Input Groups", [
        [
            sg.Column([[
                sg.Text("", size=(3, 1)),
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
                sg.Input(s=(10, 1), pad=(10, None), key="-COMPILE_OFFSET_0-"),
                sg.Input(s=(10, 1), pad=(10, None), key="-COMPILE_LENGTH_0-"),
                sg.Input(s=(10, 1), pad=(10, None), key="-COMPILE_REPEAT_0-"),
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
            [sg.Input(size=(15, 1), k="-SEND_IP-", pad=(0, 5))],
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

window = sg.Window("PKSM-Scripts Toolbox",
                   layout=layout, resizable=True, finalize=True)

while True:
    event, values = window.read(timeout=500)

    if event in (sg.WIN_CLOSED, "Exit"):
        break

    if event == "-ADD_SAVE-":
        if save_inputs > save_inputs_active:
            window[f"-SAVE_{save_inputs_active}-"].update(visible=True)
        else:
            add_save()
            save_inputs += 1
        save_inputs_active += 1
        window["-SAVE_REMOVE_0-"].update(disabled=False)
    elif event.startswith("-SAVE_REMOVE_"):
        # get ID of save being removed
        save_id = int(event[13:-1])
        # bubble up saves if ID not last
        if save_id < save_inputs_active - 1:
            for i in range(save_id, save_inputs_active-1):
                window[f"-SAVE_FILE_{i}-"].update(
                    value=values[f"-SAVE_FILE_{i+1}-"])
        window[f"-SAVE_FILE_{save_inputs_active-1}-"].update(value="")
        # cannot remove elements from GUI, so hide it
        window[f"-SAVE_{save_inputs_active-1}-"].update(visible=False)
        save_inputs_active -= 1
        if save_inputs_active == 1:
            window["-SAVE_REMOVE_0-"].update(disabled=True)
    elif event == "-COMPILE_ADD-":
        if script_inputs > script_inputs_active:
            window[f"-COMPILE_{script_inputs_active}-"].update(visible=True)
        else:
            add_script_input()
            script_inputs += 1
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
        window[f"-COMPILE_{script_inputs_active-1}-"].update(visible=False)
        script_inputs_active -= 1
        if script_inputs_active == 1:
            window["-COMPILE_REMOVE_0-"].update(disabled=True)
    elif event.startswith("-COMPILE_DATA_TYPE_"):
        input_id = int(event[19:-1])
        window[f"-COMPILE_FILE_{input_id}-"].update(
            disabled=values[f"-COMPILE_DATA_TYPE_{input_id}-"] != "File")
    elif event == "-SEND_CHANGE-":
        window["-CHANGE_NAME-"].update(visible=values["-SEND_CHANGE-"])

    if not (values["-SEND_FILE-"]
            and values["-SEND_IP-"]):
        window["-SEND_START-"].update(disabled=True)
    else:
        window["-SEND_START-"].update(disabled=False)

window.close()
