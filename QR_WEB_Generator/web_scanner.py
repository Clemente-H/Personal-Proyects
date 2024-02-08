import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import streamlit_authenticator as stauth
import pandas as pd
df = pd.read_csv('../../PersonasAllowed.csv',delimiter=';')
qr_code = qrcode_scanner(key='qrcode_scanner')

if qr_code:
    st.write(qr_code)
    url = qr_code
    # Analizar la URL y extraer los parámetros de consulta
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Extraer el RUN del diccionario de parámetros de consulta
    run = query_params.get('RUN', [None])[0]

    # Mostrar el RUN
    # print("RUN:", run)
    # st.write(run)
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


