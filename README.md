# 📚 LMS - Plataforma de Cursos Online

## Descripción del Proyecto
Este repositorio contiene la implementación inicial (v0.1) de los módulos de Gestión de Usuarios y Gestión de Cursos para una Plataforma de Cursos en Línea (LMS - Learning Management System). El proyecto sigue una arquitectura de Microservicios y se desarrolla bajo estándares de Código Limpio y mejores prácticas de ingeniería de software.

## 💻 Tecnologías Utilizadas
* **Lenguaje:** Python 3.9+
* **Gestión de Dependencias:** pip
* **Testing:** unittest (Python built-in)
* **Calidad de Código/Linting:** flake8
* **CI/CD:** GitHub Actions

## ⚙️ Instrucciones de Instalación
Para clonar y ejecutar el proyecto localmente, sigue estos pasos:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/lms-plataforma-cursos.git](https://github.com/tu-usuario/lms-plataforma-cursos.git)
    cd lms-plataforma-cursos
    ```
2.  **Crear y activar un entorno virtual (Recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    # .\venv\Scripts\activate # En Windows
    ```
3.  **Instalar dependencias (asumiendo que necesitarás flake8 para linting):**
    ```bash
    pip install flake8
    ```

## ▶️ Guía de Uso
Los módulos principales (`gestion_usuarios.py` y `gestion_cursos.py`) contienen la lógica del negocio.

### Ejecutar Pruebas
Para validar la funcionalidad (requiere el archivo `tests/test_lms.py`):
```bash
python -m unittest tests/test_lms.py
