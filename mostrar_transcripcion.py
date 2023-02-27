#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 11:12:02 2023

@author: mcerdeiro
"""

import json
import os

def mostrar_transcripcion(fname):
    if os.path.splitext(fname)[1] == '.tif':
        fname = os.path.splitext(fname)[0] + '.json'
    with open(fname, 'r') as f:
        d = json.load(f)
    
    for k in d:
        print(f'{k}: \n')
        for e in d[k]:
            print(e)
        print('----------x----------')
        

#fname = 'La Voz 1985-05-04 Ratifican las Abuelas'
#fname = 'La Voz 1985-06-22 Detuvieron en Madrid....json'
#mostrar_transcripcion(fname)
