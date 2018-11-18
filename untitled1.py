#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 15:50:39 2018

@author: MacBookPro
"""
from collections import defaultdict

import pythainlp




text = "ใครเป็นคนไทยบ้าง"






words = pythainlp.tokenize.word_tokenize(text, engine='mm')
partofspeech = pythainlp.tag.pos_tag(words, engine='perceptron', corpus='orchid')

print(partofspeech)


food_list = 'spam spam spam spam spam spam eggs spam'.split()
food_count = defaultdict(int) # default value of int is 0
for food in partofspeech:
    food_count[food[1]] += 1 # increment element's value by 1



