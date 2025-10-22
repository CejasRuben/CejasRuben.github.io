import subprocess
import datetime
import sys
import os

def run_command(command, error_message):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        if result.stdout.strip():
            print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: {error_message}\nDetalles: {e.stderr.strip() if e.stderr else e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ ERROR: No se encontró 'git'. Asegúrate de tenerlo instalado.")
        sys.exit(1)

def get_repo_name():
    try:
        result = subprocess.run(["git", "config", "--get", "remote.origin.url"], 
                                check=True, text=True, capture_output=True)
        url = result.stdout.strip()
        repo_part = url.split('/')[-1].replace(".git", "")
        return repo_part
    except Exception:
        return None

def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Actualización automática (push desde Termux) - {timestamp}"

    print("\n➤ Preparando archivos para subir (excluyendo .git)...")

    # Paso 1: Agregar manualmente todo excepto .git y otros no deseados
    for root, dirs, files in os.walk("."):
        # Ignorar carpetas ocultas
        if ".git" in dirs:
            dirs.remove(".git")
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")
        for file in files:
            if not file.startswith(".") and not file.endswith((".pyc", ".log")):
                file_path = os.path.join(root, file)
                run_command(["git", "add", file_path], f"Error al agregar {file_path}")

    print("\n➤ Creando commit...")
    run_command(["git", "commit", "-m", commit_message], "Fallo al crear el commit (puede que no haya cambios nuevos).")

    print("\n➤ Haciendo push al repositorio remoto...")
    run_command(["git", "push"], "Fallo al hacer push.")

    print("\n" + "=" * 40)
    print("✔ ¡OPERACIÓN COMPLETADA CON ÉXITO!")

    repo_name = get_repo_name()
    if repo_name and ".github.io" in repo_name:
        print(f"\n✅ Tu sitio se está desplegando: https://{repo_name}")
    else:
        print("\nℹ No se pudo determinar la URL de GitHub Pages automáticamente.")
    print("=" * 40)

if __name__ == "__main__":
    main()
