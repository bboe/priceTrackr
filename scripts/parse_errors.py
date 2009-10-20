#!/usr/bin/env python
import cPickle, os, re, sys

if __name__ == '__main__':
    def usage(msg=None):
        if msg:
            sys.stderr.write('%s\n' % msg)
        sys.stderr.write('Usage: %s folder\n' % sys.argv[0])
        sys.exit(1)

    if len(sys.argv) != 2: usage()
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        usage('File %s does not exist' % directory)

    for fname in os.listdir(directory):
        id = fname.strip('.html')
        rr = cPickle.load(open(os.path.join(directory, fname)))
        print '%s: Status: %s Error: %s' % (id, rr.responseStatus, rr.errorMsg)



    
