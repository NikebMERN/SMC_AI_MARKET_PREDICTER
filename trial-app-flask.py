from flask import Flask, render_template, request
import os
from pathlib import Path
from predict import predict_direction
import pandas as pd

app = Flask(__name__)

DATA_DIR = "data"


def list_currency_pairs():
    """List all CSV files in the data directory."""
    csv_files = list(Path(DATA_DIR).glob("*.csv"))
    return [file.name for file in csv_files]


def decide_action(confidence_scores):
    """Determine action from prediction confidence."""
    if not confidence_scores:
        return "Don't Enter"
    top_label, top_prob = max(confidence_scores.items(), key=lambda x: x[1])
    label = top_label.lower()
    if label in ["strong uptrend", "buy"]:
        return "Buy"
    elif label in ["strong downtrend", "sell"]:
        return "Sell"
    return "Don't Enter"


def calculate_tp_sl(file_path, action, tp_ratio=2, sl_ratio=1):
    df = pd.read_csv(file_path)
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


@app.route('/')
def home():
    files = list_currency_pairs()
    return render_template('index.html', datasets=files)


@app.route('/predict', methods=['POST'])
def predict():
    selected_file = request.form.get('selected_file')
    full_path = os.path.join(DATA_DIR, selected_file)

    if not os.path.exists(full_path):
        return f"❌ File {selected_file} not found.", 404

    try:
        results = predict_direction.predict_market_direction(full_path)
        prediction_data = []

        for prediction, confidence in results:
            action = decide_action(confidence)
            tp, sl = calculate_tp_sl(full_path, action)

            prediction_data.append({
                "prediction": prediction,
                "confidence": {k: f"{v * 100:.2f}%" for k, v in confidence.items()},
                "action": action,
                "tp": tp,
                "sl": sl
            })

        return render_template("result.html", file=selected_file, results=prediction_data)

    except Exception as e:
        return f"❌ Error: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
