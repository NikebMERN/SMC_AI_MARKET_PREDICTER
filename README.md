SMC Forex Predictor - Project Documentation
Prepared by: Nikodimos Elias G/Egziabher
Date: July 28, 2025

Table of Contents
1. Project Overview
2. File & Folder Structure
3. Concept: Smart Money Concept (SMC)
4. Backend Workflow
5. Technical Terms
6. Graph & Explanation
7. Additional Notes


1. Project Overview
The SMC Forex Predictor project is a Python-based system designed to analyze Forex market data using Smart Money Concepts (SMC). It utilizes a trained machine learning model to predict market direction (BUY, SELL, or NEUTRAL) based on extracted features from uploaded CSV files. The tool is integrated with a Telegram bot interface, providing user-friendly interaction.


2. File & Folder Structure
Each file and folder serves a specific role in the backend logic:

File/Folder
Description
app.py - Main Flask application for serving frontend/backend logic.
bot.py - Telegram bot interface to accept user inputs and return predictions.
features/create_features.py - Handles feature engineering and extraction from uploaded CSVs.
model/model.joblib - Serialized trained ML model used for making predictions.
model/label_encoder.joblib - Encodes/decodes class labels for prediction interpretation.
data/ - Stores user-uploaded CSV files temporarily.
utils/ - Houses additional utility functions (if any).


3. Concept: Smart Money Concept (SMC)
Smart Money Concept (SMC) is a trading approach that follows the actions of institutional investors (smart money) to identify market trends and turning points. The concept uses price action, liquidity sweeps, market structure shifts, and order blocks to determine potential buy/sell signals.


4. Backend Workflow

1. User uploads a CSV file or selects one via the Telegram bot.
2. The `extract_features` function processes the data to generate technical indicators.
3. Features are input into a trained machine learning model.
4. The model predicts the market direction and probability confidence.
5. The result is sent back to the user (via Telegram or frontend).


5. Technical Terms
- **CSV**: Comma-separated value file containing time-series market data.
- **SMA**: Simple Moving Average, a trend indicator.
- **SMC Trend**: Custom trend logic based on SMC trading strategy.
- **Label Encoder**: Maps string labels (BUY, SELL) to integers for model training.
- **Joblib**: Library for saving and loading machine learning models.


6. Graph & Explanation
In the extended version of the bot or frontend, graphs (candlestick charts, SMC zones) can be generated using `matplotlib` or `plotly`. These provide visual context to predictions and enhance user understanding.


7. Additional Notes
This system can be extended with:
- Real-time data fetching via APIs (e.g., Binance, OANDA)
- Integration with backtesting engines
- Portfolio management features
- Enhanced NLP explanation generation for summaries

Telegram-Bot: @SMCAIFXBOT
