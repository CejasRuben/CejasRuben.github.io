"""
Este script automatiza la subida de archivos HTML y CSS a GitHub desde Termux.

Qué hace:
1. Agrega los archivos .html y .css al área de preparación (git add).
2. Crea un commit con un mensaje que incluye fecha y hora.
3. Hace push de los cambios al repositorio remoto en GitHub.
4. Muestra mensajes claros de éxito o error.

Comandos para usarlo:
- Guarda este archivo como subir_html_css.py
- Ejecútalo en Termux con:
    python subir_html_css.py
"""

import subprocess
import datetime
import sys

def run_command(command, error_message):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        if result.stdout.strip():
            print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"{error_message}\nDetalles: {e.stderr.strip() if e.stderr else e}")
        sys.exit(1)

def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Actualización de archivos HTML y CSS - {timestamp}"

    print("➤ Agregando archivos HTML y CSS...")
    # Agregar archivos HTML y CSS
    run_command(["git", "add", "*.html", "*.css"], "Error al agregar los archivos HTML y CSS.")

    print("➤ Creando commit...")
    run_command(["git", "commit", "-m", commit_message], "Error al crear el commit (¿quizás no hubo cambios?).")

    print("➤ Haciendo push al repositorio...")
    run_command(["git", "push"], "Error al hacer push al repositorio remoto.")

    print("✔ Operación completada con éxito.")

if __name__ == "__main__":
    main()
