import PySimpleGUI as sg


########################
# Layout
########################

sg.theme("DarkAmber")

save_types = (
    ("Pokemon save", "*.sav;*.dsv;main;*.main;savedata.bin"), ("ALL Files", "*.*"))
saves_active = 1
save_files_inputs = 1


def add_save():
    window.extend_layout(window["-SAVE_LIST-"], [[
        sg.Column([[
            sg.Button("-", key=f"-SAVE_REMOVE_{saves_active}-", size=(2, 1)),
            sg.Text(f"{saves_active+1}."),
            sg.Input(key=f"-SAVE_FILE_{saves_active}-"),
            sg.FileBrowse(file_types=save_types,
                          target=f"-SAVE_FILE_{saves_active}-"),
        ]], key=f"-SAVE_{saves_active}-"),
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

window = sg.Window("PKSM-Scripts Development Tool",
                   layout=layout, resizable=True, finalize=True)

while True:
    event, values = window.read(timeout=500)

    if event in (sg.WIN_CLOSED, "Exit"):
        break

    if event == "-ADD_SAVE-":
        if save_files_inputs > saves_active:
            window[f"-SAVE_{saves_active}-"].update(visible=True)
        else:
            add_save()
            save_files_inputs += 1
        saves_active += 1
    elif event.startswith("-SAVE_REMOVE_"):
        # get ID of save being removed
        save_id = int(event[13:-1])
        # bubble up saves if ID not last
        if save_id < saves_active - 1:
            for i in range(save_id, saves_active-1):
                window[f"-SAVE_FILE_{i}-"].update(
                    value=values[f"-SAVE_FILE_{i+1}-"])
                window[f"-SAVE_FILE_{i+1}-"].update(value="")
        window[f"-SAVE_FILE_{saves_active-1}-"].update(value="")
        # cannot remove elements from GUI, so hide it
        window[f"-SAVE_{saves_active-1}-"].update(visible=False)
        saves_active -= 1
    elif event == "-SEND_CHANGE-":
        window["-CHANGE_NAME-"].update(visible=values["-SEND_CHANGE-"])

    if not (values["-SEND_FILE-"]
            and values["-SEND_IP-"]):
        window["-SEND_START-"].update(disabled=True)
    else:
        window["-SEND_START-"].update(disabled=False)

    if saves_active > 1:
        window["-SAVE_REMOVE_0-"].update(disabled=False)
    else:
        window["-SAVE_REMOVE_0-"].update(disabled=True)

window.close()
