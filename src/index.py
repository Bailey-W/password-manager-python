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