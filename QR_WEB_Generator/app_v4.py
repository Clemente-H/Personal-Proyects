import threading
import cv2
import streamlit as st
from matplotlib import pyplot as plt

from streamlit_webrtc import webrtc_streamer

lock = threading.Lock()
img_container = {"img": None}


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    with lock:
        img_container["img"] = img

    return frame


ctx = webrtc_streamer(key="example", video_frame_callback=video_frame_callback)

fig_place = st.empty()
fig, ax = plt.subplots(1, 1)

while ctx.state.playing:
    with lock:
        img = img_container["img"]
    if img is None:
        continue
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ax.cla()
    ax.hist(gray.ravel(), 256, [0, 256])
    fig_place.pyplot(fig)

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