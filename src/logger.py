from time import time
from datetime import datetime
import os

def get_current_time_formatted(for_file = False) -> str:
    now = datetime.now()
    if for_file:
        formatted_time = now.strftime('%Y-%m-%d %H_%M_%S')
    else:
        formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    return str(formatted_time)

def create_log_file():
    global log_file_path
    log_file_path = os.path.dirname(os.path.abspath(__file__)) + "/../logs/"
    log_file_path += get_current_time_formatted(True) + '.log'
    log_file = open(log_file_path, 'w')
    log_file.close()
    log_event("Created log file")

def log_event(event: str):
    log_file = open(log_file_path, 'a')
    log_file.write(get_current_time_formatted() + ": " + event + '\n')
    log_file.close()

create_log_file()
