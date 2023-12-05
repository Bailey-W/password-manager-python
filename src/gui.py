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
        layout[1].append(sg.Text("Password does not match. Please try again.", text_color=('red')))

    window = sg.Window('Login', layout)

    event, values = window.read()
    window.close()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        return None

    return values['Password']

def show_main_window(entries):
    logger.log_event('Showing main screen', __name__)

    layout = [
                [sg.Text("Hello! Here are your entries:"), sg.Button('+')],
             ]
    
    for entry in entries:
        layout.append([sg.Text(entry[0]), sg.Text(entry[1]), sg.Text('*****'), sg.Button('Show', key=f'Show_{entry[0]}_{entry[1]}')])

    window = sg.Window('Password Manager', layout)

    event, values = window.read()
    window.close()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        return ['EXIT']

    if event == '+':
        return ['ADD']
    
    if 'Show' in event:
        data = event.split('_')[1:]
        return ['SHOW', data[0], data[1]]

def show_add_entry(incorrect = False):
    logger.log_event('Showing add entry screen', __name__)

    layout = [  [sg.Text('Add a new entry')],
                [],
                [sg.Text('Site: '), sg.InputText('', key='Site')],
                [sg.Text('Username: '), sg.InputText('', key='Username')],
                [sg.Text('Password: '), sg.InputText('', key='Password', password_char='*')],      
                [sg.Submit(), sg.Cancel()]]
    
    if incorrect:
        layout[1].append(sg.Text('Please fill out all fields', text_color=('red')))

    window = sg.Window('Add Entry', layout)

    event, values = window.read()
    window.close()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        return None
    
    if(not values['Username'] or not values['Site'] or not values['Password']):
        return show_add_entry(True)
    
    return (values['Username'], values['Site'], values['Password'])

def show_password(url, username, password):
    logger.log_event(f'Showing {url}:{username} password', __name__)

    layout = [  [sg.Text(url), sg.Text(username), sg.Text(password), sg.Button('Copy')], ]

    window = sg.Window('View Password', layout)

    event, values = window.read()
    window.close()