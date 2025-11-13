# app.py
import streamlit as st
from rules import PatientInput, predict_state

# Configuración básica de la página
st.set_page_config(
    page_title="Clasificador de Enfermedades",
    page_icon="🏥",
    layout="centered",
)

st.title("Clasificador de Enfermedades")
st.write(
    """
Esta aplicación simula un **modelo médico basado en reglas**.
Ingresa los datos del paciente y obtendrás un estado estimado junto con una breve explicación.
"""
)

# --- Formulario de entrada ---
with st.form("patient_form"):
    age = st.number_input("Edad (años)", min_value=0, max_value=120, value=30, step=1)
    severity = st.slider(
        "Severidad de síntomas (0–10)",
        min_value=0.0,
        max_value=10.0,
        value=4.0,
        step=0.1,
    )
    duration_days = st.number_input(
        "Duración de los síntomas (días)", min_value=0, max_value=365, value=3, step=1
    )

    submitted = st.form_submit_button("Predecir")

# --- Lógica de predicción ---
if submitted:
    try:
        patient = PatientInput(
            age=int(age),
            severity=float(severity),
            duration_days=int(duration_days),
        )
        state, explanation = predict_state(patient)

        if state == "NO ENFERMO":
            st.success(f"✅ Estado estimado: **{state}**")
        elif state in ["ENFERMEDAD CRÓNICA", "ENFERMEDAD AGUDA"]:
            st.error(f"❗️ Estado estimado: **{state}**")
        else:
            st.info(f"🔵 Estado estimado: **{state}**")

        st.markdown(f"**Explicación:** {explanation}")

        with st.expander("Ver detalle de los datos de entrada"):
            st.json(
                {
                    "age": patient.age,
                    "severity": patient.severity,
                    "duration_days": patient.duration_days,
                }
            )

    except Exception as e:
        st.error(f"⚠️ Ocurrió un error al calcular la predicción: {e}")

st.markdown("---")
st.caption(
    "Lógica de clasificación definida en `rules.py`. "
    "Este demo es únicamente educativo y **no** reemplaza criterio médico profesional."
)
