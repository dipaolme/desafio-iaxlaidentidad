#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 16:58:38 2022

@author: mcerdeiro
"""
import json

# %% librerias
import cv2
import numpy as np
import pytesseract
import jamspell
import re
import os
import pandas as pd
import matplotlib.pyplot as plt

# %% directorios
path_in = 'input_data/'
path_out = 'out_data/'


# %% funciones de preprocesamiento
def preprocesamiento(img):
    # with open(img, 'r') as f:
    m = cv2.imread(img)
    m = cv2.cvtColor(m, cv2.COLOR_BGR2GRAY)
    return m


# %% funciones de transcripcion
def ocr_tesseract(filename, path_in, path_out):
    preprocessed_img = preprocesamiento(path_in + filename)
    if isinstance(preprocessed_img, np.ndarray):
        custom_config = r'-c tessedit_char_whitelist="AÁBCDEÉFGHIÍJKLMNÑOÓPQRSTUÚVWXYZaábcdeéfghiíjklmnñoópqrstuúvwxyz0123456789 -_/.,:;()"'
        text = str((pytesseract.image_to_string(preprocessed_img, lang="spa", config=custom_config)))
    return text


# %% funciones de correccion del texto
def inicializar_corrector(path_modelo='./herramientas/model_juridico.bin'):
    corrector = jamspell.TSpellCorrector()
    assert (corrector.LoadLangModel(path_modelo))
    return corrector


def spellcheck(corrector, texto):
    return corrector.FixFragment(texto)


def unir_saltos_linea(text):
    text = text.replace('-\n', '')
    return text.replace('_\n', '')


def filtrar_simbolosvalidos(texto):
    """
    Reemplaza los símbolos no presentes en el diccionario español por espacios en blanco
    """
    temp = re.sub("[^A-Za-z0-9áéíóúüñÁÉÍÓÚÜÑ.,;:{}()\+\'\"!¡¿?°\[\]\-\s]", ' ', texto)
    # temp = re.sub("\n", ' ', temp)
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
    text = spellcheck(corrector, text)  # por qué otra vez?
    # text = text.lower()
    return text


# %% funciones de chequeo de las transcripciones
def palabras_desconocidas(texto, corrector):
    cantidad = 0
    for palabra in texto.split():
        cantidad += 0 if corrector.WordIsKnown(palabra) else 1
    return cantidad


def chequeo_calidad(data, output_file, umbral_palabrasdesconocidas=0.015):
    writer = pd.ExcelWriter(output_file, engine="xlsxwriter")
    workbook = writer.book
    percent_fmt = workbook.add_format({'num_format': '0.0%'})
    emp_format = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#000000', 'bold': True})
    data.to_excel(writer, index=False, sheet_name="reporte")
    worksheet = writer.sheets["reporte"]
    worksheet.set_column('B:C', 12, percent_fmt)
    worksheet.conditional_format(f"B2:B{len(data.index) + 1}",
                                 {"type": "cell", "criteria": ">=", "value": umbral_palabrasdesconocidas,
                                  "format": emp_format})
    writer.save()


# %%
def procesar_imgs(path_in, path_out, modelo_corrector='herramientas/model_juridico.bin'):
    """
    Guarda en reporte.csv
    """
    corrector = inicializar_corrector(modelo_corrector)
    data = []
    for filename in os.listdir(path_in):
        if os.path.splitext(filename)[1] == '.tif':
            print(filename)
            texto = ocr_tesseract(filename, path_in, path_out)
            texto = postprocesamiento(texto, corrector)
            pp_desc = palabras_desconocidas(texto, corrector) / len(texto.split())
            data.append({'filename': filename, 'palabras_desconocidas': pp_desc})

            noticia_procesada = {"Diario": [],
                                 "Fecha": [],
                                 "Volanta": [],
                                 "Título": [],
                                 "Cuerpo": [],
                                 "Copete": [],
                                 "Destacado": [],
                                 "Epígrafe": []}

            noticia_procesada["Cuerpo"].append(texto)

            with open(path_out + os.path.splitext(filename)[0] + '.json', "w") as json_file:
                json.dump(noticia_procesada, json_file, ensure_ascii=False)

    reporte = pd.DataFrame(data=data)
    reporte.to_csv(path_out + 'reporte.csv', index=False)
    print("Reporte guardado en", path_out + "reporte.csv")

# %%
# ejemplo
# img = path_in + 'imagen1.tif'
# img_preprocesada = preprocesamiento(img)
# # %%
# # cv2.imshow('ventana1', img_preprocesada)
# # cv2.waitKey(0)
# cv2.destroyAllWindows()
# # %%
# plt.figure(figsize=(34, 23))
# plt.imshow(img_preprocesada, cmap='gray')
# # %%
# print(img_preprocesada.shape)
# # %%
# texto_img = ocr_tesseract('imagen1.tif', path_in, path_out)
# corrector = inicializar_corrector()
# texto_img_corregido = postprocesamiento(texto_img, corrector)
# print(texto_img_corregido)
# # %%
# output_file = path_out + 'resultados.xls'
#
# chequeo_calidad(texto_img_corregido, output_file=path_out + 'resultados', umbral_palabrasdesconocidas=0.015)
