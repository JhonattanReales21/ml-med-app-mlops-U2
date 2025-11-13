# app.py
from flask import Flask, request, jsonify, render_template
from rules import PatientInput, predict_state

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True)
        if data is None:
            # También soporta form-data (desde el HTML)
            data = {
                "age": request.form.get("age", type=int),
                "severity": request.form.get("severity", type=float),
                "duration_days": request.form.get("duration_days", type=int),
            }

        age = int(data["age"]) if data.get("age") is not None else None
        severity = float(data["severity"]) if data.get("severity") is not None else None
        duration_days = int(data["duration_days"]) if data.get("duration_days") is not None else None

        if age is None or severity is None or duration_days is None:
            return jsonify({"error": "Faltan parámetros: age, severity, duration_days"}), 400

        state, explanation = predict_state(PatientInput(age=age, severity=severity, duration_days=duration_days))
        return jsonify({
            "state": state,
            "explanation": explanation,
            "inputs": {"age": age, "severity": severity, "duration_days": duration_days}
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    # Para desarrollo local (no en Docker)
    app.run(host="0.0.0.0", port=8000, debug=True)