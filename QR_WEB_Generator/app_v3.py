import cv2
import numpy as np
import streamlit as st
from camera_input_live import camera_input_live
import pandas as pd
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from datetime import datetime

path = Path(__file__).parents[0] / 'PersonasAllowed.csv'
df = pd.read_csv(path ,delimiter=';')

image = camera_input_live()

if image is not None:
    st.image(image)
    bytes_data = image.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    detector = cv2.QRCodeDetector()

    data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)

    if data:
        parsed_url = urlparse(data)
        query_params = parse_qs(parsed_url.query)

        # Extraer el RUN del diccionario de parámetros de consulta
        run = query_params.get('RUN', [None])[0]

        st.write("# Found QR code")
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