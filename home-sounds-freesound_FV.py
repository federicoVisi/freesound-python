#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 22:55:13 2020

@author: federicovisi
"""

#TODO: turn into a function that takes a class name and a dictionary of tags

from __future__ import print_function
import freesound
import os
import sys
    
with open("_FV_freesound_API_key.txt", "r") as key_file:
    api_key = os.getenv('FREESOUND_API_KEY', key_file.read())
    
with open("_FV_freesound_oauth_token.txt", "r") as token_file:
    oauth_token = token_file.read()


if api_key is None:
    print("You need to set your API key as an evironment variable",)
    print("named FREESOUND_API_KEY")
    sys.exit(-1)
    
freesound_client = freesound.FreesoundClient()

#freesound_client.set_token(api_key)

print(oauth_token)
freesound_client.set_token(oauth_token,"oauth2")

#look for a sub category such as kitchen-> glass; coffee grinder e.g.

sound_classes = ["kitchen", "dining room", "outdoors", "city", "living room"]

kitchen_tags = ["glass","pots","cooking"]
dining_tags = ["door","eating","table"]
outdoors_tags = ["birds","forest","river"]
city_tags = ["bus","train","traffic"]
living_tags = ["tv","chatting","playing"]

tags_dict = {
    "kitchen": kitchen_tags,
    "dining room": dining_tags,
    "outdoors": outdoors_tags,
    "city": city_tags,
    "living room": living_tags    
    }    

# N_sounds = 5


# Requirements: 44100hz wav; or 320 192 mp3; at least 1 sec long

for sound_class in sound_classes:
    for tag_idx in range(len(tags_dict[sound_class])):
        # Search Example
        print("Searching for '",sound_class,"'; tag:",tags_dict[sound_class][tag_idx]," :")
        print("----------------------------")
        results_pager = freesound_client.text_search(
            query=sound_class,
            filter="duration:[1.0 TO 15.0] samplerate:44100 tag:"+tags_dict[sound_class][tag_idx],        
            sort="rating_desc",
            fields="id,name,previews,username,duration,samplerate"
        )
        print("Num results:", results_pager.count)
        print("\t----- PAGE 1 -----")
        for sound in results_pager:
            print("\t-", sound.name, "\t|", sound.duration, "sec \t|", sound.samplerate, "Hz \t|")
        # print("\t----- PAGE 2 -----")
        # results_pager = results_pager.next_page()
        # for sound in results_pager:
        #     print("\t-", sound.name, "by", sound.username)
        print()
    
        #download sound previews
        # dir_name=sound_class+'-'+tags_dict[sound_class][tag_idx]
        # os.mkdir(dir_name)
        # for sound in results_pager:
        #     sound.retrieve_preview(dir_name, sound.name+'.mp3')
        #     print(sound.name)
        
        # #download sound
        # dir_name=sound_class+'-'+tags_dict[sound_class][tag_idx]
        # os.mkdir(dir_name)
        # for sound in results_pager:
        #     sound.retrieve(dir_name)
        #     print(sound.name)        















