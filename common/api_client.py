import requests
import streamlit as st

@st.cache_data(ttl=3600, show_spinner="Obteniendo datos de la API...")
def get_api_data(url):
    """
    Obtiene datos de una API externa con caché.
    Los datos se mantienen en caché por 1 hora (3600 segundos).
    Muestra un spinner durante la carga.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza error para respuestas no exitosas
        
        # Verificar si la respuesta contiene datos
        if not response.content:
            st.warning("La API respondió sin datos")
            return None
            
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la API: {e}")
        return None
    except ValueError as e:
        st.error(f"Error al decodificar JSON: {e}")
        return None