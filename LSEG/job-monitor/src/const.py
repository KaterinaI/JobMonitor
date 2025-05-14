import os
from enum import Enum

LOG_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs', 'logs.log'))
TIME_FORMAT = "%H:%M:%S"
WARNING_THRESHOLD = 300    
ERROR_THRESHOLD = 600   
SCHEMA = ["time", "job", "status", "pid"]

class Status(Enum):
    START = "START"
    END = "END"

class Alert(Enum):
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"