import streamlit as st
import os

def show():
    st.markdown('<h1 class="report-title">📁 Reportes Generados</h1>', unsafe_allow_html=True)

    carpeta = "pdfs"
    if not os.path.exists(carpeta):
        st.warning("No se han generado reportes todavía.")
        return

    archivos = [f for f in os.listdir(carpeta) if f.endswith(".pdf")]

    if not archivos:
        st.info("No hay archivos PDF generados aún.")
        return

    st.write(f"📝 Se encontraron **{len(archivos)}** reportes:")

    # Crear una lista de checkboxes para seleccionar archivos
    archivos_seleccionados = []
    for archivo in archivos:
        checkbox = st.checkbox(f"Eliminar {archivo}", key=archivo)
        if checkbox:
            archivos_seleccionados.append(archivo)

        ruta = os.path.join(carpeta, archivo)
        with open(ruta, "rb") as f:
            st.download_button(
                label=f"📥 Descargar {archivo}",
                data=f,
                file_name=archivo,
                mime="application/pdf",
                use_container_width=True
            )

    if st.button("🗑️ Borrar los reportes seleccionados", key="delete_button"):
        if archivos_seleccionados:
            for archivo in archivos_seleccionados:
                os.remove(os.path.join(carpeta, archivo))
            st.success(f"Se han eliminado los reportes: {', '.join(archivos_seleccionados)}.")
            st.rerun()  # Actualiza la página para reflejar los cambios
        else:
            st.warning("No has seleccionado ningún archivo para eliminar.")
