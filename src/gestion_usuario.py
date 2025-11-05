import hashlib
import uuid
from typing import Dict, Optional, List

# ----------------------------------------------------------------------
# 1. EXCEPCIONES PERSONALIZADAS
# ----------------------------------------------------------------------

class ErrorAutenticacion(Exception):
    """Excepción base para errores relacionados con la autenticación o el acceso."""
    pass

class CredencialesInvalidas(ErrorAutenticacion):
    """Lanzada cuando la contraseña o el email son incorrectos."""
    pass

class UsuarioNoEncontrado(ErrorAutenticacion):
    """Lanzada cuando se intenta operar con un ID de usuario inexistente."""
    pass

class AccesoDenegado(ErrorAutenticacion):
    """Lanzada cuando un usuario intenta realizar una acción sin el rol adecuado."""
    pass

# ----------------------------------------------------------------------
# 2. ENTIDADES PRINCIPALES (Clean Code: Representación de datos)
# ----------------------------------------------------------------------

class Usuario:
    """Clase que representa la entidad de un usuario del LMS."""
    ROLES_VALIDOS = ["Estudiante", "Maestro", "Especialista", "Administrador"]

    def __init__(self, nombre: str, email: str, rol: str = "Estudiante", id_usuario: Optional[str] = None):
        """Inicializa el usuario con validación de rol."""
        if rol not in self.ROLES_VALIDOS:
            raise ValueError(f"Rol '{rol}' no válido. Debe ser uno de {self.ROLES_VALIDOS}")
            
        self.id: str = id_usuario if id_usuario else str(uuid.uuid4())
        self.nombre: str = nombre
        self.email: str = email.lower()
        self.rol: str = rol
        self.__password_hash: Optional[str] = None
        self.fecha_registro: str = str(uuid.uuid1()) # Simula timestamp de registro
        self.activo: bool = True

    def establecer_contraseña(self, password: str):
        """Hashea y almacena la contraseña. Función de responsabilidad única."""
        if not password or len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        # Usando SHA256 para simular un hash seguro (mejores prácticas)
        self.__password_hash = hashlib.sha256(password.encode()).hexdigest()

    def verificar_contraseña(self, password: str) -> bool:
        """Verifica si la contraseña coincide con el hash almacenado."""
        return hashlib.sha256(password.encode()).hexdigest() == self.__password_hash

    def cambiar_rol(self, nuevo_rol: str):
        """Permite cambiar el rol, usado típicamente por Administradores."""
        if nuevo_rol not in self.ROLES_VALIDOS:
            raise ValueError(f"El nuevo rol '{nuevo_rol}' no es válido.")
        self.rol = nuevo_rol
        
    def __str__(self):
        return f"Usuario(ID: {self.id}, Nombre: {self.nombre}, Rol: {self.rol})"

# ----------------------------------------------------------------------
# 3. GESTOR DE DATOS (Clean Code: Centralización de acceso a datos)
# ----------------------------------------------------------------------

class GestorUsuarios:
    """Clase que maneja las operaciones de la DB para la colección de usuarios."""

    def __init__(self):
        # Almacena usuarios por ID (diccionario principal)
        self._usuarios_por_id: Dict[str, Usuario] = {}
        # Mapea email a ID para búsquedas rápidas (evita duplicación de código en búsquedas)
        self._mapeo_email_id: Dict[str, str] = {}
        # Pre-registro de un administrador para pruebas
        self._inicializar_admin()

    def _inicializar_admin(self):
        """Inicializa un usuario administrador para las pruebas de roles."""
        admin = Usuario("System Admin", "admin@lms.com", rol="Administrador")
        admin.establecer_contraseña("adminpass")
        self._guardar_usuario(admin)

    def _guardar_usuario(self, usuario: Usuario):
        """Función interna DRY: Guarda el objeto Usuario y actualiza el mapeo."""
        self._usuarios_por_id[usuario.id] = usuario
        self._mapeo_email_id[usuario.email] = usuario.id

    def obtener_por_id(self, user_id: str) -> Optional[Usuario]:
        """Obtiene un usuario por su ID único."""
        return self._usuarios_por_id.get(user_id)

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario utilizando el mapeo de email a ID."""
        user_id = self._mapeo_email_id.get(email.lower())
        return self.obtener_por_id(user_id) if user_id else None

    def email_existe(self, email: str) -> bool:
        """Función corta DRY para verificar la existencia de un email."""
        return email.lower() in self._mapeo_email_id

    def obtener_todos_por_rol(self, rol: str) -> List[Usuario]:
        """Filtra y devuelve todos los usuarios que tienen un rol específico."""
        return [u for u in self._usuarios_por_id.values() if u.rol == rol]
    
    def actualizar_perfil(self, user_id: str, nuevos_datos: Dict[str, str]):
        """Función de responsabilidad única: Actualiza el nombre o el email del usuario (RF15)."""
        usuario = self.obtener_por_id(user_id)
        if not usuario:
            raise UsuarioNoEncontrado("No se puede actualizar, el usuario no existe.")

        if 'nombre' in nuevos_datos and nuevos_datos['nombre']:
            usuario.nombre = nuevos_datos['nombre']
        
        # Lógica para cambiar email
        if 'email' in nuevos_datos and nuevos_datos['email'].lower() != usuario.email:
            nuevo_email = nuevos_datos['email'].lower()
            if self.email_existe(nuevo_email):
                raise ErrorAutenticacion("El nuevo email ya está en uso.")
            
            # Actualiza el mapeo
            del self._mapeo_email_id[usuario.email]
            usuario.email = nuevo_email
            self._mapeo_email_id[usuario.email] = usuario.id
        
        self._guardar_usuario(usuario)
        return usuario
        
# Instancia global del gestor para simular el singleton de acceso a datos
gestor_usuarios = GestorUsuarios() 

# ----------------------------------------------------------------------
# 4. FUNCIONES DE LÓGICA DE NEGOCIO (Responsabilidad Única)
# ----------------------------------------------------------------------

def registrar_usuario(nombre: str, email: str, password: str, rol: str = "Estudiante") -> Usuario:
    """Lógica de negocio: Crea un nuevo usuario y lo persiste (RF2)."""
    if gestor_usuarios.email_existe(email):
        raise ErrorAutenticacion("El email ya está registrado.")
    
    nuevo_usuario = Usuario(nombre, email, rol)
    try:
        nuevo_usuario.establecer_contraseña(password)
    except ValueError as e:
        raise ErrorAutenticacion(f"Error en contraseña: {e}") from e
    
    gestor_usuarios._guardar_usuario(nuevo_usuario)
    return nuevo_usuario

def iniciar_sesion(email: str, password: str) -> Usuario:
    """Lógica de negocio: Autentica un usuario (RF2)."""
    usuario = gestor_usuarios.obtener_por_email(email)

    if not usuario or not usuario.activo:
        raise CredencialesInvalidas("Usuario o contraseña incorrectos.")

    if not usuario.verificar_contraseña(password):
        raise CredencialesInvalidas("Usuario o contraseña incorrectos.")
    
    # Simulación de generación de token de sesión aquí si fuera necesario
    return usuario
