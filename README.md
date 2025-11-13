# MLOps Medical App — Flask Demo

Esta aplicación es una **simulación de un modelo médico** desarrollado en Flask.  
El objetivo es predecir un **estado de enfermedad** (leve, aguda, crónica o no enfermo) a partir de datos básicos del paciente.  
La lógica se implementa mediante reglas definidas en el archivo `rules.py`.

---

## Requisitos previos

- Tener instalado **Docker**.
- (Opcional para ejecución local) Tener instalado **Python 3.11** y `pip`.

---

## Construir la imagen Docker

Desde la raíz del proyecto (donde está el Dockerfile):

```bash
docker build -t mlops-medical-app .
```

Este comando levanta una imagen con python:3.11, instala flask, copia el codigo fuente necesario para la app y expone el puerto 8000.


## Ejecutar el contenedor Docker

```bash
docker run -p 8000:8000 mlops-medical-app
```

Este comando mapea el puerto local 8000 al del contenedor y disponibiliza la app para ser accedida desde el navegador.  
Opcionalmente, se puede utilizar el flag "-d" antes de "-p" para correr el contenedor en segundo plano, y el flag "--name" despues de asignar los puertos para asignar un nombre al contenedor. Es decir:


```bash
docker run -d -p 8000:8000 --name medical-app mlops-medical-app
```

Una vez la aplicación este corriendo, estará disponible en:
http://localhost:8000

---

## Funcionalidad - Como obtener resultados?

Una vez se encuentre en la aplicación, notará un formulario. Para obtener las predicciones/respuestas de la solución, por favor ingrese la información solicitada y presiona en el boton "predecir".

El endpoint principal `/predict` recibe los siguientes parámetros:

| Parámetro | Tipo | Descripción |
|------------|------|-------------|
| `age` | int | Edad del paciente |
| `severity` | float | Severidad de síntomas (0 a 10) |
| `duration_days` | int | Días de duración de los síntomas |

La respuesta contiene:
- El **estado clínico** estimado (`NO ENFERMO`, `LEVE`, `AGUDA`, `CRÓNICA`)
- Una **explicación textual**
- Los **valores de entrada** procesados

Puede realizar cuantas predicciones sean necesarias.