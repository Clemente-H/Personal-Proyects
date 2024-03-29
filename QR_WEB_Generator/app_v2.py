import streamlit as st
from qreader import QReader
import cv2
import numpy as np
from camera_input_live import camera_input_live
import pandas as pd
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from datetime import datetime
#Mostrar la opción para tomar una foto con la cámara
path = Path(__file__).parents[0] / 'PersonasAllowed.csv'
df = pd.read_csv(path ,delimiter=';')
img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    # Convertir el buffer de la imagen a un array de numpy para OpenCV
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    #st.image(cv2_img, channels="BGR", caption="Captured Image")

    # Crear una instancia de QReader para decodificar el QR
    qreader = QReader()
    # Convertir la imagen a RGB para qreader (si es necesario)
    rgb_image = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    # Usar qreader para detectar y decodificar el QR en la imagen
    data  = qreader.detect_and_decode(image=rgb_image)
    data = data[0]
    if data:
        parsed_url = urlparse(data)
        query_params = parse_qs(parsed_url.query)

        # Extraer el RUN del diccionario de parámetros de consulta
        run = query_params.get('RUN', [None])[0]
 
        #st.write(data)
        if run:
            if df['Rut'].isin([str(run)]).any():

                import streamlit as st
                # Obtener el tiempo actual
                now = datetime.now()
                # Formatear el tiempo como deseas. Aquí estoy usando formato año-mes-día hora:minuto:segundo
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                st.success('Persona con entrada Valida. Ingreso: ' + str(current_time))

            else:
                st.error('Persona con entrada no Valida')