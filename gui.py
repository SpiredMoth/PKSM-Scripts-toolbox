import PySimpleGUI as sg

########################
# Layout
########################

sg.theme("DarkAmber")


file_list_column = [
    [sg.Text("TODO: Save file selection GUI")],
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
            sg.Tab("Save Diff", layout=save_diff_layout),
            sg.Tab("Search", layout=save_search_layout),
            sg.Tab("Compile", layout=compile_layout),
            sg.Tab("Send", layout=send_layout),
        ]])
    ]], vertical_alignment="top", expand_y=True)
]]

window = sg.Window("PKSM-Scripts Development Tool",
                   layout=layout, resizable=True)

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        break

window.close()
