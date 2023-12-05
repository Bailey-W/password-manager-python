import logger
logger.log_event('Started process', __name__)
import db_manager
import password_manager
import gui
import keygen

success = False
first_time = True
while not success:
    master = gui.show_login_window(not keygen.check_master_exists(), not first_time)
    first_time = False
    if not master:
        logger.log_event('Exiting...', __name__)
        exit()
    success = password_manager.login(master)

result = ['']

while result[0] != 'EXIT':
    result = gui.show_main_window(db_manager.get_all_entries())
    if result[0] == 'ADD':
        data = gui.show_add_entry()
        if not data[2]:
            password_manager.add_entry_with_generated_password(data[0], data[1])
        else:
            password_manager.add_entry(data[0], data[2], data[1])
    if result[0] == 'SHOW':
        password = password_manager.get_password_for_entry(result[2], result[1])
        gui.show_password(result[1], result[2], password)

# success = False
# while not success:
#     password = input("Enter your password: ")
#     success = password_manager.login(password)
#     print(success)

# username = input('Enter username: ')
# # password = input('Enter password: ')
# url = 'http://google.com'

# # password_manager.add_entry(username, password, url)

# print(password_manager.get_password_for_entry(username, url))