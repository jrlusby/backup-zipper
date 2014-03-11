#! /usr/bin/env python3

"""
John R Lusby 2014

MIT License in file LICENSE
"""

import sys, os, re

#settings
local_dir = "C:\Program Files\Microsoft SQL Server\MSSQL.1\MSSQL\Backup"
max_backups = 14
#ftp settings
destination =
username =
password =
target_dir = 'BACKUPs/spiceworks'

def main(argv):
    ftp_sync(local_dir, target_dir, destination, username, password)

def ftp_sync(local_dir, target_dir, destination, username, password):
    from ftplib import FTP
    try:
        #connect to ftp server
        ftp = FTP(destination)
        ftp.login(user=username, passwd=password)
        #select target directory
        ftp.cwd(target_dir)
        #index the files in remote and local directories
        local_files = os.listdir(local_dir)
        print("local files: " + local_files)
        remote_files = ftp.nlst()
        print("remote files: " + remote_files)
        #create file diffs
        local_only = list(set(local_files) - set(remote_files))
        print("local only files: " + local_only)
        remote_only = list(set(remote_files) - set(local_files))
        print("remote only files: " + remote_only)
        #copy local only files to remote
        print("storing")
        for file in local_only:
            print(file)
            with open(os.path.join(local_dir, file), 'rb') as binary_file:
                ftp.storbinary('STOR ' + file, binary_file)
        #delete remote only files from remote
        print("deleting")
        for file in remote_only:
            print(file)
            ftp.delete(file)
    except:
        print('wtf')

if __name__ == '__main__':
    sys.exit(main(sys.argv))