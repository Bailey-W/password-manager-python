import logger
logger.log_event("Started process", __name__)

import PySimpleGUI as sg

sg.theme('Topanga')

def show_login_window(first_time = False, incorrect = False):
    logger.log_event(f'Showing login screen: first time {first_time}', __name__)
    text = 'This is your first time logging in. Please enter a master password and remember it.' if first_time else 'Enter master password:'
    layout = [  [sg.Text(text)],
                [],
                [sg.InputText('', key='Password', password_char='*')],      
                [sg.Submit(), sg.Cancel()]]
    
    if incorrect:
        layout[1].append(sg.Text("Password does not match. Please try again."))

    window = sg.Window('Login', layout)

    event, values = window.read()
    window.close()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        return None

    return values['Password']