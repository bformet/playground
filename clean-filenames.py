#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os.path, os, fnmatch

for dir in ['Films', u'Dessins animés', u'Séries']:
    for root, dirnames, filenames in os.walk('/media/removable/Externe/'+dir):
        # Clean directory names
        for dirname in fnmatch.filter(dirnames, '[[]*[]] *'):
            newname = dirname.split('] ')[-1]
            print u'%s => %s' % (dirname, newname)
            os.rename(os.path.join(root, dirname), os.path.join(root, newname))
            
    for root, dirnames, filenames in os.walk('/media/removable/Externe/'+dir):
        # Clean file names
        for filename in fnmatch.filter(filenames, '[[]*[]] *.*'):
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
