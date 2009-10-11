#!/usr/bin/env python
import hashlib
import os
import sys

"""Verify the website source hasn't changed.

This script verifies that the website source hasn't changed since the
last manual update. Running this script regularly ensures that the proper
method is used for updating the site which is through svn.

In the event of a change the script emails the admins.

"""

def buildDirectoryIntegrity(path,filename):
    """Creates a directory integrity file.

    Each line of the file lists the following attributes of a file:
    fullpath	filesize	md5sum

    The very last line of the file is the md5sum of the integrity file.
    """

    file = open(filename,'w')

    output = ''
    for dirpath, dirnames, filenames in os.walk(path,True,os.error):
        for filename in filenames:
            path = os.path.join(dirpath,filename)
            output += path+'\t'
            output += str(os.path.getsize(path))+'\t'
            output += hashlib.md5(open(path).read()).hexdigest()
            output += '\n'
    output += hashlib.md5(output).hexdigest()
    file.write(output)
    file.close()

def verifyDirectoryIntegrity(path,filename):
    # Verify integrity of integrity file
    integrity = open(filename).readlines()
    if hashlib.md5(''.join(integrity[:-1])).hexdigest() != integrity[-1]:
        raise 'integrity file compromised'

    # Verify line by line noting differences
    index = 0
    for dirpath, dirnames, filenames in os.walk(path,True,os.error):
        for filename in filenames:
            path = os.path.join(dirpath,filename)

            # Check length
            if index == len(integrity)-1:
                output += 'extra line: %s' % path
                continue

            i_filename, i_size, i_hash = integrity[index][:-1].split('\t')

            # Compare filenames
            if i_filename != path:
                raise 'file mismatch: %s %s' % (i_filename,path)

            # Compare filesizes
            if int(i_size) != os.path.getsize(path):
                raise 'size mismatch: %s %s' % (i_filename,path)

            # Compare file hashes
            if hashlib.md5(open(path).read()).hexdigest() != i_hash:
                raise 'hash mismatch: %s %s' % (i_filename,path)
                
            index += 1

if __name__ == '__main__':
    path = os.path.join(os.getcwd(),'../')
    filename = '/tmp/a'

    buildDirectoryIntegrity(path,filename)
    verifyDirectoryIntegrity(path,filename)

    print "Success"
