from distutils.log import INFO
import os


class Config:
    """Base configuration variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    LOGIN_DISABLED = True
    LOG_LEVEL = INFO
  #  if not SECRET_KEY:
  #      raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
