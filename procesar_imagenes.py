#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 16:51:35 2022

@author: mcerdeiro
"""

# procesar_imagenes.py
# tiene que ser parecido a digitize,py

#%% librerias
import argparse
import src.src

# def procesar_img(path_in, path_out)
desc = 'Software para transcripción de notas periodísticas'


parser = argparse.ArgumentParser(description=desc, epilog="Fundación Sadosky - Procuración del Tesoro de la Nación")
parser.add_argument('imgs',
    help="Directorio donde se encuentran los archivos de imagen para digitalizar.",
    type=str)
parser.add_argument('-r', '--reporte',
    default='reporte_digitalizacion.xlsx',
    help="Archivo de salida excel, con el reporte del proceso de digitalización.",
    type=str)
parser.add_argument('-s', '--salida',
    default='resultados',
    help="Directorio donde se guardan los resultados.",
    type=str)
parser.add_argument('--txt',
    default='txt',
    help="Nombre del directorio de salida de los textos digitalizados, dentro del directorio de resultados.",
    type=str)
parser.add_arsgument('--modelo-corrector',
    default='./resources/model_juridico.bin',
    help="Archivo del modelo del corrector ortográfico JamSpell (archivo .bin).",
    type=str)

def main():
    args = parser.parse_args()
    
    
    
    
    ocr_files(path_in=args.imgs,
        archivo_salida=args.reporte,
        salida=args.salida,
        tmp=args.tmp,
        txts=args.txt,
        tesseract=args.tesseract,
        kodak=args.kodak,
        umbral_palabrasdesconocidas=args.umbral_palabras_desconocidas,
        umbral_diferenciaocr=args.umbral_diferencia_ocr,
        reporte=args.reporte_detallado,
        modelo_jamspell=args.modelo_corrector)

main()