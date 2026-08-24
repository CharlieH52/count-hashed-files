"""
Configuración global del Certificador de Archivos.
"""

# Constante de tipo boolean para activar y desactivar el almacenamiento
# de las certificaciones en el repositorio JSON.
SAVE_JSON_CERTIFICATIONS: bool = True

# Directorio de salida para reportes y certificaciones
OUTPUT_DIRECTORY: str = "Certificaciones"

# Algoritmo de hash por defecto
DEFAULT_HASH_ALGORITHM: str = "SHA256"

# Tamaño de bloque para lectura de archivos (64 KB)
HASH_CHUNK_SIZE: int = 65536
