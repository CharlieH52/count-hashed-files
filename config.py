"""
Configuración global del Certificador de Archivos.
"""

# Constante de tipo boolean para activar y desactivar el almacenamiento
# de las certificaciones en el repositorio JSON.
SAVE_JSON_CERTIFICATIONS: bool = True

# Constante de tipo boolean para activar y desactivar el almacenamiento
# de las certificaciones en la base de datos SQLite3.
SAVE_SQLITE_CERTIFICATIONS: bool = True

# Directorio de salida para reportes y certificaciones
OUTPUT_DIRECTORY: str = "Certificaciones"

# Nombre del archivo de base de datos SQLite3
SQLITE_DB_NAME: str = "certificaciones.sqlite3"

# Algoritmo de hash por defecto
DEFAULT_HASH_ALGORITHM: str = "SHA256"

# Tamaño de bloque para lectura de archivos (64 KB)
HASH_CHUNK_SIZE: int = 65536
