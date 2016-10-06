#!/usr/bin/python

import logging
import os
import exifread
import json
import sys

def replace_right(source, target, replacement, replacements=None):
    return replacement.join(source.rsplit(target, replacements))

def getFiles(dir):
    files = []
    for (path, dirnames, filenames) in os.walk(dir):
        files.extend(filenames)
        break
    logging.info('Read files')
    return files

def getEXIFtitle(directory, filename):
    logging.info('Looking for title tag in ' + filename)
    f = open(directory + '/' + filename, 'rb')
    tags = exifread.process_file(f, details=False)
    for tag in tags.keys():
        if tag == 'Image ImageDescription':
            logging.info('Found title tag for ' + filename)
            return tags[tag].values

def buildJson(numOfBgs):
    files = getFiles('backgrounds')
    bgjson = "{\"backgrounds\": ["
    i = 0
    for file in files:
        if i > int(numOfBgs):
            break;
        title = getEXIFtitle('backgrounds', file)
        if title is None:
            title = file
        title = title.replace("\t", " ")
        bgjson = bgjson + "{\"filename\": \"" + file + "\", \"title\": \"" + title + "\" },"
        i = i + 1
    bgjson = replace_right(bgjson, ",", "", 1)
    bgjson = bgjson + "]}"
    return json.dumps(bgjson)

logging.basicConfig(level=logging.INFO)

#if __name__ == '__main__':
num = 2000
if len(sys.argv) > 1:
    num = sys.argv[1]
bgjson = buildJson(num)
jsonFile = open('backgrounds.json', 'w')
jsonFile.write(bgjson)
jsonFile.close()
#else:
#    buildJson()


