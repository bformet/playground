#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, fnmatch

# remove trailing brackets from names
PATTERN = '[[]*[]] *' 

def clean_folder( path_list ):
    for path in path_list:
        for root, dirnames, filenames in os.walk(path):
            # Clean directory names
            for dirname in fnmatch.filter(dirnames, PATTERN):
                newname = dirname.split('] ')[-1]
                print u'%s => %s' % (dirname, newname)
                os.rename(os.path.join(root, dirname), os.path.join(root, newname))
                
        for root, dirnames, filenames in os.walk(path):
            # Clean file names
            for filename in fnmatch.filter(filenames, PATTERN):
                newname = filename.split('] ')[-1]
                print u'%s => %s' % (filename, newname)
                os.rename(os.path.join(root, filename), os.path.join(root, newname))

            # Delete dat files
            for filename in fnmatch.filter(filenames, '*.dat'):
                print 'removing %s' % os.path.join(root, filename)
                os.remove(os.path.join(root, filename))

            # Delete .db files
            for filename in fnmatch.filter(filenames, 'Thumbs.db'):
                print 'removing %s' % os.path.join(root, filename)
                os.remove(os.path.join(root, filename))


if __name__ == '__main__':

    path_list = sys.argv[1:] or map(lambda x: '/media/removable'+x, ['Films', u'Dessins animés', u'Séries'])

    clean_folder(path_list)
