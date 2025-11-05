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
