#! /usr/bin/env python3

import sys
import os
import zipfile
import re
import datetime

today = datetime.date.today()
id = today.strftime('%m_%d_%Y') #default value for whynot

def main(argv):
    # filelist = process_backups(argv[1])
    filelist = os.listdir(argv[1])
    filelist[:] = [os.path.join(argv[1], file) for file in filelist]
    tobackup = process_backups(filelist)
    destination = "backup_"+id+".zip"
    zip(tobackup, destination)
    # upload zip to remote
    upload_arc(destination, 'BACKUPs/ATMMANAGERPRO', '192.168.26.80', 'support', 'asai1234')
    # print(n_newest(filelist))
    os.remove(destination)

def zip(files, dst):
    zf = zipfile.ZipFile(dst, "w", allowZip64=True)
    for absname in files:
        basename = os.path.basename(absname)
        arcname = os.path.join(dst, basename)
        zf.write(absname, arcname)
    zf.close()

def n_newest(files, n=3):
    ids = extract_backup_ids(files)
    ids.sort()
    newest = []
    if len(ids) > n:
        newest = ids[-n:]
    else:
        newest = ids
    newest_files = []
    for id in newest:
        for file in files:
            if id in file:
                newest_files.append(file)
    return newest_files

def process_backups(filelist):
    # filelist = os.listdir(src)
    # filelist[:] = [os.path.join(src, file) for file in filelist]
    ids = extract_backup_ids(filelist)
    ids.sort()
    to_zips = []
    global id
    id = ids[len(ids)-1]
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
        files = ftp.nlst()
        n = 3
        tokeeps = n_newest(files, n)
        if len(tokeeps) == n:
            for file in files:
                if file not in tokeeps:
                    #ftp.delete(file)
                    print("delete " + file)
                else
                    print("keep " + file)
        file.close()
        ftp.quit()
    except:
        print('whoa wtf happened?', sys.exc_info()[0])

if __name__ == '__main__':
    sys.exit(main(sys.argv))
