# MLOps Medical App — Streamlit Demo

Esta aplicación es una **simulación de un modelo médico** desarrollada en Streamlit.  
El objetivo es predecir un **estado de enfermedad** (no enfermo, leve, aguda, crónica o terminal) a partir de datos básicos del paciente.  
La lógica se implementa mediante reglas definidas en el archivo `rules.py` y se registra el histórico de predicciones para generar un pequeño reporte.

> ⚠️ **Aviso:** Este proyecto es únicamente para fines educativos y de demostración de MLOps / prototipado.  
> No debe utilizarse para soporte real a la decisión clínica.

---

## 1. Estructura principal del proyecto

Archivos y carpetas principales:

- `app.py` → Aplicación web en **Streamlit**:
  - UI para captura de datos del paciente.
  - Llamada a la función de reglas (`predict_state`).
  - Registro de las predicciones en un archivo JSON Lines.
  - Vista de **reporte** (estadísticas + tabla de predicciones + descarga CSV).

- `rules.py` → Lógica de negocio / reglas determinísticas:
  - Define el dataclass `PatientInput`.
  - Implementa `predict_state(patient: PatientInput)` que devuelve:
    - El estado clínico (`NO ENFERMO`, `LEVE`, `ENFERMEDAD AGUDA`, `ENFERMEDAD CRÓNICA`, `ENFERMEDAD TERMINAL`).
    - Una explicación textual basada en las reglas activas.

- `utils/ui_data.py` → Funciones auxiliares de datos en la UI:
  - `log_prediction(...)` → Guarda cada predicción en `predictions_log.jsonl` (formato JSON Lines).
  - `load_stats()` → Lee el log y devuelve:
    - Conteo total de predicciones por estado.
    - Últimas 5 predicciones.
    - Timestamp de la última predicción.

- `utils/ui_style.py` → Estilos y layout de la interfaz:
  - Define una paleta de colores y estilos CSS inyectados en Streamlit.
  - Funciones:
    - `header()` → Título y texto introductorio de la app.
    - `style_cards()` y `style_sidebar()` → Estilo de tarjetas, sidebar y botones.

- `tests/` → Tests automatizados (Pytest):
  - `tests/test_rules.py` → Pruebas unitarias para `predict_state`:
    - Casos terminales, crónicos y entradas inválidas (deben lanzar `ValueError`).
  - `tests/test_ui_data.py` → Pruebas para `log_prediction` y `load_stats`.

- `.github/workflows/tests_workflow.yml` → Workflow de GitHub Actions:
  - Ejecuta los tests con `pytest` en cada *pull request* a `main`.

- `requirements.txt` → Dependencias de Python (Streamlit, Pandas, etc.).

- `Dockerfile` → Definición del contenedor Docker:
  - Basado en `python:3.11-slim`.
  - Copia el código, instala dependencias y expone la app Streamlit en el puerto **8000**.

- `pipeline.md` → Documento de apoyo describiendo el flujo de MLOps a nivel conceptual.

---

## 2. Requisitos previos

Puedes ejecutar el proyecto de dos formas:

### Opción A: Con Docker (recomendado para despliegue)

- Tener instalado **Docker**.

### Opción B: Localmente con Python

- **Python 3.11** (o compatible).
- `pip` para instalar dependencias.
- (Opcional) `git` para clonar el repositorio.
- (Opcional, para tests) `pytest`.

---

## 3. Ejecución local sin Docker

1. **Clonar el repositorio** (o descargar el código):

   ```bash
   git clone https://github.com/USER/ml-med-app-mlops-U2.git
   cd ml-med-app-mlops-U2
   ```

2. *(Opcional pero recomendado)* Crear y activar un entorno virtual:

   ```bash
   python -m venv .venv
   # En Windows
   .venv\Scriptsctivate
   # En macOS / Linux
   source .venv/bin/activate
   ```

3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. *(Opcional) Instalar herramientas de testing*:

   ```bash
   pip install pytest
   ```

5. **Ejecutar la aplicación Streamlit**:

   ```bash
   streamlit run app.py
   ```

   Por defecto, Streamlit levantará la app en:

   - http://localhost:8501  
     (o en otro puerto libre, por ejemplo http://localhost:8502)

---

## 4. Construir la imagen Docker

Desde la **raíz del proyecto** (donde está el `Dockerfile`):

```bash
docker build -t mlops-medical-app .
```

Este comando construye una imagen basada en `python:3.11-slim` que:

- Copia el código fuente de la app.
- Instala las dependencias definidas en `requirements.txt`.
- Configura Streamlit para levantar `app.py`.
- Expone el puerto **8000** dentro del contenedor.

---

## 5. Ejecutar el contenedor Docker

Para levantar la aplicación en un contenedor:

```bash
docker run -d -p 8000:8000 --name medical-app mlops-medical-app
```

- `-d` → Ejecuta el contenedor en segundo plano.
- `-p 8000:8000` → Mapea el puerto 8000 del host al 8000 del contenedor.
- `--name medical-app` → Asigna un nombre al contenedor.

Una vez la aplicación esté corriendo, estará disponible en:

- http://localhost:8000

---

## 6. Funcionalidad – ¿Cómo obtener resultados?

Al ingresar a la aplicación verás una **barra lateral** con dos vistas:

- **"Realizar predicción"**  
- **"Ver reporte"**

### 6.1. Vista "Realizar predicción"

1. Selecciona en la barra lateral **"Realizar predicción"**.
2. Completa el formulario con la información del paciente:

**Datos numéricos:**

| Parámetro         | Tipo   | Descripción                                              |
|-------------------|--------|----------------------------------------------------------|
| `Edad (años)`     | int    | Edad del paciente (0 a 120).                            |
| `Severidad`       | float  | Severidad de síntomas (0 a 10).                         |
| `Duración (días)` | int    | Días de duración de los síntomas (0 a 3650).            |

**Preguntas adicionales (checkboxes):**

- ¿El paciente tiene una **enfermedad crónica** diagnosticada?
- ¿Se conoce **enfermedad metastásica** o compromiso avanzado?
- ¿Ha tenido **pérdida de peso significativa** reciente?
- ¿Permanece la mayor parte del día **encamado** o con movilidad muy reducida?
- ¿Presenta **dolor intenso** pese a tratamiento analgésico adecuado?
- ¿Hay evidencia de **falla de más de un órgano mayor**?

**Imagen diagnóstica (opcional):**

- Se puede cargar una imagen **.jpg / .jpeg / .png** reciente.
- La app no “lee” la imagen, pero marca que existe y muestra una vista previa.

3. Haz clic en **"Predecir estado"**.

La respuesta mostrará:

- El **estado clínico estimado** (`NO ENFERMO`, `LEVE`, `ENFERMEDAD AGUDA`, `ENFERMEDAD CRÓNICA`, `ENFERMEDAD TERMINAL`).
- Una **explicación textual** basada en las reglas activadas.
- Un bloque con el **detalle de los datos de entrada** (`st.json`).
- Un mensaje adicional si se cargó una imagen diagnóstica (recordatorio de revisión manual).
- Un botón **"Nueva predicción"** para limpiar el formulario y volver a empezar.

Además:

- Cada predicción se registra en `predictions_log.jsonl`.
- Desde la misma vista se puede **descargar un CSV** con el histórico de predicciones (botón "Descargar listado de predicciones").

---

## 7. Vista "Ver reporte"

En la barra lateral, selecciona **"Ver reporte"**.

En esta vista se leen las predicciones del archivo `predictions_log.jsonl` (a través de `load_stats()`) y se muestran:

1. Un selector de vista:

   - **"Estadísticas"**  
     - Número total de predicciones por categoría (estado).
     - Listado de las **últimas 5 predicciones** (más reciente primero) con:
       - Timestamp.
       - Estado predicho.
       - Edad, severidad y duración del caso.
     - Fecha/hora de la última predicción registrada.

   - **"Predicciones"**  
     - Tabla completa (`st.dataframe`) con todas las predicciones leídas del archivo de log.

2. Si todavía no hay predicciones registradas, la app muestra un mensaje informativo pidiendo realizar al menos una predicción.

---

## 8. Tests automatizados y CI/CD

Para ejecutar los tests localmente:

```bash
pytest -v
```

Los tests cubren:

- **Lógica de reglas (`rules.py`)**:
  - Casos que deben clasificar como **ENFERMEDAD TERMINAL** y **CRÓNICA** según la combinación de variables.
  - Comportamiento ante **entradas inválidas** (por ejemplo, severidad fuera de [0, 10] o duración negativa) → deben lanzar `ValueError` con un mensaje específico.

- **Módulo de datos para la UI (`utils/ui_data.py`)**:
  - `load_stats()` sin archivo previo → retorna estadísticas vacías.
  - `log_prediction()` → crea el archivo `predictions_log.jsonl` y registra correctamente el contenido.

En GitHub, el workflow `.github/workflows/tests_workflow.yml`:

- Instala las dependencias (`pip install -r requirements.txt`).
- Instala `pytest`.
- Ejecuta los tests en cada **pull request** contra `main`.
- Comenta en el PR cuando la CI/CD termina con éxito.

---

## 9. Notas finales

- Este proyecto está orientado a practicar conceptos de **MLOps y prototipado rápido** con Streamlit, más que a un modelo de ML entrenado con datos reales.
- La lógica se basa en **reglas determinísticas** para facilitar la explicación y el testeo.
- Puedes extender el proyecto para:
  - Reemplazar las reglas por un modelo de ML real.
  - Integrar un Model Registry (MLflow, SageMaker, etc.).
  - Conectar la app a una API externa o a un pipeline de datos real.

---

Demo desarrollada para fines educativos.
