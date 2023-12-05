import logger
logger.log_event('Started process', __name__)
import db_manager
import password_manager

password_manager.add_entry("New User", "password", "www.spotify.com")