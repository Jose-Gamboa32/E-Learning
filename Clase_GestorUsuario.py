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
