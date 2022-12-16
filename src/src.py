#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 16:58:38 2022

@author: mcerdeiro
"""
#%% librerias
import cv2
import numpy as np
import pytesseract
import jamspell
import re
import os
import pandas as pd

#%% funciones de preprocesamiento
def preprocesamiento(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
#%% funciones de transcripcion
def ocr_tesseract(filename, path_in, path_out):
    img = cv2.imread(path_in+filename)
    preprocessed_img = preprocesamiento(img)
    if isinstance(preprocessed_img, np.ndarray):
        custom_config = r'-c tessedit_char_whitelist="AÁBCDEÉFGHIÍJKLMNÑOÓPQRSTUÚVWXYZaábcdeéfghiíjklmnñoópqrstuúvwxyz0123456789 -_/.,:;"'
        text = str(((pytesseract.image_to_string(preprocessed_img,lang="spa", config=custom_config))))
        with open(str(path_out+filename), "wb") as f:
            f.write(text.encode("utf-8"))
    return text
#%% funciones de correccion del texto
def inicializar_corrector(path_modelo = './resources/model_juridico.bin'):
    corrector = jamspell.TSpellCorrector()
    assert(corrector.LoadLangModel(path_modelo))
    return corrector

def spellcheck(corrector, texto):
    return corrector.FixFragment(texto)

def unir_saltos_linea(text):
    text = text.replace('-\n', '')    
    return text.replace('_\n', '')

def filtrar_simbolosvalidos(texto):
    temp = re.sub("[^A-Za-z0-9áéíóúüñÁÉÍÓÚÜÑ.,;\s]", ' ', texto)
    temp = re.sub("\n", ' ', temp)
    return re.sub(' +', ' ', temp)

def es_basura(string):
    return all(len(x) < 3 for x in string.split(' '))

def postprocesamiento(text, corrector):
    text = os.linesep.join([s for s in text.splitlines() if s])
    text = os.linesep.join([s for s in text.splitlines() if not es_basura(s)])
    text = unir_saltos_linea(text)    
    text = spellcheck(corrector, text)    
    # text = unir_saltos_linea(text) # por qué otra vez?
    text = filtrar_simbolosvalidos(text)
    # text = text.lower() # por qué?
    text = spellcheck(corrector, text) # por qué otra vez?
    # text = text.lower()
    return text    
#%% funciones de chequeo de las transcripciones   
def palabras_desconocidas(texto, corrector):
    cantidad = 0
    for palabra in texto.split():
        cantidad += 0 if corrector.WordIsKnown(palabra) else 1
    return cantidad 

def chequeo_calidad(data, output_file, umbral_palabrasdesconocidas = 0.015):
    writer = pd.ExcelWriter(output_file, engine="xlsxwriter")
    workbook = writer.book
    percent_fmt = workbook.add_format({'num_format': '0.0%'})
    emp_format = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#000000', 'bold': True})
    data.to_excel(writer, index=False, sheet_name="reporte")
    worksheet = writer.sheets["reporte"]
    worksheet.set_column('B:C', 12, percent_fmt)
    worksheet.conditional_format(f"B2:B{len(data.index) + 1}", {"type": "cell", "criteria": ">=", "value": umbral_palabrasdesconocidas, "format": emp_format})
    writer.save()

#%% 
def procesar_imgs(path_in, path_out, modelo_corrector = './resources/model_juridico.bin'):
    corrector = inicializar_corrector(modelo_corrector)
    data = []
    for filename in path_in:
        texto = ocr_tesseract(filename, path_in, path_out)
        texto = postprocesamiento(texto, corrector)
        pp_desc = palabras_desconocidas(texto,corrector)/len(texto.split())
        data.append({'filename':filename, 'palabras_desconocidas':pp_desc})
        with open(path_out+filename, "wb") as text_file:
            text_file.write(texto.encode("utf-8"))
            


    
