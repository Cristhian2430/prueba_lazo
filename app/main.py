import os
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator

from src.my_config import get_authenticator
from src.my_bucket import my_storage
from src.my_files import upload_file_school

from dotenv import load_dotenv

load_dotenv()

# Ahora puedes acceder a las variables de entorno como variables normales
CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
BUCKET      = os.getenv("NOMBRE_BUCKET")
ENVIROMENT  = os.getenv("ENVIROMENT")


st.set_page_config(page_title="Colegios Dashboard", page_icon=":bar_chart:", layout="wide")

storage = my_storage(nombre_bucket=BUCKET,env=ENVIROMENT,ruta_credenciales=CREDENTIALS)
authenticator = get_authenticator()
name, authentication_status, username = authenticator.login('Login', 'main')


if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main', key='unique_key')
elif st.session_state["authentication_status"] is False:
    st.error('usuario/contraseña es incorrecto')
elif st.session_state["authentication_status"] is None:
    st.warning('Por favor ingrese correctamente usuario o contraseña')


        
if authentication_status:
    st.write(f'Bienvenido *{st.session_state["name"]}*')
    st.title('Analitica de estudiantes')
    
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Bienvenido {name}")
    
    uploaded_file = st.sidebar.file_uploader('Subir archivo', type=["csv", "xlsx"])
    upload_file_school(uploaded_file,storage)
    
    if os.path.exists("prod.xlsx"):
        
        df = pd.read_excel("prod.xlsx")
        df["Nombre_Completo"] = df["Nombres"] + " " + df["Apellidos"]

        st.sidebar.header("Por favor filtra aqui:")
        grado = st.sidebar.multiselect(
            "Select the Grado:",
            options=df["Grado"].unique(),
            default=df["Grado"].unique()
        )

        seccion = st.sidebar.multiselect(
            "Select the Sección:",
            options=df["Sección"].unique(),
            default=df["Sección"].unique(),
        )

        trimestre = st.sidebar.multiselect(
            "Select the Trimestre:",
            options=df["Trimestre"].unique(),
            default=df["Trimestre"].unique()
        )

        print("Grado:",grado)
        df_selection = df.query(
            "Grado == @grado & Sección ==@seccion & Trimestre == @trimestre"
        )

        st.markdown("##")

        # TOP KPI's
        # Crear una columna combinada de Nombres y Apellidos
        cantidad_alumnos_unicos = df["Nombre_Completo"].nunique()
        
        average_nota = round(df_selection["Nota"].mean(), 1)
        star_nota = ":star:" * int(round(average_nota/4, 0))
        
        average_edad = round(df_selection["Edad"].mean(), 2)

        left_column, middle_column, right_column = st.columns(3)
        with left_column:
            st.subheader("Total Alumnos:")
            st.subheader(f"{cantidad_alumnos_unicos}")
        with middle_column:
            st.subheader("Nota promedio general:")
            st.subheader(f"{average_nota} {star_nota}")
        with right_column:
            st.subheader("Edad promedio general:")
            st.subheader(f"{average_edad} años")

        st.markdown("""---""")
        st.title('Analitica de por Grado')
        
        #######################################
        # Obtener la cantidad de alumnos únicos considerando Nombres y Apellidos
        cantidad_alumnos_unicos = df["Nombre_Completo"].nunique()

        # Crear un DataFrame con la frecuencia de cada cantidad de alumnos únicos
        frecuencia_alumnos = df.groupby("Grado")["Nombre_Completo"].nunique().reset_index()

        # Crear y mostrar el gráfico de distribución de la cantidad de alumnos únicos por grado
        fig_frecuencia_alumnos = px.bar(frecuencia_alumnos, x="Grado", y="Nombre_Completo",
                    title="Distribución de la Cantidad de Alumnos Únicos por Grado")
        
        #######################################
        fig_distribucion_nota = px.box(df, x="Grado", y="Nota", title="Distribución de Notas por Grado")       
        
        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_frecuencia_alumnos, use_container_width=True)
        right_column.plotly_chart(fig_distribucion_nota, use_container_width=True)
        
        #Distribucicon de Edades
        fig_distribucion_edades = px.box(df, x="Grado", y="Nota", title="Distribución de Notas por Grado")       
        
        # Calcular la media de notas por grado y curso
        media_notas = df.groupby(["Grado", "Curso"])["Nota"].mean().reset_index()
        # Crear y mostrar el gráfico de barras apiladas de la media de notas por grado y curso
        fig_media_notas_grado = px.bar(media_notas, x="Grado", y="Nota", color="Curso",
                    title="Media de Notas por Grado y Curso",
                    barmode="group",  # Mostrar barras apiladas por curso
                    )
        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_distribucion_edades, use_container_width=True)
        right_column.plotly_chart(fig_media_notas_grado, use_container_width=True)
        


        # ---- HIDE STREAMLIT STYLE ----
        hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                    </style>
                    """
        st.markdown(hide_st_style, unsafe_allow_html=True)
