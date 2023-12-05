import logger
logger.log_event("Started process", __name__)

import PySimpleGUI as sg
import pyperclip

# Sets the theme for the GUI
sg.theme('Topanga')

# Shows the user a window asking for password
# If this is the first run, then it asks for the user to set a password
# Expects: first_time, to know if this is the first time a user has run the prrogram
#          incorrect, to know if the user tried before and got the password wrong
# Returns: Password if the user input one
#          None if the user did not input one or pressed cancel or closed the window
def show_login_window(first_time = False, incorrect = False):
    logger.log_event(f'Showing login screen: first time {first_time}', __name__)
    # If this is the first run, then prompt the user to set a master password
    text = 'This is your first time logging in. Please enter a master password and remember it.' if first_time else 'Enter master password:'
    layout = [  [sg.Text(text)],
                [],
                [sg.InputText('', key='Password', password_char='*')],      
                [sg.Submit(), sg.Cancel()]]
    
    # This means the user has tried before and got it wrong, so throw up an error message for them
    if incorrect:
        layout[1].append(sg.Text("Password does not match. Please try again.", text_color=('red')))

    window = sg.Window('Login', layout)

    event, values = window.read()
    window.close()

    # The user pressed cancel or the X, which will result in the program exiting
    if event == sg.WIN_CLOSED or event == 'Cancel':
        return None

    # Returns the password input by the user
    return values['Password']

# Shows the user the main window
# Expects: A list of entries (comprised of usernames and urls) to show the user
# Returns: The result of the window
#               Possible results are:
#               - EXIT: the user closed the window
#               - ADD: the user pressed the '+' button to add a new entry
#               - SHOW: the user pressed the show button on an entry, also includes data about the entry
def show_main_window(entries):
    logger.log_event('Showing main screen', __name__)

    layout = [
                [sg.Text("Hello! Here are your entries:", size=(70, None)), sg.Button('+')],
                [sg.Text('Website', size=(25,None)), sg.Text('Username', size=(25,None)), sg.Text('Password', size=(15,None)), sg.Text('Show')],
             ]
    
    # Adds every entry to the screen (username, url, censored password, and a show button)
    for entry in entries:
        layout.append([sg.Text(entry[0], size=(25,None)), sg.Text(entry[1], size=(25,None)), sg.Text('*****', size=(15,None)), sg.Button('Show', key=f'Show_{entry[0]}_{entry[1]}')])

    window = sg.Window('Password Manager', layout)

    event, values = window.read()
    window.close()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        return ['EXIT']

    # The user pressed the '+' button
    if event == '+':
        return ['ADD']
    
    # The user pressed the 'show' button on an entry
    if 'Show' in event:
        # Gets the information about the selected entry from the name of the button
        data = event.split('_')[1:]
        return ['SHOW', data[0], data[1]]

# Add entry screen, where the user can add username, password, and url for an entry
# Expects: incorrect, to show if the user incorrectly filled out the form previously
# Returns: the Username, url, and password
def show_add_entry(incorrect = False):
    logger.log_event('Showing add entry screen', __name__)

    layout = [  [sg.Text('Add a new entry')],
                [],
                [sg.Text('Site: '), sg.InputText('', key='Site')],
                [sg.Text('Username: '), sg.InputText('', key='Username')],
                [sg.Text('Password: '), sg.InputText('', key='Password', password_char='*'), sg.Checkbox("Generate", key='Generate')],      
                [sg.Submit(), sg.Cancel()]]
    
    # If the user incorrectly filled out the form before, tell them to fill everything in
    if incorrect:
        layout[1].append(sg.Text('Please fill out all fields', text_color=('red')))

    window = sg.Window('Add Entry', layout)

    event, values = window.read()
    window.close()

    if event == sg.WIN_CLOSED or event == 'Cancel':
        return None
    
    # The user did not enter a password or select to generate a password
    if not values['Password'] and not values['Generate']:
        # Show the window to the user again, this time with an error message
        return show_add_entry(True)

    # The user did not enter a username or did not enter a url
    if(not values['Username'] or not values['Site']):
        # Show the window to the user again, this time with an error message
        return show_add_entry(True)
    
    # Marks the password for generation if generate is selected
    password = values['Password'] if not values['Generate'] else None

    return (values['Username'], values['Site'], password)

# Shows the user a username, password, url combination and lets them copy it
# Expects: url, the url
#          username, the username
#          password, the decrypted password
#          copied, if the user previously copied the password
def show_password(url, username, password, copied=False):
    logger.log_event(f'Showing {url}:{username} password', __name__)

    layout = [ [],
               [sg.Text(url), sg.Text(username), sg.Text(password), sg.Button('Copy')], 
               [sg.CloseButton('Close')]]
    
    # If the user previously copied the password, show a success message
    if copied:
        layout[0].append(sg.Text('Password copied to clipboard', text_color='green'))

    window = sg.Window('View Password', layout)

    event, values = window.read()
    window.close()

    # if the user clicks copy
    if event == 'Copy':
        # Copy the password to their clipboard
        pyperclip.copy(password)
        # Reload the window, this time with a success message
        show_password(url, username, password, True)