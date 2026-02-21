import chromadb
import os
import sys

def inspect_db(company_folder):
    # Ruta estándar en HMO Auditor
    base_path = os.path.join(os.getcwd(), "Auditorias_HMO", company_folder, "02_Auditoria_IA", "vdb")
    
    if not os.path.exists(base_path):
        print(f"❌ No se encontró base de datos en: {base_path}")
        return

    try:
        client = chromadb.PersistentClient(path=base_path)
        collections = client.list_collections()
        
        print(f"\n--- 🛡️ HMO Auditor: Inspector de Base de Datos Vectorial ---")
        print(f"📍 Directorio: {base_path}")
        print(f"📦 Colecciones: {len(collections)}")
        print("-" * 50)
        
        for col in collections:
            print(f"🔹 [{col.name}] -> {col.count()} fragmentos normativos/evidencias.")
            
    except Exception as e:
        print(f"⚠️ Error al conectar: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inspect_db(sys.argv[1])
    else:
        print("Uso: python inspect_vdb.py [Nombre_Carpeta_Empresa]")
