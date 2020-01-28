#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyFingerprint
Copyright (C) 2015 Bastian Raschke <bastian.raschke@posteo.de>
All rights reserved.

"""

import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import json
import urllib.request
import subprocess
import sqlite3
import datetime
from random import randint
import requests
import settings

def make_request(user_id):
    url = settings.WEB_APP_URL
    data = {
            'user_id' : user_id
            }
    post = requests.post(url, data=data)
    return post


## Play sound
def sound(level):
    cmd = "aplay -D hw:1,0 ~/works/audioplay/level"+str(level)+".wav"
    subprocess.call(cmd, shell=True)
##

## Search for a finger
##

## Tries to initialize the sensor
try:
    f = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to search the finger and calculate hash
try:
    print('Waiting for finger...')

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)

    ## Searchs template
    result = f.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]

    if ( positionNumber == -1 ):
        print('No match found!')
        exit(0)
    else:
        print('Found template at position #' + str(positionNumber))
        print('The accuracy score is: ' + str(accuracyScore))

        ## OPTIONAL stuff
        ##

        ## Loads the found template to charbuffer 1
        f.loadTemplate(positionNumber, 0x01)

        ## Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

        ## Hashes characteristics of template
        print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())
       
        user_id = positionNumber+1
        res = make_request(user_id).json()
        expected_day = res['expected_day']
        sound_level = res['sound_level']
        user_id = res['user_id']
        print(datetime.datetime.fromtimestamp(expected_day))
        print(sound_level)
        print(user_id)

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)
