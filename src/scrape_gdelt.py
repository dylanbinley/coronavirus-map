import requests

GDELT_MASTER_FILE_LIST_URL = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'

GDELT_MASTER_FILE_LIST  = requests.get(GDELT_MASTER_FILE_LIST_URL, headers = {"Range": "bytes=0-105"})

for line in GDELT_MASTER_FILE_LIST.text.splitlines():
    *_, NEWEST_GDELT_STORY_LIST_URL = line.split()
    break

NEWEST_GDELT_STORY_LIST = requests.get(NEWEST_GDELT_STORY_LIST_URL).text

print(len(NEWEST_GDELT_STORY_LIST))
