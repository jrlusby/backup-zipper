#! /usr/bin/env python3

"""
John R Lusby 2014

MIT License in file LICENSE
"""

import sys
import os
import re

#settings
backup_dir = "C:\Program Files\Microsoft SQL Server\MSSQL.1\MSSQL\Backup"
archive_dir = "C:\Program Files\Microsoft SQL Server\MSSQL.1\MSSQL\Archives"
local_tokeep = 5
ftp_tokeep = 5
#ftp settings
destination =
username =
password =
target_dir = 'BACKUPs/ATMMANAGERPRO'

def main(argv):
    #index the backup files
    backup_files = os.listdir(backup_dir)
    backup_ids = extract_ids(backup_files)
    backup_ids.sort()

    #index the archives
    archives = os.listdir(archive_dir)
    archive_ids = extract_ids(archives)
    archive_ids.sort()

    #compress the latest backup into the compressed backup directory
    tozipids = list(set(backup_ids) - set(archive_ids))
    print(tozipids)
    for id in tozipids:
        to_zips = []
        for file in backup_files:
            if id in file:
                to_zips.append(os.path.join(backup_dir, file))
        bzip_backups(to_zips, id)

    #index the archives
    archives = os.listdir(archive_dir)
    archive_ids = extract_ids(archives)
    archive_ids.sort()
    #trim backups in the atm manager pro backup directory
    for file in backup_files:
        for id in archive_ids:
            if id in file:
                print("removed " + file)
                os.remove(os.path.join(backup_dir, file))
                break

    #trim backups in the zipped backup directory
    for id in archive_ids[0:-local_tokeep]:
        for file in archives:
            if id in file:
                print("removed " + file)
                os.remove(os.path.join(archive_dir, file))
            else:
                print("keeping " + file)

    archives = os.listdir(archive_dir)
    archive_ids = extract_ids(archives)
    archive_ids.sort()
    #login to ftp
    #rewrite this to do a diff between the remote and the local and send everything thats in the local and not in the remote and then trim the remote
    from ftplib import FTP
    try:
        ftp = FTP(destination)
        ftp.login(user=username, passwd=password)
        ftp.cwd(target_dir)
        #index the archives already in the remote
        files = ftp.nlst()
        ftp_archives = []
        for file in files:
            if 'tar.gz' in file:
                ftp_archives.append(file)
        ftp_archive_ids = extract_ids(ftp_archives)
        ftp_archive_ids.sort()
        print(ftp_archive_ids)
        #move most recent backup to ftp server
        tosend_ids = list(set(archive_ids) - set(ftp_archive_ids))
        print(tosend_ids)
        for id in tosend_ids:
            archive = id + '.tar.gz'
            archive_full = os.path.join(archive_dir, archive)
            with open(archive_full, 'rb') as file:
                print(archive)
                ftp.storbinary('STOR ' + archive, file)
        #trim backups in the ftp server
        todelete = ftp_archive_ids[0:-ftp_tokeep]
        print(todelete)
        print(ftp_archive_ids)
        for id in todelete:
            for file in files:
                if id in file:
                    ftp.delete(file)
                    print("delete " + file)
                else:
                    print("keep " + file)
        ftp.quit()
    except:
        print('whoa wtf happened?', sys.exc_info())

def extract_ids(backup_files):
    backup_ids = []
    for file in backup_files:
        backup_id = re.findall(r'\d+', file)
        if len(backup_id) > 0 and backup_id[-1] not in backup_ids:
            backup_ids.append(backup_id[-1])
    return backup_ids

def zip_backups(files, dst):
    import zipfile
    zf = zipfile.ZipFile(dst, "w", allowZip64=True)
    for absname in files:
        basename = os.path.basename(absname)
        arcname = os.path.join(dst, basename)
        zf.write(absname, arcname)
    zf.close()

def bzip_backups(files, id):
    import tarfile
    with tarfile.open(os.path.join(archive_dir, id + ".tar.gz"), "w:gz") as tar:
        for absname in files:
            basename = os.path.basename(absname)
            print(basename)
            arcname = os.path.join(id, basename)
            print(arcname)
            tar.add(absname, arcname)
    print("done with " + id)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
