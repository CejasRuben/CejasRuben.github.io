"""
subir_html_css_icon.py

Este script automatiza la subida de archivos web a GitHub desde Termux.
Incluye HTML, CSS, iconos, manifest y todos los recursos del proyecto.

Qué hace:
1. Agrega archivos .html, .css, .png, .ico, .xml, .webmanifest y recursos
2. Crea un commit con un mensaje que incluye fecha y hora
3. Hace push de los cambios al repositorio remoto en GitHub
4. Muestra la URL probable de tu sitio de GitHub Pages
"""

import subprocess
import datetime
import sys
import glob
import os

def run_command(command, error_message, continue_on_error=False):
    """Ejecuta un comando de shell y maneja posibles errores."""
    try:
        # check=True lanzará una excepción si el comando falla
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        if result.stdout.strip():
            # Muestra la salida del comando si existe (ej. lista de archivos commitados)
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        if continue_on_error:
            print(f"⚠️  Advertencia: {error_message}")
            return False
        else:
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

def verificar_archivos_esenciales():
    """Verifica que existan los archivos esenciales para el proyecto."""
    archivos_esenciales = [
        'index.html',
        'site.webmanifest',
        'favicon.ico',
        'favicon-16x16.png',
        'favicon-32x32.png',
        'apple-touch-icon.png',
        'android-chrome-192x192.png',
        'android-chrome-512x512.png'
    ]
    
    print("\n🔍 Verificando archivos esenciales...")
    faltantes = []
    
    for archivo in archivos_esenciales:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} - NO ENCONTRADO")
            faltantes.append(archivo)
    
    if faltantes:
        print(f"\n⚠️  Advertencia: Faltan {len(faltantes)} archivos esenciales")
        print("   El sitio puede no funcionar correctamente sin ellos.")
    
    return len(faltantes) == 0

def main():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Actualización completa del sitio - {timestamp}"

    print("🚀 INICIANDO SUBIDA AUTOMÁTICA A GITHUB")
    print("=" * 50)
    
    # Verificar archivos esenciales
    todos_presentes = verificar_archivos_esenciales()
    
    if not todos_presentes:
        print("\n💡 Consejo: Genera los archivos faltantes con 'genera_index_html_6_chatgpt_iconos.py'")
        respuesta = input("¿Continuar con la subida? (s/N): ")
        if respuesta.lower() not in ['s', 'si', 'y', 'yes']:
            print("❌ Subida cancelada por el usuario.")
            return

    # Paso 1: Agregar archivos HTML, CSS, iconos y recursos
    print("\n📁 Agregando archivos web al control de versiones...")
    
    # Patrones de archivos específicos basados en tu proyecto
    file_patterns = [
        "*.html",
        "*.css", 
        "*.js",
        "*.png",
        "*.ico",
        "*.xml",
        "*.webmanifest",
        "*.json",
        "*.txt"
    ]
    
    # Agregar cada patrón de archivo (continuar si no hay archivos)
    archivos_agregados = 0
    for pattern in file_patterns:
        files = glob.glob(pattern)
        if files:
            success = run_command(["git", "add", pattern], 
                               f"Fallo al agregar los archivos {pattern}.", 
                               continue_on_error=True)
            if success:
                archivos_agregados += len(files)
                print(f"   ✅ {pattern} ({len(files)} archivos)")

    # También intentar agregar cualquier archivo en carpetas comunes de recursos
    additional_folders = ["images/", "img/", "icons/", "assets/", "resources/", "css/", "js/"]
    for folder in additional_folders:
        if os.path.exists(folder):
            success = run_command(["git", "add", f"{folder}*"], 
                               f"Fallo al agregar archivos en {folder}", 
                               continue_on_error=True)
            if success:
                print(f"   ✅ {folder}*")

    if archivos_agregados == 0:
        print("   ℹ️  No se encontraron archivos nuevos para agregar.")

    # Paso 2: Verificar si hay cambios antes de commit
    print("\n🔍 Verificando cambios...")
    result = subprocess.run(["git", "status", "--porcelain"], 
                          capture_output=True, text=True)
    
    if not result.stdout.strip():
        print("ℹ️  No hay cambios para commitear.")
        return

    # Paso 3: Crear commit
    print("\n💾 Creando commit...")
    run_command(["git", "commit", "-m", commit_message], 
               "Fallo al crear el commit.")

    # Paso 4: Hacer push
    print("\n🚀 Iniciando push al repositorio remoto...")
    run_command(["git", "push"], 
               "Fallo al subir los cambios (push) al repositorio remoto.")

    print("\n" + "=" * 60)
    print("🎉 ¡OPERACIÓN DE SUBIDA COMPLETADA CON ÉXITO!")
    
    # Paso 5: Mostrar la URL de GitHub Pages
    repo_name = get_repo_name()
    if repo_name and ".github.io" in repo_name:
        page_url = f"https://{repo_name}"
        print(f"\n✅ Tu sitio web está siendo desplegado ahora mismo.")
        print(f"🔗 **URL de tu página:** {page_url}")
        print("📱 **Configuración:** Acceso directo 'En lo profundo'")
        print("⏱️  **NOTA:** El despliegue en GitHub Pages tarda 1-2 minutos en actualizarse.")
        print("\n📋 Archivos incluidos:")
        print("   • HTML, CSS, JavaScript")
        print("   • Iconos (PNG, ICO, Apple Touch)")
        print("   • Configuración PWA (site.webmanifest)")
        print("   • Browserconfig (Windows)")
    else:
        print("\n⚠️  No se pudo obtener la URL de GitHub Pages automáticamente.")
        print("   Revisa la configuración de tu repositorio en GitHub.")
        print("   Ve a: Settings > Pages > GitHub Pages")
    
    print("=" * 60)

    # Información adicional
    print("\n💡 **Siguientes pasos:**")
    print("   1. Espera 1-2 minutos para que GitHub Pages se actualice")
    print("   2. Visita tu sitio para verificar que todo funcione")
    print("   3. Prueba agregar el sitio a tu pantalla de inicio")
    print("   4. Verifica que el acceso directo se cree como 'En lo profundo'")


if __name__ == "__main__":
    main()
