import streamlit as st
from PIL import Image

def show():
    st.markdown('<h1 class="title">Bienvenido a la Plataforma Deportiva</h1>', unsafe_allow_html=True)

    # Mostrar imagen de bienvenida
    image = Image.open("image.jpg")  # Reemplaza "image.jpg" por la imagen que quieras
    st.image(image, use_container_width=True)

    # Texto explicativo
    st.markdown("""
    <p class="intro-text">
        Usa el <strong>menú lateral izquierdo</strong> para navegar por las diferentes secciones de la aplicación. <br>
        Allí encontrarás páginas como <em>Inicio</em>, <em>Analítica</em> y <em>Reportes</em>. <br>
        Explora los datos deportivos y sácale el máximo partido a la plataforma.
    </p>
    """, unsafe_allow_html=True)

    # Pie de página
    st.markdown('<p class="footer">Desarrollado por Felix Ramirez</p>', unsafe_allow_html=True)
