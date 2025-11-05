class GestorCursos:
    """Clase que maneja las operaciones de la DB para cursos y certificados."""

    def __init__(self):
        self._cursos_por_id: Dict[str, Curso] = {}
        self._certificados: Dict[str, Certificado] = {}

    def _guardar_curso(self, curso: Curso):
        """Función interna DRY: Persiste el objeto Curso."""
        self._cursos_por_id[curso.id] = curso

    def obtener_por_id(self, curso_id: str) -> Optional[Curso]:
        """Obtiene un curso por su ID."""
        return self._cursos_por_id.get(curso_id)

    def obtener_cursos_por_instructor(self, instructor_id: str) -> List[Curso]:
        """Obtiene todos los cursos creados por un instructor (RF12)."""
        return [c for c in self._cursos_por_id.values() if c.instructor_id == instructor_id]

    def obtener_cursos_publicados(self) -> List[Curso]:
        """Obtiene el catálogo de cursos disponibles (RF9)."""
        return [c for c in self._cursos_por_id.values() if c.publicado]

    def guardar_certificado(self, certificado: Certificado):
        """Guarda un certificado en la colección."""
        self._certificados[certificado.id] = certificado

    def obtener_certificado_por_id(self, cert_id: str) -> Optional[Certificado]:
        """Busca un certificado para su validación."""
        return self._certificados.get(cert_id)

# Instancia global del gestor
gestor_cursos = GestorCursos()

# ----------------------------------------------------------------------
# 4. FUNCIONES DE LÓGICA DE NEGOCIO (Responsabilidad Única)
# ----------------------------------------------------------------------

def crear_curso(titulo: str, instructor_id: str, precio: float = 0.0) -> Curso:
    """Lógica de negocio: Crea una instancia de Curso (RF1)."""
    instructor = gestor_usuarios.obtener_por_id(instructor_id)

    if not instructor or instructor.rol not in ["Maestro", "Especialista"]:
        # Validación de rol (Clean Code: Manejo de errores de acceso)
        raise AccesoDenegado("Solo Maestros/Especialistas pueden crear cursos.")

    nuevo_curso = Curso(titulo, instructor_id, precio)
    gestor_cursos._guardar_curso(nuevo_curso)
    return nuevo_curso
