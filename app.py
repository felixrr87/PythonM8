import streamlit as st
from controllers.auth import login
import _pages.inicio as inicio
import _pages.analitica as analitica
import _pages.reportes as reportes

def main():
    # --- Configuración inicial de la página ---
    st.set_page_config(
        page_title="Plataforma Deportiva",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="expanded"  # Barra lateral siempre abierta por defecto
    )
    # --- Estado de sesión ---
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    # --- Sistema de login ---
    if not st.session_state.authenticated:
        login()
    else:
        # --- Barra lateral de navegación --- 
        with st.sidebar:
            st.markdown(f"### 👋 Hola, {st.session_state.username}")
            st.markdown("---")
            if st.button("🚪 Cerrar sesión", type="primary"):
                st.session_state.clear()
                st.rerun()

            # Menú de navegación con estilo
            page = st.radio(
                "Navegación",
                options=["🏠 Inicio", "📊 Analítica", "📈 Reportes"],
                label_visibility="collapsed"
            )

        # --- Sistema de rutas para cambiar de página ---
        if page == "🏠 Inicio":
            inicio.show()
        elif page == "📊 Analítica":
            analitica.show()
        elif page == "📈 Reportes":
            reportes.show()

if __name__ == "__main__":
    main()
