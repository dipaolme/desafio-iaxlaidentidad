#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 16:58:38 2022

@author: mcerdeiro
"""
import json
import os
import re
import warnings

# bibliotecas
import cv2
import jamspell
import numpy as np
import pandas as pd
import pytesseract

# directorios
path_in = 'input_data/'
path_out = 'out_data/'


# funciones de preprocesamiento
def preprocesamiento(img) -> np.ndarray:
    # with open(img, 'r') as f:
    m = cv2.imread(img)
    m = cv2.cvtColor(m, cv2.COLOR_BGR2GRAY)
    return m


# funciones de transcripción
def ocr_tesseract(filename, path_in):
    """
    Aplica el algoritmo de OCR a la imagen pasada por parámetro.

    :param filename: nombre del archivo.
    :param path_in: directorio donde se encuentra el archivo.
    :return: string con el texto leído de la imagen o None si no pudo procesarse.
    """
    preprocessed_img = preprocesamiento(path_in + filename)
    if isinstance(preprocessed_img, np.ndarray):
        custom_config = r'-c tessedit_char_whitelist="AÁBCDEÉFGHIÍJKLMNÑOÓPQRSTUÚVWXYZaábcdeéfghiíjklmnñoópqrstuúvwxyz0123456789 -_/.,:;()"'
        text = str(pytesseract.image_to_string(preprocessed_img, lang="spa", config=custom_config))
        return text

    warnings.warn("Could not process OCR in", path_in + filename)
    return None


# funciones de corrección del texto
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


def es_basura(text):
    """
    Determina como basura si todos las palabras del texto tienen menos de 3 caracteres.
    """
    return all(len(x) < 3 for x in text.split(' '))


def postprocesamiento(text, corrector):
    """
    Transforma el string crudo en texto: une los saltos de línea (unificando las palabras que se cortan al final de la
    línea), filtra los caracteres válidos y aplica el corrector ortográfico.

    :param text: String a postprocesar.
    :param corrector: Corrector ortográfico JamSpell.
    :return: Texto postprocesado.
    """
    text = os.linesep.join([s for s in text.splitlines() if s])
    text = os.linesep.join([s for s in text.splitlines() if not es_basura(s)])
    text = unir_saltos_linea(text)
    # text = spellcheck(corrector, text)
    # text = unir_saltos_linea(text) # por qué otra vez?
    text = filtrar_simbolosvalidos(text)
    # text = text.lower() # por qué?
    text = spellcheck(corrector, text)  # por qué otra vez?
    # text = text.lower()
    return text


# funciones de chequeo de las transcripciones
def palabras_desconocidas(texto, corrector):
    """
    Calcula la cantidad de palabras desconocidas para el corrector del texto.

    :param texto: string.
    :param corrector: Corrector ortográfico JamSpell.
    """
    cantidad = 0
    for palabra in texto.split():
        cantidad += 0 if corrector.WordIsKnown(palabra) else 1
    return cantidad


def procesar_imgs(path_in, path_out, modelo_corrector='herramientas/model_juridico.bin'):
    """
    Procesa los archivos '.tif' de 'path_in' con un OCR, aplica un corrector ortográfico, cuenta la proporción de
    palabras desconocidas y los exporta a formato json con toda la noticia como "Cuerpo".
    Además, guarda en 'reporte.csv' la proporción de palabras desconocidas en la imagen.

    :param path_in: directorio de donde tomar las imágenes.
    :param path_out: directorio adonde se guardan los JSON y el CSV de reporte.
    :param modelo_corrector: path del modelo del corrector ortográfico.
    """
    corrector = inicializar_corrector(modelo_corrector)
    data = []
    for filename in os.listdir(path_in):
        if os.path.splitext(filename)[1] == '.tif':
            print(f'Procesando la imagen: {filename}.\n----------')
            texto = ocr_tesseract(filename, path_in)
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
    print(f'Procesamiento finalizado. Los resultados fueron guardados en el directorio: {path_out}.')
