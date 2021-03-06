#! /usr/bin/env python3

"""
You pass the full path to the directory containing the backups as an argument
to the script
Execute it as an argument of the python3 interpreter, I tried adding it to the
path but for some reason its not working. so just prefix the script with
C:\Python33\python.exe
You can modify the number of backups to keep with the NUM_BACKUPS_TO_KEEP
variable

John R Lusby 2013

MIT License
"""

import sys
import os
import re

NUM_BACKUPS_TO_KEEP = 1

def main(argv):
    backup_files = os.listdir(argv[1])
    ids = extract_backup_ids(backup_files) #essentially counts the total number of backups
    ids.sort()
    # print(ids)
    if len(ids) > NUM_BACKUPS_TO_KEEP: #if theres more than 2 backups
        for item in ids[:len(ids)-NUM_BACKUPS_TO_KEEP]: #for each backup older than the two newest
            for file in backup_files: #for each file 
                if item in file: #if it belongs to an old backup
                    os.remove(os.path.join(argv[1],file)) #delete the file
                    print('removed %s' % file)

def extract_backup_ids(backup_files):
    backup_ids = []
    for file in backup_files:
        backup_id = re.findall(r'\d+', file)
        if backup_id[0] not in backup_ids:
            backup_ids.append(backup_id[0])
    return backup_ids

if __name__ == '__main__':
    sys.exit(main(sys.argv))
