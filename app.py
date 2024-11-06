import base64
from io import BytesIO
from PIL import Image  # Cambia esta línea
import streamlit as st
import google.generativeai as genai
import os

# Directorio donde se guardarán los archivos
upload_dir = "uploads"

# Crear el directorio si no existe
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir, mode=0o755)  # Permisos 755 (rwxr-xr-x)

# Try to import GEMINI_API_KEY from config, but don't fail if it's not available
try:
    from config import GEMINI_API_KEY
except ImportError:
    # If config.py is not available, try to get the API key from environment variable
    GEMINI_API_KEY = os.getenv("AIzaSyDOMI3iuGgkiBIxY-prmD9O9Z1ED2A7jOA")

    if GEMINI_API_KEY is None:
        # If environment variable is not set, use a default value
        print("Warning: GEMINI_API_KEY not found in config or environment variables. Using default value.")
        GEMINI_API_KEY = "your_default_api_key_here"

# Configuración del modelo
genai.configure(api_key="AIzaSyDOMI3iuGgkiBIxY-prmD9O9Z1ED2A7jOA")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Configuración del tema
st.set_page_config(
    page_title="E-WASTE",
    page_icon="Logo 2.jpeg",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Añade esta función al principio del archivo, después de las importaciones
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# Cargar y mostrar el logo
logo = Image.open("Logo 2.jpeg")  # Reemplaza con la ruta real de tu logo
st.markdown(
    """
    <style>
    .logo-container {
        position: absolute;
        margin-top: 15px;
        margin-left: 700px;
        z-index: 500;
    }
    .logo-image {
        border-radius: 50%;
        box-shadow: 0 0 15px #06be17;
        width: 200px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    f"""
    <div class="logo-container">
        <img src="data:image/jpeg;base64,{image_to_base64(logo)}" class="logo-image" width="100">
    </div>
    """,
    unsafe_allow_html=True
)

 # Aplicar un tema personalizado
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, rgb(10,30,40) 0%, rgb(15,20,50) 50%, rgb(5,3,30) 100%);
    }
    .stButton>button {
        background-color: #06be17;
        color: white;
    }
    body {
        color: #06be17;
    }
    h1, h2, h3 {
        color: #06be17;
        text-shadow: 0 0 1px #06be17, 0 0 2px #06be17;
        animation: subtle-neon 3s ease-in-out infinite alternate;
    }
    @keyframes subtle-neon {
        from {
            text-shadow: 0 0 1px #06be17, 0 0 2px #06be17;
        }
        to {
            text-shadow: 0 0 2px #06be17, 0 0 3px #06be17, 0 0 4px #06be17;
        }
    }
    .stSelectbox label {
        color: #b0e0e6;
    }
    /* Ajuste adicional para mejorar la legibilidad */
    .stMarkdown {
        color: #ffffff;
    }
    /* Estilos para los inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background: linear-gradient(135deg, rgb(10,30,40) 0%, rgb(15,20,50) 50%, rgb(5,3,30) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        color: white !important;
    }
    .stTextInput>label, .stSelectbox>label {
        color: white !important;
    }
    /* Ajuste para el texto del selectbox */
    .stSelectbox>div>div>div>div {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_component_info(component_name):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(f"Describe en español cómo extraer el {component_name} de una placa de circuito. La respuesta debe ser detallada y fácil de entender para un principiante.")
    return response.text

def main():
    st.title("E-WASTE")
    
    stage = st.session_state.get('stage', 1)
    
    if stage == 1:
        st.header("Etapa 1: Identificación del Componente")
        component = st.selectbox("Selecciona un componente", ["conductor", "condensador", "puerto USB", "luces led", "circuito integrado", "resistencia", "capacitador", "microcontrolador", "puerto ethernet", "puerto de alimentación", "puerto cable", "semiconductor"])

        if st.button("Siguiente"):
            st.session_state['component_name'] = component
            st.session_state['stage'] = 2
            st.rerun()
    
    elif stage == 2:
        st.header("Etapa 2: Extracción del Componente")
        component_name = st.session_state.get('component_name', '')
        if component_name:
            st.write(f"Componente: {component_name}")
            info = get_component_info(component_name)
            st.markdown(info)  # Cambiado de st.write a st.markdown para mejor formato
        
            st.video("Video de extracción de componentes.mp4")  # Replace with actual video URL
            st.write("Lista de herramientas necesarias:")
            st.write("- Fuente de calor o cautín")
            st.write("- Estaño")
            st.write("- Pasta de soldar")
            st.write("- Pasta Flux")
            if st.button("¡Presiona aquí!"):
                st.write("¡Cada componente es un nuevo desafío y una oportunidad de aprendizaje!")
            if st.button("Regresar a la Etapa 1"):
                st.session_state['stage'] = 1
                st.stop()  # Cambia st.rerun() a st.experimental_rerun()

if __name__ == "__main__":
    main()
