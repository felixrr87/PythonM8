import sqlite3
import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600, show_spinner="Cargando datos de jugadores...")
def get_sport_data():
    """
    Obtiene datos de jugadores desde la base de datos SQLite con caché.
    Los datos se mantienen en caché por 1 hora (3600 segundos).
    """
    # Verifica la ruta correcta a tu base de datos
    conn = sqlite3.connect('data/sports.db')
    
    # Consulta SQL para obtener los datos
    query = 'SELECT name, goals FROM players'
    
    try:
        # Leer los datos usando pandas
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"Error al leer la base de datos: {e}")
        df = pd.DataFrame(columns=['name', 'goals'])  # Devuelve DataFrame vacío para evitar errores
    finally:
        # Asegurarse de cerrar la conexión
        conn.close()
    
    return df