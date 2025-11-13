# Punto 1 – Descripción del Pipeline de MLOps

## 1. Contexto del problema
El objetivo es desarrollar un **modelo de aprendizaje automático** que, a partir de los síntomas de un paciente, prediga la probabilidad de que padezca una enfermedad.  
Hay dos escenarios:
- **Enfermedades comunes:** gran cantidad de datos disponibles.  
- **Enfermedades huérfanas:** pocos datos, alto desbalance y riesgo de sobreajuste.

---

## 2. Diseño del pipeline (visión general)
A continuación se presenta el flujo completo **end-to-end**:


    [Ingesta de datos] 
           ↓
    [Procesamiento y limpieza]
           ↓
    [Análisis exploratorio]
           ↓
    [Entrenamiento y validación de modelos]
           ↓
    [Registro del modelo (Model Registry)]
           ↓
    [Despliegue en entorno de prueba / producción]
           ↓
    [Monitoreo y retraining]
