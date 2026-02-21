# Guía de Acceso y Visualización: ChromaDB (HMO Auditor)

Al usar una base de datos vectorial local como **ChromaDB**, no tienes un "archivo Excel" que puedas abrir con un doble clic, ya que los datos son vectores matemáticos (largas listas de números). Sin embargo, aquí tienes cómo puedes "entrar" y ver lo que hay dentro.

## 1. ¿Necesitas instalar algo?
Sí, para manejar e inspeccionar la base de datos desde tu PC, necesitas instalar la librería en tu entorno de Python:

```powershell
pip install chromadb
```

## 2. ¿Dónde viven los datos físicos?
En tu estructura de carpetas, una vez que el motor RAG esté extrayendo datos, verás una subcarpeta llamada `vdb` dentro de la carpeta de la empresa (bajo `02_Auditoria_IA`). Allí verás archivos como:
- `chroma.sqlite3`: Donde se guardan los metadatos y el índice.
- Carpetas con IDs largos: Donde se guardan los tensores (los vectores).

## 3. Script de Inspección Rápida (El "Peek")
He creado este pequeño script para que puedas ver cuántos párrafos de la norma o de tu empresa han sido indexados.

```python
import chromadb
import os

# Ruta a la carpeta de tu empresa
db_path = os.path.join(os.getcwd(), "Auditorias_HMO", "Nombre_Empresa", "02_Auditoria_IA", "vdb")

# Conectar al cliente
client = chromadb.PersistentClient(path=db_path)

# Listar colecciones (ej. 'normas_iso', 'contexto_empresa')
collections = client.list_collections()
print(f"📦 Colecciones encontradas: {len(collections)}")

for col in collections:
    count = col.count()
    print(f"🔹 Colección: {col.name} | Párrafos indexados: {count}")
    
    # Ver los primeros 2 elementos (metadatos y texto)
    peek = col.peek(limit=2)
    print(f"   🔍 Ejemplo de contenido: {peek['documents']}")
```

## 4. Visualización Gráfica (Opcional)
Si quieres algo visual (una interfaz gráfica), existen herramientas de la comunidad como:
- **[Chroma-UI](https://github.com/mgramin/chroma-ui)**: Una interfaz web sencilla para navegar por tus colecciones.
- **[ChromaDB-Admin](https://github.com/flanker/chromadb-admin)**: Otra opción popular.

> [!TIP]
> **Recomendación Profesional**: No edites los archivos `.sqlite3` o las carpetas de ChromaDB manualmente, ya que podrías corromper el índice vectorial. Usa siempre el aplicativo o scripts controlados para interactuar con la base de datos.
