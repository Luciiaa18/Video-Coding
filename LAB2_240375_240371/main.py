import subprocess
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


# Base class for video encoding
class VideoEncoder:
    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = input_path
        self.output_path = output_path

    def encode(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def run_command(self, command):
        try:
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error during conversion: {e.stderr.decode() or str(e)}"
            )


# VP8 Encoder (inherits from VideoEncoder)
class VP8Encoder(VideoEncoder):
    def encode(self):
        command = [
            "ffmpeg",
            "-i", str(self.input_path),
            "-c:v", "libvpx",  # VP8 codec
            "-b:v", "1M",  # Bitrate
            "-c:a", "libvorbis",  # Audio codec
            str(self.output_path)
        ]
        self.run_command(command)


# VP9 Encoder (inherits from VideoEncoder)
class VP9Encoder(VideoEncoder):
    def encode(self):
        command = [
            "ffmpeg",
            "-i", str(self.input_path),
            "-c:v", "libvpx-vp9",  # VP9 codec
            "-b:v", "1M",  # Bitrate
            "-c:a", "libopus",  # Audio codec
            str(self.output_path)
        ]
        self.run_command(command)


# H.265 Encoder (inherits from VideoEncoder)
class H265Encoder(VideoEncoder):
    def encode(self):
        command = [
            "ffmpeg",
            "-i", str(self.input_path),
            "-c:v", "libx265",  # H.265 codec
            "-crf", "28",  # Quality setting
            "-preset", "medium",  # Encoding preset
            "-c:a", "aac",  # Audio codec
            str(self.output_path)
        ]
        self.run_command(command)


# AV1 Encoder (inherits from VideoEncoder)
class AV1Encoder(VideoEncoder):
    def encode(self):
        command = [
            "ffmpeg",
            "-i", str(self.input_path),
            "-c:v", "libaom-av1",  # AV1 codec
            "-crf", "30",  # Quality setting
            "-b:v", "0",  # Variable bitrate
            "-c:a", "libopus",  # Audio codec
            str(self.output_path)
        ]
        self.run_command(command)


# Base model to define input request
class VideoConversionRequest(BaseModel):
    file_path: str
    output_dir: str
    formats: List[str]  # List of formats to convert into


@app.post("/EJERCICIO 1/")
async def convert_video(request: VideoConversionRequest):
    input_path = Path(request.file_path).resolve()
    output_dir = Path(request.output_dir).resolve()
    formats = request.formats

    # Verificamos si el archivo de entrada existe
    if not input_path.exists():
        raise HTTPException(status_code=404, detail="El archivo de entrada no existe.")

    # Verificamos si el directorio de salida existe y si no lo creamos
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

   
    for format in formats:
        
        output_path = output_dir / f"{input_path.stem}_{format}.mp4"

        
        if format == "vp8":
            encoder = VP8Encoder(input_path, output_path)
        elif format == "vp9":
            encoder = VP9Encoder(input_path, output_path)
        elif format == "h265":
            encoder = H265Encoder(input_path, output_path)
        elif format == "av1":
            encoder = AV1Encoder(input_path, output_path)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")

        
        encoder.encode()

    return {
        "message": "Conversión completada exitosamente.",
        "outputs": {format: str(output_dir / f"{input_path.stem}_{format}.mp4") for format in formats}
    }


@app.get("/")
async def root():
    return {"message": "Todo va bien profe."}









