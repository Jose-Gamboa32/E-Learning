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

# ----------------------------------------------------------------------
# 3. GESTOR DE DATOS (Clean Code: Centralización de acceso a datos)
# ----------------------------------------------------------------------

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

def agregar_contenido_al_curso(curso_id: str, modulo_titulo: str, lecciones: List[str]):
    """Función de responsabilidad única: Añade contenido al curso."""
    curso = gestor_cursos.obtener_por_id(curso_id)
    if not curso:
        raise UsuarioNoEncontrado("Curso no encontrado.")

    if curso.publicado:
        raise ErrorCurso("No se puede editar el contenido de un curso publicado.")

    curso.agregar_modulo_y_lecciones(modulo_titulo, lecciones)
    gestor_cursos._guardar_curso(curso)

def publicar_curso(curso_id: str):
    """Lógica de negocio: Valida y publica un curso."""
    curso = gestor_cursos.obtener_por_id(curso_id)
    if not curso:
        raise UsuarioNoEncontrado("Curso no encontrado.")

    # Validación mínima de contenido (RD5)
    if curso.obtener_total_lecciones() < 3:
        raise PublicacionInvalida("El curso debe tener al menos 3 lecciones para ser publicado.")

    # Set the 'publicado' attribute to True instead of calling a non-existent method
    curso.publicado = True
    gestor_cursos._guardar_curso(curso)
    return curso

def matricular_usuario(curso_id: str, usuario_id: str, pago_exitoso: bool = True):
    """
    Lógica de negocio: Matricula un usuario. Simula la verificación del pago (RF5).
    """
    curso = gestor_cursos.obtener_por_id(curso_id)
    usuario = gestor_usuarios.obtener_por_id(usuario_id)

    if not curso or not usuario:
        raise UsuarioNoEncontrado("Curso o Usuario no encontrados.")

    if not curso.publicado:
        raise MatriculaInvalida("El curso no está disponible para matrícula.")

    if usuario_id in curso.inscritos:
        raise MatriculaInvalida("El usuario ya está inscrito.")

    # Simulación de verificación de pago
    if curso.precio > 0 and not pago_exitoso:
        raise Exception("Fallo de Transacción: Se requiere pago.")

    curso.inscritos.append(usuario_id)
    # Inicializa el progreso
    curso.progreso[usuario_id] = 0.0
    gestor_cursos._guardar_curso(curso)
    return True

def actualizar_progreso(curso_id: str, usuario_id: str, porcentaje: float):
    """Función de responsabilidad única: Actualiza el progreso del usuario (RF7)."""
    curso = gestor_cursos.obtener_por_id(curso_id)

    if not curso or usuario_id not in curso.inscritos:
        raise MatriculaInvalida("Usuario no matriculado o curso inexistente.")

    if porcentaje >= 100 and curso.progreso.get(usuario_id, 0) < 100:
        # Lógica de emisión de certificado al 100%
        cert = Certificado(usuario_id, curso_id, str(time.time()))
        gestor_cursos.guardar_certificado(cert)
        print(f"🎉 Certificado emitido para {usuario_id}. Enlace: {cert.generar_url_verificacion()}")

    curso.progreso[usuario_id] = min(porcentaje, 100.0)
    gestor_cursos._guardar_curso(curso)
