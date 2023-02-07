#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 10:29:36 2023

@author: mcerdeiro
"""

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