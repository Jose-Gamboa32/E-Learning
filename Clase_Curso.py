import uuid
from typing import List, Dict, Optional, TYPE_CHECKING
import time

# Permite la verificación de tipos sin crear dependencia cíclica
if TYPE_CHECKING:
    from gestion_usuarios import Usuario, GestorUsuarios

# Simulamos la importación del gestor de usuarios para validación de roles
# En una aplicación real, esto sería inyección de dependencia.
# from gestion_usuarios import gestor_usuarios, AccesoDenegado, UsuarioNoEncontrado, Usuario

# ----------------------------------------------------------------------
# 1. EXCEPCIONES PERSONALIZADAS
# ----------------------------------------------------------------------

class ErrorCurso(Exception):
    """Excepción base para errores relacionados con la gestión de cursos."""
    pass

class PublicacionInvalida(ErrorCurso):
    """Lanzada cuando un curso no cumple los requisitos para ser publicado."""
    pass

class MatriculaInvalida(ErrorCurso):
    """Lanzada cuando un usuario no puede matricularse (ej. ya inscrito)."""
    pass

# ----------------------------------------------------------------------
# 2. ENTIDADES PRINCIPALES (Clean Code: Representación de datos)
# ----------------------------------------------------------------------

class Certificado:
    """Representa un certificado de finalización (RF8)."""
    def __init__(self, usuario_id: str, curso_id: str, fecha_emision: str):
        self.id = str(uuid.uuid4())
        self.usuario_id = usuario_id
        self.curso_id = curso_id
        self.fecha_emision = fecha_emision

    def generar_url_verificacion(self) -> str:
        """Función corta: Simula la generación de un enlace de verificación."""
        return f"lms.com/verify/cert/{self.id}"

class Curso:
    """Representa la entidad Curso (RF1)."""
    def __init__(self, titulo: str, instructor_id: str, precio: float = 0.0, id_curso: Optional[str] = None):
        self.id: str = id_curso if id_curso else str(uuid.uuid4())
        self.titulo: str = titulo
        self.instructor_id: str = instructor_id
        self.precio: float = precio
        self.modulos: List[Dict] = []
        self.publicado: bool = False
        self.inscritos: List[str] = [] # Almacena IDs de usuario
        self.progreso: Dict[str, float] = {} # {usuario_id: porcentaje_progreso}

    def agregar_modulo_y_lecciones(self, titulo_modulo: str, lecciones: List[str]):
        """Añade un módulo con su lista de lecciones (RF1.1)."""
        self.modulos.append({"titulo": titulo_modulo, "lecciones": lecciones})

    def obtener_total_lecciones(self) -> int:
        """Función corta DRY: Calcula el número total de lecciones."""
        return sum(len(m['lecciones']) for m in self.modulos)

    def __str__(self):
        return f"Curso(ID: {self.id}, Título: {self.titulo}, Módulos: {len(self.modulos)})"
