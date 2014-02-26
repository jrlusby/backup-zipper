#! /usr/bin/env python3

"""
John R Lusby 2013

MIT License in file LICENSE
"""

import sys
import os
def main(argv):
    #settings
    backup_dir = "."
    archive_dir = "archives"
    local_tokeep = 2
    ftp_tokeep = 4
    #ftp settings
    destination
    username
    password
    target_dir

    backup_files = os.listdir(backup_dir)
    #compress the latest backup into the compressed backup directory
    ids = extract_backup_ids(backup_files)
    ids.sort()
    for id in ids:
        to_zips = []
        for file in filelist:
            if id in file:
                to_zips.append(file)
        bzip_backups(to_zips, id + '.tar.bz2')

    #trim backups in the atm manager pro backup directory
    for file in backup_files: #could also check if the file is in one of the archives,but its a lot more work
        os.remove(os.path.join(backup_dir, file))

    #trim backups in the zipped backup directory
    archives = os.listdir(archive_dir)
    ids = extract_backup_ids(archives)
    ids.sort()
    for id in ids[0:-local_tokeep]:
        for file in archives:
            if id in file:
                print("removed " + file)
                os.remove(os.path.join(archive_dir, file))
            else:
                print("keeping " + file)

    #login to ftp
    from ftplib import FTP
    try:
        ftp = FTP(destination)
        ftp.login(user=username, passwd=password)
        ftpcwd(target_dir)
        #move most recent backup to ftp server
        file = open(archive, 'rb')
        ftp.storbinary('STOR '+archive, file)
        #trim backups in the ftp server
        files = ftp.nlst()
        n = 3
        tokeeps = n_newest(files, n)
        if len(tokeeps) == n:
            for file in files:
                if file not in tokeeps:
                    #ftp.delete(file)
                    print("delete " + file)
                else:
                    print("keep " + file)
        file.close()
        ftp.quit()
    except:
        print('whoa wtf happened?', sys.exc_info()[0])

def extract_backup_ids(backup_files):
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

def bzip_backups(files, dst):
    import tarfile
    with tarfile.open(dst, "w:bz2") as tar:
        for absname in files:
            basename = os.path.basename(absname)
            arcname = os.path.join(dst, basename)
            tar.add(absname, arcname)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
