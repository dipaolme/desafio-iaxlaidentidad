#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 16:58:38 2022

@author: mcerdeiro
"""
#%% librerias


#%% funciones de preprocesamiento
def preprocesamiento(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
#%% funciones de transcripcion
# TODO: limpiar estas funciones!!!!!!

def ocr_tesseract(filename, path_in, path_out):
    img = cv2.imread(path_in+filename)
    preprocessed_img = default_preprocessing(img)
    if isinstance(preprocessed_img, np.ndarray):
        custom_config = r'-c tessedit_char_whitelist="AÁBCDEÉFGHIÍJKLMNÑOÓPQRSTUÚVWXYZaábcdeéfghiíjklmnñoópqrstuúvwxyz0123456789 -_/.,:;"'
        text = str(((pytesseract.image_to_string(preprocessed_img,lang="spa", config=custom_config))))
        with open(str(path_out+filename), "wb") as f:
            f.write(text.encode("utf-8"))
        filename.unlink()
    return text


def ocr_file(PDF_file, carpeta_salida, carpeta_tmp, carpeta_txts, carpeta_tesseract, carpeta_kodak, corrector):

    texto = ocr_tesseract(PDF_file, tesseract_path, tmp_path)
    ocr_kodak(PDF_file, kodak_path)

    texto = default_postprocessing(rawtext, corrector)
    filename = txt_path / f"{clave}.txt"
    with open(str(filename), "wb") as text_file:
        text_file.write(texto.encode("utf-8"))
    pd = ocr_quality.unknown_words(texto, corrector) / len(texto.split())
    difs = ocr_quality.kodak_tesseract_comparison(clave, tesseract_path, kodak_path, corrector)

    return clave, pd, difs    
    
def ocr_files(carpeta_pdfs, archivo_salida, salida, tmp, txts, tesseract, kodak, umbral_palabrasdesconocidas, umbral_diferenciaocr, reporte, modelo_jamspell):
    pdfs_path = Path(carpeta_pdfs)
    for carpeta in pdfs_path.iterdir():
        print(f'Directorio {carpeta.name}')
        carpeta_salida = carpeta / Path(salida)
        carpeta_tmp = carpeta / Path(tmp)
        carpeta_txts = carpeta / Path(txts)
        carpeta_tesseract = carpeta / Path(tesseract)
        carpeta_kodak = carpeta / Path(kodak)
        data = []
        pdf_files = list(carpeta.rglob('*.pdf'))
        print(f'Total de archivos: {len(pdf_files)}')
        n_archivo = 1
        corrector = ocr_postprocessing.inicializar_corrector(modelo_jamspell)
        print('Archivos procesados:')
        for pdf in pdf_files:
            print(f'{n_archivo} archivo: {str(pdf)}')
            try:
                clave, palabras_desconocidas, diferencias_ocr = ocr_file(pdf, carpeta_salida, carpeta_tmp, carpeta_txts, carpeta_tesseract, carpeta_kodak, corrector)
                data.append({'DICTAMEN': clave, 'PALABRAS DESCONOCIDAS': palabras_desconocidas, 'DIFERENCIA CON KODAK': diferencias_ocr})
            except Exception:
                print("No se pudo procesar el archivo")
            n_archivo += 1
        if data:
            print('Generando reporte')
            ocr_quality.thersholds_check(pd.DataFrame(data), archivo_salida, umbral_palabrasdesconocidas, umbral_diferenciaocr, reporte)
        print(f"Reporte de procesamiento: {archivo_salida}")
        print(f"Archivos de texto procesados: {str(carpeta_salida / carpeta_txts)}")

    
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

def default_postprocessing(text, corrector):
    # The recognized text is stored in variable text
    # Any string processing may be applied on text
    # Here, basic formatting has been done:
    # In many PDFs, at line ending, if a word can't
    # be written fully, a 'hyphen' is added.
    # The rest of the word is written in the next line
    # Eg: This is a sample text this word here GeeksF-
    # orGeeks is half on first line, remaining on next.
    # To remove this, we replace every '-\n' to ''.
    text = os.linesep.join([s for s in text.splitlines() if s])
    text = os.linesep.join([s for s in text.splitlines() if not es_basura(s)])
    text = unir_saltos_linea(text)    
    text = spellcheck(corrector, text)    
    text = unir_saltos_linea(text) # por qué otra vez?
    text = filtrar_simbolosvalidos(text)
    text = text.lower() # por qué?
    text = spellcheck(corrector, text) # por qué otra vez?
    text = text.lower()
    return text    
    
#%% funciones de chequeo de las transcripciones    
def chequeo_calidad:
    
    
    
#%% 