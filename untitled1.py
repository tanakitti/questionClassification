#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 15:50:39 2018

@author: MacBookPro
"""

import pythainlp
import numpy as np

text = "หลับเป็นเพื่อนน้องมั้ย"

words = pythainlp.tokenize.word_tokenize(text, engine='newmm')
partofspeech = pythainlp.tag.pos_tag(words, engine='unigram', corpus='orchid')

print(partofspeech)


tagset = np.array([]);
textvec = np.zeros(7)
print(textvec)