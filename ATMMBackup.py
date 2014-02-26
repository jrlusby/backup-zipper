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
def main(argv):
    #trim backups in the atm manager pro backup directory
    #trim backups in the zipped backup directory
    #compress the latest backup into the compressed backup directory
    #trim backups in the ftp server
    #move recent backup to ftp server
    test_files = ['A/a.txt', 'A/b.txt']
    bzip_backups(test_files, 'test.tar.bz2')

def trim_backups(dir, tokeep):
    backup_files = os.listdir(dir)
    ids = extract_backup_ids(backup_files) #essentially counts the total number of backups
    ids.sort()
    # print(ids)
    if len(ids) > tokeep: #if theres more than 2 backups
        for id in ids[:len(ids)-tokeep]: #for each backup older than the two newest
            for file in backup_files: #for each file 
                if id in file: #if it belongs to an old backup
                    os.remove(os.path.join(argv[1],file)) #delete the file
                    print('removed %s' % file)

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
                else:
                    print("keep " + file)
        file.close()
        ftp.quit()
    except:
        print('whoa wtf happened?', sys.exc_info()[0])

if __name__ == '__main__':
    sys.exit(main(sys.argv))
