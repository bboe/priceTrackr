#!/usr/bin/env python
import cPickle, pprint, sys, tarfile

def main():
    try:
        tfile = tarfile.open(sys.argv[1])
    except:
        raise

    for tarinfo in tfile:
        print tarinfo.name
        data = cPickle.loads(tfile.extractfile(tarinfo).read())
        sys.stdout.write('\t')
        pprint.pprint(data.error)

if __name__ == '__main__':
    main()
