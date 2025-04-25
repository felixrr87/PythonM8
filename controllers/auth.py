import streamlit as st

def login():
    # --- Título centrado ---
    st.markdown('<h2 class="login-title">🔐 Acceso a la Plataforma</h2>', unsafe_allow_html=True)
    
    # --- Campos de login ---
    usuario = st.text_input("Usuario", key="user_input", placeholder="admin")
    contrasena = st.text_input("Contraseña", type="password", key="pass_input", placeholder="admin")
    
    # --- Botones en columnas ---
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Iniciar sesión", type="primary"):
            if usuario == "admin" and contrasena == "admin":
                st.session_state.authenticated = True
                st.session_state.username = usuario
                st.success(f"¡Bienvenido, {usuario}!")
                st.rerun()
            else:
                st.error("Credenciales incorrectas", icon="⚠️")
    with col2:
        if st.button("Limpiar", type="secondary"):
            st.rerun()