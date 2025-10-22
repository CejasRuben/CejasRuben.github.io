"""
Este script automatiza la subida de archivos HTML y CSS a GitHub desde Termux.

Qué hace:
1. Agrega solo archivos .html y .css al área de preparación.
2. Crea un commit con un mensaje que incluye fecha y hora.
3. Hace push de los cambios al repositorio remoto en GitHub.
4. Muestra la URL probable de tu sitio de GitHub Pages.
"""

import subprocess
import datetime
import sys

def run_command(command, error_message):
    """Ejecuta un comando de shell y maneja posibles errores."""
    try:
        # check=True lanzará una excepción si el comando falla
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        if result.stdout.strip():
            # Muestra la salida del comando si existe (ej. lista de archivos commitados)
            print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: {error_message}\nDetalles: {e.stderr.strip() if e.stderr else e}")
        # Salir del script si el comando falla
        sys.exit(1)
    except FileNotFoundError:
        print("❌ ERROR: El comando 'git' no se encontró. Asegúrate de que Git esté instalado y en el PATH.")
        sys.exit(1)

def get_repo_name():
    """Intenta obtener el nombre del repositorio para construir la URL de GitHub Pages."""
    try:
        # Obtiene la URL remota de 'origin'
        result = subprocess.run(["git", "config", "--get", "remote.origin.url"], 
                                check=True, text=True, capture_output=True)
        
        url = result.stdout.strip()
        
        # Limpiamos la URL para obtener solo el nombre del repositorio
        repo_part = url.split('/')[-1].replace(".git", "")
        
        # Retornamos el nombre del repo (ej: CejasRuben.github.io)
        return repo_part
            
    except Exception:
        # En caso de error (no es un repositorio git, no hay remote, etc.)
        return None

def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Actualización de archivos HTML y CSS - {timestamp}"

    # Paso 1: Agregar solo archivos HTML y CSS
    print("\n➤ Agregando archivos HTML y CSS al control de versiones...")
    run_command(["git", "add", "*.html", "*.css"], "Fallo al agregar los archivos HTML y CSS.")

    # Paso 2: Crear commit
    print("\n➤ Creando commit...")
    run_command(["git", "commit", "-m", commit_message], "Fallo al crear el commit (puede que no haya cambios nuevos en HTML/CSS).")

    # Paso 3: Hacer push
    print("\n➤ Iniciando push al repositorio remoto...")
    run_command(["git", "push"], "Fallo al subir los cambios (push) al repositorio remoto.")

    print("\n" + "=" * 40)
    print("✔ ¡OPERACIÓN DE SUBIDA COMPLETADA CON ÉXITO!")
    
    # Paso 4: Mostrar la URL de GitHub Pages
    repo_name = get_repo_name()
    if repo_name and ".github.io" in repo_name:
        page_url = f"https://{repo_name}"
        print(f"\n✅ Tu sitio web está siendo desplegado ahora mismo.")
        print(f"🔗 **URL probable de tu página:** {page_url}")
        print("NOTA: El despliegue a través de GitHub Actions tarda unos segundos en hacerse efectivo.")
    else:
        print("\nNo se pudo obtener la URL de GitHub Pages automáticamente.")
        print("Revisa la pestaña 'Actions' en GitHub para confirmar el estado del despliegue.")
    print("=" * 40)


if __name__ == "__main__":
    main()
