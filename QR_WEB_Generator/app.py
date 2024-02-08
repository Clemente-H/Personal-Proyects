import streamlit as st
import re
import qrcode
from PIL import Image
from io import BytesIO

# Título de la aplicación
st.title('QR Personal Info')

# Campo de texto para entrada de usuario
user = st.text_input('Ingrese Nombre')
# Campo de texto para entrada de correo electrónico
email_usuario = st.text_input('Ingrese dirección de correo electrónico')

# Función para validar el correo electrónico
def validar_email(email):
    # Expresión regular para validar un correo electrónico
    regex = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    if re.match(regex, email):
        return True
    else:
        return False

# Botón para validar el correo electrónico
if st.button('Generar QR'):
    # Validar el correo electrónico ingresado
    if validar_email(email_usuario):
        user_info = {'Nombre':user, 'email':email_usuario}
        img = qrcode.make(user_info)
        # Convertir la imagen PIL a bytes
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_bytes = buffer.getvalue()
        st.success('El correo electrónico es válido.')
        st.image(qr_bytes, caption='Código QR de Clemente')
    else:
        st.error('El correo electrónico no es válido. Por favor, ingresa una dirección de correo válida.')

