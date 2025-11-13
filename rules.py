# rules.py
from dataclasses import dataclass

@dataclass
class PatientInput:
    age: int               # años
    severity: float        # severidad de síntomas 0–10
    duration_days: int     # duración de síntomas en días

# Estados posibles
NO_ENFERMO = "NO ENFERMO"
LEVE = "ENFERMEDAD LEVE"
AGUDA = "ENFERMEDAD AGUDA"
CRONICA = "ENFERMEDAD CRÓNICA"


def predict_state(inp: PatientInput) -> tuple[str, str]:
    """
    Reglas determinísticas para simular un modelo médico.

    Lógica (orden importante):
    - Si la duración > 30 días ⇒ CRÓNICA
    - Si severidad ≥ 6 y duración ≤ 30 ⇒ AGUDA
    - Si severidad ∈ [3,5] y duración ≤ 7 ⇒ LEVE
    - Si severidad ≤ 2 y duración ≤ 2 y edad < 65 ⇒ NO ENFERMO
    - En cualquier otro caso, por seguridad clínica mínima ⇒ LEVE

    Retorna: (estado, explicación)
    """
    age = inp.age
    sev = inp.severity
    dur = inp.duration_days

    # Validaciones básicas
    if age < 0 or dur < 0 or not (0 <= sev <= 10):
        raise ValueError("Entradas inválidas: age>=0, duration_days>=0, severity en [0,10].")

    if dur > 30:
        return CRONICA, "Síntomas prolongados (>30 días) sugieren condición crónica."

    if sev >= 6 and dur <= 30:
        return AGUDA, "Alta severidad con duración corta-media sugiere cuadro agudo."

    if 3 <= sev <= 5 and dur <= 7:
        return LEVE, "Severidad moderada y pocos días: cuadro leve y autolimitado probable."

    if sev <= 2 and dur <= 2 and age < 65:
        return NO_ENFERMO, "Síntomas muy leves y breves en persona <65 años; control expectante."

    return LEVE, "Caso fuera de reglas estrictas; se clasifica como leve por seguridad."