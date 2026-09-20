TIME = r"(\d{4}-\d{2}-\d{2} +\d{2}:\d{2}:\d{2})\s+"
SOURCE_COMP=r'\|\s+(\w+)\s+'
LOG_LEVEL= r'\|\s+(\w+)\s+'
MESSAGE=r'\|\s+(.+)'
PATTERN = TIME + LOG_LEVEL + SOURCE_COMP + MESSAGE
