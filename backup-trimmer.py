#! /usr/bin/env python3

import sys
import os
import re

def main(argv):
    print("whatever")
    backup_files = os.listdir(argv[1])
    print(backup_files)
    ids = extract_backup_ids(backup_files) #essentially counts the total number of backups
    ids.sort()
    print(ids)
    if len(ids) > 1: #if theres more than 2 backups
        for item in ids[:len(ids)-1]: #for each backup older than the two newest
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
