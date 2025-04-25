import streamlit as st
from common.database import get_sport_data
from common.api_client import get_api_data
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
from datetime import datetime
import pandas as pd
from io import BytesIO
import os

def guardar_pdf(pdf, nombre_base):
    if not os.path.exists("pdfs"):
        os.makedirs("pdfs")
    nombre_archivo = f"{nombre_base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    ruta = os.path.join("pdfs", nombre_archivo)
    pdf.output(ruta)
    return ruta, nombre_archivo

def fig_to_img(fig):
    img_stream = BytesIO()
    fig.savefig(img_stream, format='png', bbox_inches='tight')
    img_stream.seek(0)
    return img_stream

def show():
    st.title("⚽ Análisis Deportivo Avanzado")

    st.sidebar.header("⚙️ Filtros y Opciones")
    option = st.sidebar.selectbox("Elige la fuente de los datos", ("Base de Datos", "API"))

    if option == "Base de Datos":
        st.subheader("📊 Datos desde la Base de Datos")
        db_data = get_sport_data()
        st.dataframe(db_data[["name", "goals"]], height=200, use_container_width=True, hide_index=True)

        # Gráfico 1 - Barras
        st.subheader("🏟️ Goles por Jugador")
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        bars = ax1.bar(db_data['name'], db_data['goals'], color=sns.color_palette("coolwarm", len(db_data)))
        ax1.set_title("Distribución de Goles por Jugador")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig1)

        # Gráfico 2 - Línea
        st.subheader("📈 Tendencia de Goles por Jugador")
        db_data_sorted = db_data.sort_values(by='goals', ascending=True)
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        ax2.plot(db_data_sorted['name'], db_data_sorted['goals'], marker='o', linestyle='-')
        ax2.set_title("Tendencia de Goles por Jugador")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig2)

        # Gráfico 3 - Pastel
        st.subheader("🔵 Distribución de Goles")
        fig3, ax3 = plt.subplots(figsize=(8, 8))
        ax3.pie(db_data['goals'], labels=db_data['name'], autopct='%1.1f%%', startangle=90)
        ax3.set_title("Distribución de Goles por Jugador")
        st.pyplot(fig3)


        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        st.subheader("📤 Exportar a PDF")
        if st.button("Exportar a PDF", key="export_pdf", help="Genera un reporte en formato PDF con todos los gráficos"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Reporte Deportivo - Jugadores y Goles", ln=1, align='C')
            pdf.ln(10)

            pdf.set_font("Arial", 'B', 12)
            pdf.cell(80, 10, txt="Jugador", border=1, align='C')
            pdf.cell(30, 10, txt="Goles", border=1, align='C')
            pdf.ln()
            pdf.set_font("Arial", size=10)
            for _, row in db_data.iterrows():
                pdf.cell(80, 10, txt=row['name'], border=1)
                pdf.cell(30, 10, txt=str(row['goals']), border=1, align='C')
                pdf.ln()

            for fig in [fig1, fig2, fig3,]:
                img_stream = fig_to_img(fig)
                pdf.image(img_stream, x=10, w=180)

            ruta, nombre_archivo = guardar_pdf(pdf, "reporte_jugadores")
            with open(ruta, "rb") as f:
                st.download_button("Descargar PDF", data=f, file_name=nombre_archivo, mime="application/pdf")
            st.success("¡PDF generado con todos los gráficos!")

        # Agregar botón de imprimir 
        st.markdown("""
            <div style="margin-top: 10px;">
                <button onclick="window.print()" style="background-color:#6200ea; color:white; border-radius:5px; padding: 10px; font-size: 16px; border:none;">Imprimir</button>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    elif option == "API":
        st.subheader("🌐 Datos de la Premier League")
        available_seasons = {
            "2019-20": "https://raw.githubusercontent.com/openfootball/football.json/master/2019-20/en.1.json",
            "2020-21": "https://raw.githubusercontent.com/openfootball/football.json/master/2020-21/en.1.json",
            "2021-22": "https://raw.githubusercontent.com/openfootball/football.json/master/2021-22/en.1.json"
        }
        selected_seasons = st.sidebar.multiselect("Selecciona temporadas", list(available_seasons.keys()), default=["2020-21"])

        all_matches = []
        for season in selected_seasons:
            api_data = get_api_data(available_seasons[season])
            if api_data and "matches" in api_data:
                for match in api_data["matches"]:
                    match["season"] = season
                    all_matches.append(match)

        if not all_matches:
            st.warning("No hay partidos disponibles para las temporadas seleccionadas.")
            return

        teams = sorted({match["team1"] for match in all_matches} | {match["team2"] for match in all_matches})
        selected_teams = st.sidebar.multiselect("Filtrar por equipos", teams)
        min_goals = st.sidebar.slider("Goles mínimos por partido", 0, 10, 3)

        processed_matches = []
        for match in all_matches:
            ft_score = match.get("score", {}).get("ft", [0, 0])
            total_goals = int(ft_score[0]) + int(ft_score[1])
            if selected_teams and (match["team1"] not in selected_teams and match["team2"] not in selected_teams):
                continue
            if total_goals < min_goals:
                continue
            processed_matches.append({
                "Temporada": match["season"],
                "Fecha": match["date"],
                "Local": match["team1"],
                "Visitante": match["team2"],
                "Resultado": f"{ft_score[0]} - {ft_score[1]}",
                "Goles Totales": total_goals
            })

        df = pd.DataFrame(processed_matches)
        st.dataframe(df, use_container_width=True)

        # Gráfico 1 - Barras
        st.subheader("📈 Partidos por Goles")
        fig_api1, ax_api1 = plt.subplots(figsize=(12, 6))
        labels = [f"{m['Fecha']}\n{m['Local']} vs {m['Visitante']}" for m in processed_matches[:20]]
        goals = [m["Goles Totales"] for m in processed_matches[:20]]
        bars = ax_api1.bar(labels, goals, color='tab:orange')
        ax_api1.set_title("Goles por Partido")
        plt.xticks(rotation=90, ha='right')
        st.pyplot(fig_api1)

        # Gráfico 2 - Pastel
        st.subheader("🔵 Distribución de Goles por Equipo")
        goles_por_equipo = {}
        for match in processed_matches:
            local = match["Local"]
            visitante = match["Visitante"]
            resultado = match["Resultado"]
            goles_local, goles_visitante = map(int, resultado.split(" - "))
            goles_por_equipo[local] = goles_por_equipo.get(local, 0) + goles_local
            goles_por_equipo[visitante] = goles_por_equipo.get(visitante, 0) + goles_visitante

        fig_api2, ax_api2 = plt.subplots(figsize=(8, 8))
        ax_api2.pie(list(goles_por_equipo.values()), labels=list(goles_por_equipo.keys()), autopct='%1.1f%%', startangle=90)
        ax_api2.set_title("Distribución de Goles por Equipo")
        st.pyplot(fig_api2)


        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        st.subheader("📤 Exportar a PDF")
        if st.button("Exportar a PDF", key="export_api_pdf"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Reporte de la Premier League", ln=1, align='C')
            pdf.ln(10)

            pdf.set_font("Arial", 'B', 12)
            pdf.cell(80, 10, txt="Fecha", border=1, align='C')
            pdf.cell(50, 10, txt="Local", border=1, align='C')
            pdf.cell(50, 10, txt="Visitante", border=1, align='C')
            pdf.cell(30, 10, txt="Goles Totales", border=1, align='C')
            pdf.ln()

            pdf.set_font("Arial", size=10)
            for match in processed_matches:
                pdf.cell(80, 10, txt=match['Fecha'], border=1)
                pdf.cell(50, 10, txt=match['Local'], border=1)
                pdf.cell(50, 10, txt=match['Visitante'], border=1)
                pdf.cell(30, 10, txt=str(match['Goles Totales']), border=1, align='C')
                pdf.ln()

            for fig in [fig_api1, fig_api2,]:
                img_stream = fig_to_img(fig)
                pdf.image(img_stream, x=10, w=180)

            ruta, nombre_archivo = guardar_pdf(pdf, "reporte_premier_league")
            with open(ruta, "rb") as f:
                st.download_button("Descargar PDF", data=f, file_name=nombre_archivo, mime="application/pdf")
            st.success("¡PDF generado con todos los gráficos!")

        # Agregar botón de imprimir
        st.markdown("""
            <div style="margin-top: 10px;">
                <button onclick="window.print()" style="background-color:#6200ea; color:white; border-radius:5px; padding: 10px; font-size: 16px; border:none;">Imprimir</button>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
