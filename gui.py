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
            sg.FileBrowse(file_types=save_types, target=f"-SAVE_FILE_{saves_active}-"),
        ]], key=f"-SAVE_{saves_active}-"),
    ]])


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

save_diff_layout = [
    [sg.Text("TODO: Save file diff GUI")],
]

save_search_layout = [
    [sg.Text("TODO: Save search GUI")],
]

compile_layout = [
    [sg.Text("TODO: Simple script creation and compilation GUI")],
]

send_layout = [
    [sg.Text("TODO: PKSM communication GUI")],
]

layout = [[
    sg.Column(file_list_column, vertical_alignment="top", expand_y=True),
    sg.Column([[
        sg.TabGroup([[
            sg.Tab("Send", layout=send_layout),
            sg.Tab("Compile", layout=compile_layout),
            sg.Tab("Save Diff", layout=save_diff_layout),
            sg.Tab("Search", layout=save_search_layout),
        ]])
    ]], vertical_alignment="top", expand_y=True)
]]

window = sg.Window("PKSM-Scripts Development Tool",
                   layout=layout, resizable=True)

while True:
    event, values = window.read()

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
        # hide last save input
        window[f"-SAVE_{saves_active-1}-"].update(visible=False)
        saves_active -= 1

    if saves_active > 1:
        window["-SAVE_REMOVE_0-"].update(disabled=False)
    else:
        window["-SAVE_REMOVE_0-"].update(disabled=True)

window.close()
