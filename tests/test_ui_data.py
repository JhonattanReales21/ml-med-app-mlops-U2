import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import utils.ui_data as ui_data
from rules import PatientInput, predict_state
import json


## Test para función load_stats
# Al llamar la función load_stats sin contar con un archivo de predicciones
# existente, debe retornar estadísticas vacías.
def test_load_stats_no_file(tmp_path):
    # Redefinir LOG_FILE para usar un archivo temporal
    ui_data.LOG_FILE = tmp_path / "predictions_log.jsonl"

    stats = ui_data.load_stats()
    assert stats["total_by_state"] == {}
    assert stats["last_five"] == []
    assert stats["last_timestamp"] is None


## Test para función log_prediction
# Al registrar una predicción, el archivo se debe crear
# y debe contener la entrada correcta.
def test_log_prediction(tmp_path):
    # Redefinir LOG_FILE para usar un archivo temporal
    ui_data.LOG_FILE = tmp_path / "predictions_log.jsonl"

    patient = PatientInput(
        age=50,
        severity=5,
        duration_days=10,
        has_chronic_disease=False,
        has_metastasis=False,
        recent_weight_loss=False,
        is_bedridden=False,
        refractory_pain=False,
        multiple_organ_failure=False,
        has_recent_imaging=False,
    )

    state, explanation = predict_state(patient)

    ui_data.log_prediction(state, explanation, patient)

    # Verificar que el archivo se creó y contiene la entrada correcta
    assert ui_data.LOG_FILE.exists()
    with ui_data.LOG_FILE.open("r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert record["state"] == state
        assert record["explanation"] == explanation
        assert record["inputs"]["age"] == patient.age
