#!/bin/python

import sys
import json
import requests
import logging
import os.path

def getJsonData(url):
    logging.info('Starting request for Json Data')
    bbResponse = requests.get(url)
    bbImageData = bbResponse.text
    jsonData = bbImageData.replace('(function(w,n){var a=w[n]=w[n]||{};a.browseData=', '')
    jsonData = jsonData.replace( ';})(window, \'BingGallery\');', '')
    arrays = json.loads(jsonData)
    return arrays

def filterByCategory(jsonData):
    indexes = []
    names = []
    for i, val in enumerate(jsonData["categories"]):
        if (val == "Nature" or val == "Animal" or val == "Travel" or val == "Science" or val == "Space" or val == "Cute"):
            indexes.append(i)
    for val in indexes:
        names.append(jsonData["imageNames"][val])
    return names

def downloadImages(directory, imageNames):
    urls = ["http://az608707.vo.msecnd.net/files/", "http://az619519.vo.msecnd.net/files/", "http://az619822.vo.msecnd.net/files/"]
    for image in imageNames:
        filename = directory + '/' + image + '.jpg'
        if not os.path.isfile(filename):
            for url in urls:
                imageRes = requests.get(url + image + '_1920x1200.jpg')
                if imageRes.status_code == 200:
                    with open(filename, 'wb') as outfile: outfile.write(imageRes.content)
                break
        else:
            logging.info('Skipping file, already downloaded')

def downloadBackgrounds():
    urls = ["http://az608707.vo.msecnd.net/files/", "http://az619519.vo.msecnd.net/files/", "http://az619822.vo.msecnd.net/files/"]
    arrays = getJsonData('https://www.bing.com/gallery/home/browsedata?z=0')
    names = filterByCategory(arrays)
    downloadImages('backgrounds', names)

logging.basicConfig(level=logging.INFO)
if __name__ == " __main__":
    logging.info('Starting downloader')
    downloadBackgrounds()
else:
    logging.info('Starting downloader')
    downloadBackgrounds()
