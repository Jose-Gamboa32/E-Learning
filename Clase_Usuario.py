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
