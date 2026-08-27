import subprocess
import sys
import shutil
import os
from pathlib import Path


def build_exe():
    output_name = "GENERADOR_HUELLA_HASH"
    script_name = "main.py"
    icon_file = None
    
    base_dir = Path(__file__).parent.resolve()
    script_path = base_dir / script_name
    dist_dir = base_dir / "dist"
    build_dir = base_dir / "build"
    spec_file = base_dir / f"{output_name}.spec"

    if not script_path.exists():
        print(f"[ERROR] No se encontró: {script_path}")
        sys.exit(1)

    if shutil.which("pyinstaller") is None:
        print("[ERROR] PyInstaller no está instalado.")
        sys.exit(1)

    # --- Limpieza profunda ---
    print("[INFO] Limpiando builds anteriores...")
    for folder in [dist_dir, build_dir]:
        if folder.exists():
            shutil.rmtree(folder)
    if spec_file.exists():
        spec_file.unlink()

    # --- Generar .spec base (SIN --noconfirm, SIN --clean) ---
    makespec_cmd = [
        sys.executable, "-m", "PyInstaller.utils.cliutils.makespec",
        "--windowed",
        "--onefile",
        f"--name={output_name}",
        "--collect-all", "flet",
        str(script_path)
    ]
    
    print("[INFO] Generando archivo .spec base...")
    try:
        result = subprocess.run(makespec_cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Falló pyi-makespec:\n{e.stderr}")
        sys.exit(1)

    # --- Modificar el .spec para excluir tkinter COMPLETAMENTE ---
    spec_content = spec_file.read_text(encoding="utf-8")

    # Busca la línea de excludes y reemplázala
    if "excludes=" in spec_content:
        spec_content = spec_content.replace(
            "excludes=[],",
            "excludes=['tkinter', '_tkinter', 'Tkinter'],"
        )
    else:
        # Fallback: insertar en el constructor de Analysis
        spec_content = spec_content.replace(
            "a = Analysis(",
            "a = Analysis(\n    excludes=['tkinter', '_tkinter', 'Tkinter'],"
        )

    spec_file.write_text(spec_content, encoding="utf-8")
    print(f"[INFO] .spec modificado con excludes de tkinter")

    # --- Compilar desde el .spec modificado ---
    build_cmd = [
        sys.executable, "-m", "PyInstaller",
        str(spec_file),
        "--clean",
        "--noconfirm",
    ]

    print(f"[INFO] Compilando desde spec...\n")
    try:
        result = subprocess.run(
            build_cmd,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        print(result.stdout)
        print(f"\n[OK] Ejecutable generado en: {dist_dir / output_name}.exe")
        
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] La compilación falló. Código: {e.returncode}")
        print("\n--- STDOUT ---\n", e.stdout or "(vacío)")
        print("\n--- STDERR ---\n", e.stderr or "(vacío)")
        sys.exit(1)


if __name__ == "__main__":
    build_exe()