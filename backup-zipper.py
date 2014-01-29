#! /usr/bin/env python3

import sys
import os
import zipfile
import re
import datetime

today = datetime.date.today()
id = today.strftime('%m_%d_%Y')

def main(argv):
    # print("1 "+id)
    filelist = process_backups(argv[1])
    # print("3 "+id)
    destination = "backup_"+id+".zip"
    zip(filelist, destination)
    # upload zip to remote
    # upload_arc(destination, 'BACKUPs/ATMMANAGERPRO', '192.168.26.80', 'support', 'asai1234')
    os.remove(destination)

def zip(files, dst):
    zf = zipfile.ZipFile(dst, "w", allowZip64=True)
    for absname in files:
        basename = os.path.basename(absname)
        arcname = os.path.join(dst, basename)
        zf.write(absname, arcname)
    zf.close()

def process_backups(src):
    filelist = os.listdir(src)
    filelist[:] = [os.path.join(src, file) for file in filelist]
    ids = extract_backup_ids(filelist)
    ids.sort()
    to_zips = []
    global id
    id = ids[len(ids)-1]
    # print("2 "+id)
    for file in filelist:
        if ids[len(ids)-1] in file:
            to_zips.append(file)
    return to_zips

def extract_backup_ids(backup_files):
    backup_ids = []
    for file in backup_files:
        backup_id = re.findall(r'\d+', file)
        if len(backup_id) > 0 and backup_id[-1] not in backup_ids:
            backup_ids.append(backup_id[-1])
    return backup_ids
    
def upload_arc(archive, target_dir, destination, username, password):
    from ftplib import FTP
    try:
        ftp = FTP(destination)
        ftp.login(user=username, passwd=password)
        ftp.cwd(target_dir)
        file = open(archive, 'rb')
        ftp.storbinary('STOR '+archive, file)
        file.close()
        ftp.quit()
    except:
        print('whoa wtf happened?', sys.exc_info()[0])

if __name__ == '__main__':
    sys.exit(main(sys.argv))
