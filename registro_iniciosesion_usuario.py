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
