from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore
import os
import pandas as pd
from predict.predict_direction import predict_market_direction

app = Flask(__name__)
CORS(app)  #! Enable CORS for all routes

DATA_FOLDER = "data"

def decide_action(confidence_scores):
    """Determine trading action based on model's confidence scores."""
    if not confidence_scores:
        return "Don't Enter"

    top_label, top_prob = max(confidence_scores.items(), key=lambda x: x[1])

    label = top_label.lower()
    if label in ["strong uptrend", "buy"]:
        return "Buy"
    elif label in ["strong downtrend", "sell"]:
        return "Sell"
    else:
        return "Don't Enter"

def calculate_tp_sl(csv_file_path, action, tp_ratio=2, sl_ratio=1):
    """Calculate TP and SL based on the latest close price."""
    df = pd.read_csv(csv_file_path)

    if df.empty or "Close" not in df.columns:
        return None, None

    last_close = df["Close"].iloc[-1]

    if action == "Buy":
        sl = last_close - (last_close * (sl_ratio / 100))
        tp = last_close + (last_close * (tp_ratio / 100))
    elif action == "Sell":
        sl = last_close + (last_close * (sl_ratio / 100))
        tp = last_close - (last_close * (tp_ratio / 100))
    else:
        return None, None

    return round(tp, 5), round(sl, 5)

@app.route("/")
def index():
    return jsonify({
        "message": "Welcome to the SMC Forex Predictor API.",
        "endpoints": {
            "GET /data": "List available data files",
            "POST /predict": "Send filename to get market prediction"
        }
    })

@app.route("/data", methods=["GET"])
def list_data_files():
    try:
        files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]
        return jsonify({"available_files": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        filename = data.get("filename")

        if not filename:
            return jsonify({"error": "Filename is required."}), 400

        filepath = os.path.join(DATA_FOLDER, filename)

        if not os.path.exists(filepath):
            return jsonify({"error": f"File '{filename}' not found."}), 404

        # Run prediction
        results = predict_market_direction(filepath)

        response = []
        for label, confidence_scores in results:
            action = decide_action(confidence_scores)
            tp, sl = calculate_tp_sl(filepath, action)

            response.append({
                "prediction": label,
                "confidence": {k: round(v * 100, 2) for k, v in confidence_scores.items()},
                "action": action,
                "take_profit": tp,
                "stop_loss": sl
            })

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
