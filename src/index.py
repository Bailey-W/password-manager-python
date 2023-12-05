import logger
logger.log_event('Started process', __name__)
import db_manager
import password_manager
import gui
import keygen

# Starts by asking for the password
success = False
first_time = True
while not success:                                                                      # Asks repeatedly until the user gets it right
    master = gui.show_login_window(not keygen.check_master_exists(), not first_time)    # Shows the window where the user enters password, returns the entered password
    first_time = False                                                                  # This tracks whether the user has entered the password incorrectly before
    if not master:                                                                      # If the user does not enter a password, or presses cancel or X, then the program exits
        logger.log_event('Exiting...', __name__)
        exit()
    success = password_manager.login(master)                                            # Checks if the password matches

result = ['']

while result[0] != 'EXIT':                                                              # This loops until the user exits the program (with the X)
    result = gui.show_main_window(db_manager.get_all_entries())                         # Shows the user the main window (containing all of the entries that come from db_manager) and stores the result
    if result[0] == 'ADD':                                                              # This result means the user pressed the "+" button to add a new entry
        data = gui.show_add_entry()                                                     # Shows the user the add entry screen and stores the input
        if not data[2]:                                                                 # The only way this could happen is if the user selected to generate a password
            password_manager.add_entry_with_generated_password(data[0], data[1])        # Stores a new entry using the input username, url, and the generated password
        else:
            password_manager.add_entry(data[0], data[2], data[1])                       # This means the user input a password, so it stores an entry with the input data
    if result[0] == 'SHOW':                                                             # This result means that the user clicked on the "Show" button on an entry
        password = password_manager.get_password_for_entry(result[2], result[1])        # Gets the corresponding password (decrypted)
        gui.show_password(result[1], result[2], password)                               # Opens a new window for the user showing the password