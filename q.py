#!/usr/bin/env python
import os
from datetime import datetime, timedelta
from subprocess import Popen
from PIL import Image

# Configuraciones
START_DATE = datetime(2024, 1, 1)  # Fecha inicial para comenzar los commits
REPO_DIR = "complex_pattern_repo"
IMAGE_PATH = "pattern_52x7.png"  # Ruta de la imagen con el patrón deseado (52x7 píxeles)
USER_NAME = "Git Pattern Generator"
USER_EMAIL = "pattern@example.com"

def main():
    # Crear o inicializar un repositorio temporal
    os.makedirs(REPO_DIR, exist_ok=True)
    os.chdir(REPO_DIR)
    
    if not os.path.exists(".git"):
        run(["git", "init"])
        run(["git", "config", "user.name", USER_NAME])
        run(["git", "config", "user.email", USER_EMAIL])

    # Cargar la imagen y procesar el patrón
    try:
        img = Image.open(IMAGE_PATH)
        img = img.convert("L")  # Convertir a escala de grises
        width, height = img.size

        if width != 52 or height != 7:
            raise ValueError("La imagen debe ser de 52x7 píxeles para ajustarse a la cuadrícula de GitHub.")

        for y in range(height):
            for x in range(width):
                pixel_value = img.getpixel((x, y))
                if pixel_value < 128:  # Píxel oscuro (donde queremos hacer commit)
                    commit_date = START_DATE + timedelta(weeks=x, days=y)
                    create_commit(commit_date)

        print("\nPatrón complejo generado exitosamente en la cuadrícula de contribuciones de GitHub.")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar la imagen en la ruta '{IMAGE_PATH}'")
    except Exception as e:
        print(f"Error inesperado: {e}")

def create_commit(commit_date):
    # Crear/modificar README.md para realizar un commit
    with open("README.md", "a") as file:
        file.write(f"Contribution on {commit_date.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Añadir cambios al índice de Git
    run(["git", "add", "."])

    # Realizar commit con la fecha especificada
    run([
        "git", "commit", "-m", f"Commit on {commit_date.strftime('%Y-%m-%d')}",
        "--date", commit_date.strftime("%Y-%m-%dT%H:%M:%S")
    ])

def run(commands):
    """Ejecuta comandos de sistema"""
    Popen(commands).wait()

if __name__ == "__main__":
    main()
