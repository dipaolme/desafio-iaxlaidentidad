#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 11:12:02 2023

@author: mcerdeiro
"""

import json


def mostrar_transcripcion(fname):
    with open(fname, 'r') as f:
        d = json.load(f)
    
    for k in d:
        print(f'{k}: \n')
        for e in d[k]:
            print(e)
        print('----------x----------')
        

fname = 'La Voz 1985-05-04 Ratifican las Abuelas....json'
fname = 'La Voz 1985-06-22 Detuvieron en Madrid....json'
mostrar_transcripcion(fname)