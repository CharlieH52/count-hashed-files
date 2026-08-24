import subprocess

def build_exe():
    output_name = 'GENERADOR_HUELLA_HASH'
    script_name = 'main.py'

    BUILD_SECUENCE = [
        'pyinstaller',
        '--windowed',
        '--onefile',
        '--clean',
        f'--name={output_name}',
        '--collect-all',
        'flet',
        script_name
    ]

    try:
        subprocess.run(BUILD_SECUENCE)
    except subprocess.CalledProcessError as e:
        print(e)

    except PermissionError as e:
        print(e)

build_exe()