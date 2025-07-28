import subprocess
from pathlib import Path
from predict import predict_direction
import pandas as pd


def run_script(script_path):
    """Run a Python script and handle errors."""
    print(f"🚀 Running: {script_path}")
    try:
        subprocess.run(["python", script_path], check=True)
        print(f"✅ Completed: {script_path}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run {script_path}\nError: {e}")
        exit(1)


def list_currency_pairs(data_dir):
    """List all available CSV files (currency pairs)."""
    print("📂 Available currency pairs:\n")
    csv_files = list(Path(data_dir).glob("*.csv"))
    for idx, file in enumerate(csv_files, start=1):
        print(f"{idx}. {file.stem}")
    return csv_files


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


def main():
    print("📈 Welcome to SMC Forex Predictor!\n")

    # Optional steps
    # print("🔄 Running optional scripts...")
    # print("Creating features...")
    # run_script("features/create_features.py")

    # print("Training model...")
    # run_script("model/train_model.py")

    # print("Evaluating model...")
    # run_script("model/evaluate_model.py")

    # Select data
    data_dir = "data"
    csv_files = list_currency_pairs(data_dir)

    try:
        choice = int(input("\n🔢 Enter the number of the currency pair you want to predict: "))
        selected_file = csv_files[choice - 1]
    except (ValueError, IndexError):
        print("❌ Invalid choice. Exiting.")
        return

    print(f"\n🔍 Predicting trend for: {selected_file.stem}")
    results = predict_direction.predict_market_direction(str(selected_file))

    for prediction, confidence in results:
        print(f"\n📊 Prediction: {prediction}")

        if confidence:
            print("📈 Confidence Scores:")
            for label, prob in confidence.items():
                print(f"  - {label}: {prob * 100:.2f}%")

            action = decide_action(confidence)
            print(f"\n🚦 Final Action: {action}")

            # ✅ Add TP and SL calculation
            tp, sl = calculate_tp_sl(str(selected_file), action)
            if tp is not None and sl is not None:
                print(f"🎯 Take Profit: {tp}")
                print(f"🛡️ Stop Loss: {sl}")
            else:
                print("⚠️ Could not calculate TP/SL.")
        else:
            print("⚠️ No confidence data available. Default action: Don't Enter")


if __name__ == "__main__":
    main()
