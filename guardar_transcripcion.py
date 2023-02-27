#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 11:12:02 2023

@author: mcerdeiro
"""

import json
import os

def guardar_transcripcion(path, fname):
    if os.path.splitext(fname)[1] == '.tif':
        fname = os.path.splitext(fname)[0] + '.json'
    with open(path+fname, 'r') as f:
        d = json.load(f)
    
    texto = ''
    for k in d:
        texto = texto + f'{k}: \n'
        print(f'{k}: \n')
        for e in d[k]:
            texto = texto + e
            print(e)
        texto = texto + '\n----------x----------\n'
        print('----------x----------')
    
    with open(f'{fname}_transcripcion.txt', 'w') as f:
        f.write(texto)
        
        
#%%
path = 'out_data/'
fname = 'La Voz 1985-05-04 Ratifican las Abuelas....json'
#fname = 'La Voz 1985-06-22 Detuvieron en Madrid....json'
guardar_transcripcion(path, fname)
#%%
path = 'out_data_manual/'
fname = 'La Voz 1985-05-04 Ratifican las Abuelas....json'
guardar_transcripcion(path, fname)


