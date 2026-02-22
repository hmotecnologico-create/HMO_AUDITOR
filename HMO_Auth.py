"""
HMO_Auth.py — Módulo de Autenticación Local v1.0
Contraseñas hasheadas con SHA-256. Sin dependencias externas.
Roles: admin | auditor | visitante
"""

import json
import os
import hashlib
import datetime

USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hmo_users.json")

DEFAULT_ADMIN_USER = "admin"
DEFAULT_ADMIN_PASS = "HMO2024!"  # Contraseña temporal — se fuerza cambio en primer login

# ─── UTILIDADES ──────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Hashea una contraseña con SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(password: str, stored_hash: str) -> bool:
    """Verifica una contraseña contra su hash almacenado."""
    return hash_password(password) == stored_hash

# ─── CARGA Y GUARDADO ────────────────────────────────────────────────────────

def load_users() -> dict:
    """Carga el archivo de usuarios. Si no existe, lo crea con el admin por defecto."""
    if not os.path.exists(USERS_FILE):
        _create_default_users()
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(data: dict) -> None:
    """Guarda el archivo de usuarios."""
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def _create_default_users() -> None:
    """Crea el archivo inicial con un admin temporal."""
    data = {
        "meta": {
            "version": "1.0",
            "creado": datetime.datetime.now().isoformat(),
            "descripcion": "Archivo de usuarios HMO Auditor"
        },
        "usuarios": [
            {
                "user": DEFAULT_ADMIN_USER,
                "hash": hash_password(DEFAULT_ADMIN_PASS),
                "rol": "admin",
                "nombre": "Administrador HMO",
                "activo": True,
                "primer_login": True,  # Obliga a cambiar clave al primer acceso
                "creado": datetime.datetime.now().isoformat(),
                "ultimo_acceso": None
            }
        ]
    }
    save_users(data)

# ─── AUTENTICACIÓN ───────────────────────────────────────────────────────────

def check_login(username: str, password: str) -> dict | None:
    """
    Verifica credenciales.
    Retorna el dict del usuario si son correctas, None si no.
    """
    data = load_users()
    username = username.strip().lower()
    for user in data["usuarios"]:
        if user["user"].lower() == username and user["activo"]:
            if verify_password(password, user["hash"]):
                # Actualizar último acceso
                user["ultimo_acceso"] = datetime.datetime.now().isoformat()
                save_users(data)
                return user
    return None

def change_password(username: str, new_password: str) -> bool:
    """Cambia la contraseña de un usuario y desactiva la bandera primer_login."""
    data = load_users()
    for user in data["usuarios"]:
        if user["user"].lower() == username.strip().lower():
            user["hash"] = hash_password(new_password)
            user["primer_login"] = False
            save_users(data)
            return True
    return False

# ─── GESTIÓN DE USUARIOS (ADMIN) ─────────────────────────────────────────────

def get_all_users() -> list:
    """Devuelve la lista de usuarios (sin hashes)."""
    data = load_users()
    return [
        {k: v for k, v in u.items() if k != "hash"}
        for u in data["usuarios"]
    ]

def create_user(username: str, password: str, rol: str, nombre: str) -> tuple[bool, str]:
    """
    Crea un nuevo usuario.
    Retorna (True, "ok") o (False, "mensaje de error").
    """
    if rol not in ("admin", "auditor", "visitante"):
        return False, "Rol inválido. Usa: admin, auditor o visitante."
    
    data = load_users()
    username = username.strip().lower()
    
    # Verificar que no exista
    for user in data["usuarios"]:
        if user["user"].lower() == username:
            return False, f"El usuario '{username}' ya existe."
    
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres."
    
    new_user = {
        "user": username,
        "hash": hash_password(password),
        "rol": rol,
        "nombre": nombre.strip(),
        "activo": True,
        "primer_login": True,
        "creado": datetime.datetime.now().isoformat(),
        "ultimo_acceso": None
    }
    data["usuarios"].append(new_user)
    save_users(data)
    return True, "ok"

def toggle_user_active(username: str) -> bool:
    """Activa/desactiva un usuario. Retorna el nuevo estado."""
    data = load_users()
    for user in data["usuarios"]:
        if user["user"].lower() == username.strip().lower():
            if user["rol"] == "admin":
                # Nunca desactivar el último admin
                admins_activos = [u for u in data["usuarios"]
                                  if u["rol"] == "admin" and u["activo"]]
                if len(admins_activos) <= 1:
                    return user["activo"]  # Sin cambio
            user["activo"] = not user["activo"]
            save_users(data)
            return user["activo"]
    return False

def delete_user(username: str) -> tuple[bool, str]:
    """Elimina un usuario (no se puede eliminar al único admin activo)."""
    data = load_users()
    username = username.strip().lower()
    
    for i, user in enumerate(data["usuarios"]):
        if user["user"].lower() == username:
            if user["rol"] == "admin":
                admins = [u for u in data["usuarios"] if u["rol"] == "admin"]
                if len(admins) <= 1:
                    return False, "No puedes eliminar el único administrador."
            data["usuarios"].pop(i)
            save_users(data)
            return True, "ok"
    return False, "Usuario no encontrado."

# ─── UTILIDADES DE ROL ───────────────────────────────────────────────────────

ROL_LABELS = {
    "admin":     ("👑 Administrador", "#F59E0B"),
    "auditor":   ("🔍 Auditor",       "#00C2FF"),
    "visitante": ("👁️ Visitante",     "#94A3B8"),
}

def get_rol_label(rol: str) -> tuple[str, str]:
    """Retorna (etiqueta, color) del rol."""
    return ROL_LABELS.get(rol, ("❓ Desconocido", "#475569"))

def can(auth: dict, accion: str) -> bool:
    """
    Verifica si un usuario autenticado puede realizar una acción.
    auth = st.session_state['auth']
    """
    rol = auth.get("rol", "visitante")
    permisos = {
        "nuevo_proyecto":    ["admin", "auditor"],
        "ver_simulacion":    ["admin", "auditor", "visitante"],
        "gestion_usuarios":  ["admin"],
        "override_campos":   ["admin"],
        "ver_todos_proyectos": ["admin"],
        "emitir_informe":    ["admin", "auditor"],
    }
    return rol in permisos.get(accion, [])

# ─── RECUPERACIÓN DE EMERGENCIA ───────────────────────────────────────────────

# Clave maestra "break glass" — HMO entrega físicamente a responsable de TI
# NUNCA almacenar esta clave en el sistema de producción de forma visible
MASTER_RECOVERY_KEY = "HMO-RECOVERY-2024-ADMIN"

def emergency_reset_admin(master_key: str, new_password: str) -> tuple[bool, str]:
    """
    Restablece la clave del primer admin usando la clave maestra.
    Se invoca desde recuperar_acceso.bat o desde la pantalla de emergencia.
    
    Args:
        master_key: Clave maestra proporcionada por HMO.
        new_password: Nueva contraseña para el administrador.
    
    Returns:
        (True, "ok") o (False, "mensaje de error")
    """
    if master_key.strip() != MASTER_RECOVERY_KEY:
        return False, "Clave maestra incorrecta. Contacta a HMO Tecnológico."

    if len(new_password) < 8:
        return False, "La nueva contraseña debe tener al menos 8 caracteres."

    data = load_users()
    
    # Buscar primer admin
    admin_encontrado = False
    for user in data["usuarios"]:
        if user["rol"] == "admin":
            user["hash"] = hash_password(new_password)
            user["activo"] = True
            user["primer_login"] = False
            admin_encontrado = True
            # Registrar evento
            user["ultimo_acceso"] = f"RESET-EMERGENCIA-{datetime.datetime.now().isoformat()}"
            break

    if not admin_encontrado:
        # Si no hay ningún admin, recrear el archivo completo
        _create_default_users()
        data = load_users()
        data["usuarios"][0]["hash"] = hash_password(new_password)
        data["usuarios"][0]["primer_login"] = False
        admin_encontrado = True

    save_users(data)
    
    # Registrar evento de recuperación en log
    log_path = os.path.join(os.path.dirname(USERS_FILE), "hmo_recovery_log.txt")
    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"{datetime.datetime.now().isoformat()} — RESET DE EMERGENCIA ejecutado\n")
    
    return True, "ok"


# ─── PUNTO DE ENTRADA CLI (para recuperar_acceso.bat) ────────────────────────
if __name__ == "__main__":
    """
    Permite ejecutar: python HMO_Auth.py
    Solicita clave maestra y nueva contraseña del admin por consola.
    """
    print("=" * 55)
    print("  HMO Auditor — RECUPERACIÓN DE ACCESO DE EMERGENCIA")
    print("=" * 55)
    print("Este proceso requiere la clave maestra entregada por HMO.")
    print()
    
    master = input("Ingresa la clave maestra: ").strip()
    if not master:
        print("❌ Operación cancelada.")
        exit(1)
    
    new_pass = input("Nueva contraseña para el administrador (min. 8 car.): ").strip()
    confirm  = input("Confirmar contraseña: ").strip()
    
    if new_pass != confirm:
        print("❌ Las contraseñas no coinciden. Operación cancelada.")
        exit(1)
    
    ok, msg = emergency_reset_admin(master, new_pass)
    if ok:
        print()
        print("✅ ¡Acceso restablecido! Puedes ingresar con usuario 'admin'.")
        print("   Abre la app HMO nuevamente.")
    else:
        print(f"❌ Error: {msg}")

