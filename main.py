import streamlit as st
import ffmpeg
import os

# Carpetas de entrada y salida
INPUT_FOLDER = 'videos/input/'
OUTPUT_FOLDER = 'videos/output/'

# Creamos la carpeta de salida si no existe
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Resoluciones y tasas de bits predeterminadas para la encoding ladder
DEFAULT_LADDER = [
    {"resolution": "1920x1080", "bitrate": "8M"},
    {"resolution": "1280x720", "bitrate": "4M"},
    {"resolution": "854x480", "bitrate": "2M"},
    {"resolution": "640x360", "bitrate": "1M"}
]

# Función para convertir video a diferentes códecs
def convert_video(input_file, codecs, progress_bar, task_progress):
    for idx, (codec_name, codec) in enumerate(codecs.items()):
        output_file = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(input_file)[0]}_{codec_name}.mkv")
        try:
            task_progress.progress(0)
            (
                ffmpeg
                .input(os.path.join(INPUT_FOLDER, input_file))
                .output(output_file, vcodec=codec, crf=28)
                .run(overwrite_output=True)
            )
            task_progress.progress(100)
            progress_bar.progress((idx + 1) / len(codecs))
        except ffmpeg.Error as e:
            st.error(f"Error al convertir a {codec_name}: {e.stderr.decode()}")

# Función para crear la encoding ladder (varias versiones con diferentes resoluciones y tasas de bits)
def encode_ladder(input_file, selected_ladder, progress_bar, task_progress):
    total_tasks = len(selected_ladder)
    for idx, config in enumerate(selected_ladder):
        resolution = config["resolution"]
        bitrate = config["bitrate"]
        output_file = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(input_file)[0]}_{resolution}_{bitrate}.mp4")
        try:
            task_progress.progress(0)
            (
                ffmpeg
                .input(os.path.join(INPUT_FOLDER, input_file))
                .output(output_file, vcodec='libx264', video_bitrate=bitrate, s=resolution)
                .run(overwrite_output=True)
            )
            task_progress.progress(100)
            progress_bar.progress((idx + 1) / total_tasks)
        except ffmpeg.Error as e:
            st.error(f"Error al generar la versión: {e.stderr.decode()}")

# Interfaz de usuario con Streamlit
def main():
    st.set_page_config(page_title="Conversor de Video", page_icon=":movie_camera:", layout="wide")

    # Esto es para centrar el logo
    col1, col2, col3 = st.columns([1, 2, 4])
    with col3:
        st.image("logo.png", width=150)

    # Título
    st.markdown("<h1 style='text-align: center;'>Conversor de Video API</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Convierte videos a múltiples códecs y crea una encoding ladder</h3>", unsafe_allow_html=True)

    # Descripción del proyecto
    st.markdown("""
        <div style='text-align: center;'>
            Bienvenido a nuestro conversor de video. Aquí podrás convertir tus videos a los códecs VP8, VP9 y H.265, 
            además de generar una *encoding ladder* con las diferentes resoluciones y tasas de bits que desees.
        </div>
    """, unsafe_allow_html=True)

    # Subimos el archivo de video
    uploaded_file = st.file_uploader("Sube tu video", type=["mp4", "mkv", "avi"])

    if uploaded_file is not None:
        # Guardamos el archivo subido en la carpeta de entrada
        input_file_path = os.path.join(INPUT_FOLDER, uploaded_file.name)
        with open(input_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write(f"Has subido el archivo: {uploaded_file.name}")

        # Seleccionamos los códecs a los que convertir el video
        codecs = {
            'vp8': 'libvpx',
            'vp9': 'libvpx-vp9',
            'h265': 'libx265',
        }

        selected_codecs = st.multiselect(
            "Selecciona los códecs a los que deseas convertir el video",
            options=list(codecs.keys()),
            default=list(codecs.keys())
        )

        # Seleccionamos resoluciones y tasas de bits para la encoding ladder
        resolutions = ['1920x1080', '1280x720', '854x480', '640x360']
        bitrates = ['8M', '4M', '2M', '1M']

        selected_resolutions = st.multiselect(
            "Selecciona las resoluciones para la encoding ladder",
            options=resolutions,
            default=resolutions
        )

        selected_bitrates = st.multiselect(
            "Selecciona las tasas de bits para la encoding ladder",
            options=bitrates,
            default=bitrates
        )

        # Creamos la encoding ladder con las selecciones del usuario
        selected_ladder = [
            {"resolution": res, "bitrate": bit}
            for res in selected_resolutions
            for bit in selected_bitrates
        ]

        # Botón para iniciar la conversión
        if st.button("Iniciar conversión"):
            st.write("Iniciando la conversión...")

            # Barra de progreso general
            progress_bar = st.progress(0)
            task_progress = st.progress(0)

            # Convertimos a los códecs seleccionados
            if selected_codecs:
                convert_video(uploaded_file.name, {codec_name: codecs[codec_name] for codec_name in selected_codecs}, progress_bar, task_progress)

            # Generamos la encoding ladder con las resoluciones y tasas de bits seleccionadas
            if selected_ladder:
                encode_ladder(uploaded_file.name, selected_ladder, progress_bar, task_progress)

            st.write("Conversión completada. Los archivos generados están en la carpeta de salida.")

            # Descargamos los archivos convertidos
            files = os.listdir(OUTPUT_FOLDER)
            for file in files:
                if file.endswith(('.mkv', '.mp4')):
                    st.download_button(
                        label=f"Descargar {file}",
                        data=open(os.path.join(OUTPUT_FOLDER, file), "rb"),
                        file_name=file
                    )

if __name__ == "__main__":
    main()