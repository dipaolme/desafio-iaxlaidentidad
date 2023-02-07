#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 16:51:35 2022

@author: mcerdeiro
"""

# run.py
# tiene que ser parecido a digitize,py

# %% librerias
import argparse
from src.src import procesar_imgs

# def procesar_img(path_in, path_out)
desc = 'Software para transcripción de notas periodísticas'

parser = argparse.ArgumentParser(description=desc, epilog="Fundación Sadosky - Procuración del Tesoro de la Nación")
parser.add_argument('-e', '--entrada',
                    default="input_data/",
                    help="Directorio donde se encuentran los archivos de imagen para digitalizar.",
                    type=str)
parser.add_argument('-s', '--salida',
                    default='out_data/',
                    help="Directorio donde se guardan los resultados.",
                    type=str)
parser.add_argument('--modelo-corrector',
                    default='herramientas/model_juridico.bin',
                    help="Archivo del modelo del corrector ortográfico JamSpell (archivo .bin).",
                    type=str)


def main():
    args = parser.parse_args()

    procesar_imgs(path_in=args.entrada,
                  path_out=args.salida,
                  modelo_corrector=args.modelo_corrector)


main()
