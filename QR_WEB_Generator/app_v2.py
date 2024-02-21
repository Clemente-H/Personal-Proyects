import streamlit as st
from qreader import QReader
import cv2
import numpy as np
from camera_input_live import camera_input_live
#Mostrar la opción para tomar una foto con la cámara

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
    decoded_text = qreader.detect_and_decode(image=rgb_image)
    if decoded_text:
        st.success(f"QR Code detected: {decoded_text}")
    else:
        st.error("No QR Code found.")