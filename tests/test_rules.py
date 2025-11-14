import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from rules import PatientInput, predict_state, TERMINAL, CRONICA


## Test para condición terminal:
# Dado un paciente con múltiples banderas rojas y sintomas
# de alta gravedad, este debe ser clasificado como TERMINAL.
def test_terminal_condition():
    patient = PatientInput(
        age=80,
        severity=9,
        duration_days=200,
        has_chronic_disease=True,
        has_metastasis=True,
        recent_weight_loss=True,
        is_bedridden=False,
        refractory_pain=False,
        multiple_organ_failure=True,
        has_recent_imaging=True,
    )

    state, explanation = predict_state(patient)
    assert state == TERMINAL


## Test para condicion cronica:
# Dado un paciente con enfermedad crónica y mas de 30 días de síntomas,
# este debe ser clasificado como CRONICA.
def test_chronic_condition():
    patient = PatientInput(
        age=60,
        severity=5,
        duration_days=45,
        has_chronic_disease=True,
        has_metastasis=False,
        recent_weight_loss=False,
        is_bedridden=False,
        refractory_pain=False,
        multiple_organ_failure=False,
        has_recent_imaging=False,
    )

    state, explanation = predict_state(patient)
    assert state == CRONICA


##  Test para entradas inválidas:
# Al proporcionar entradas inválidas, la función debe
# lanzar una excepción ValueError.
def test_invalid_inputs():
    patient = PatientInput(
        age=-5,  # Edad inválida
        severity=11,  # Severidad inválida
        duration_days=-10,  # Duración inválida
        has_chronic_disease=False,
        has_metastasis=False,
        recent_weight_loss=False,
        is_bedridden=False,
        refractory_pain=False,
        multiple_organ_failure=False,
        has_recent_imaging=False,
    )

    try:
        predict_state(patient)
        assert False, "Se esperaba una excepción ValueError por entradas inválidas."
    except ValueError as e:
        assert (
            str(e)
            == "Entradas inválidas: age>=0, duration_days>=0, severity en [0,10]."
        )
