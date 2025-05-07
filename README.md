# FirmaApp - Sistema de Firmas Digitales para Constancias Médicas

**FirmaApp** es una aplicación desarrollada en Python para automatizar el proceso de firma de constancias de asistencia médica por parte de los pacientes. Este sistema fue diseñado para integrarse con el flujo de trabajo de clínicas u hospitales que usan plataformas como **Nesys**, y permite que, una vez descargado un documento PDF con la constancia de asistencia, el paciente pueda firmarlo digitalmente en una interfaz amigable y sencilla.

---

## 🧠 ¿Cómo funciona?

1. **Configuración inicial**: Al iniciar por primera vez, el sistema solicitará la configuración de dos rutas:
   - Carpeta de **origen**: donde el sistema escuchará la llegada de nuevos PDFs.
   - Carpeta de **destino**: donde se guardarán los PDFs después de firmarlos.

2. **Monitoreo automático**: El sistema se mantiene en segundo plano, vigilando la carpeta de descargas.

3. **Firma de documento**:
   - Cuando se detecta un archivo PDF cuyo nombre contiene el prefijo `CURL`, se lanza automáticamente una interfaz gráfica.
   - El paciente puede firmar con el mouse directamente en pantalla.
   - El sistema inserta la firma en el PDF y lo guarda en la carpeta destino.

---

## 📁 Estructura del Proyecto

```
    📁 firmaApp
    ├── 📁 assets
    ├── 📁 data
    │ └── firmaapp-prevrenal.db
    ├── 📁 logs
    │ └── app.log
    ├── 📁 src
    │ ├── 📁 core/
    │ │ ├── 📁controllers/
    │ │ │ └── rutas_controller.py
    │ │ ├── 📁models/
    │ │ │ └── rutas_models.py
    │ │ ├── 📁utils/
    │ │ │ ├── config.py
    │ │ │ ├── monitor.py
    │ │ │ ├── pdf_utils.py
    │ │ │ ├── setup_db.py
    │ │ │ └── logging_utils.py
    │ │ ├── app_logic.py
    │ │ ├── app.py
    │ │ └── bootstrap.py
    │ ├── 📁ui/
    │ │ └── 📁modules/
    │ │ ├── 📁firma/
    │ │ │ └── index.py
    │ │ └── 📁rutasconfig/
    │ │ └── index.py
    │ ├── main.py
    ├── requirements.txt
    ├── README.md
    ├── license.txt
    ├── .gitignore
```

🧪 Requisitos
Para ejecutar este proyecto, asegúrate de tener Python 3.9 o superior y los siguientes paquetes instalados (puedes instalarlos con pip install -r requirements.txt):

    - customtkinter

    - PyMuPDF (fitz)

    - Pillow

    - watchdog

    - sqlite3 (incluido en Python)

## 🚀 Instrucciones de Uso

    - Clona el repositorio: 
    git clone https://github.com/tu-usuario/firmaapp.git
    cd firmaapp

    -  Instala las dependencias:
    pip install -r requirements.txt

    - Ejecuta la aplicación:
    python main.py

    - Configura las rutas (solo la primera vez).
    Después de eso, el sistema se ejecutará de forma silenciosa y solo mostrará la ventana cuando haya un documento pendiente de firmar.

📦 Compilación a Ejecutable
    - Con consola
    pyinstaller main.py --name=FirmaApp --onefile --icon=assets/firmaAppIcono.ico

    - Sin consola
    pyinstaller main.py --name=FirmaApp --noconsole --onefile --icon=assets/firmaAppIcono.ico

🧑‍💻 Autor
    - Desarrollado por Jean Pierre Geovany Florez Desarrollador de sistemas
    Contacto:
        - GitHub: Jeanpiflorez
        - Correo: jeanpi.g.florez@gmail.com

📌 Proyecto desarrollado para
    - Este sistema fue desarrollado para [Digital Solutions Prevrena, Fundación Prevrenal], con el objetivo de digitalizar y automatizar la firma de constancias de asistencia médica, mejorando la eficiencia y trazabilidad del proceso en entornos clínicos.

🏥 Aplicación en entornos reales
    - FirmaApp está pensada para clínicas y centros médicos que requieren un sistema rápido y sin fricciones para validar la asistencia del paciente con firma digital.