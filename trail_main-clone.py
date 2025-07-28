import sys
import os
import pandas as pd  # type: ignore
from utils.preprocess_data import preprocess_data
from smc_indicators.trend_detector import detect_trend
from smc_indicators.support_resistance import find_support_resistance
from smc_indicators.market_structure import detect_swings, label_market_structure, identify_market_trend_from_labels
from smc_indicators.bos_detector import detect_bos
from smc_indicators.fvg_detector import detect_fvg
from smc_indicators.order_blocks import detect_order_blocks
from smc_indicators.liquidity_pools import detect_liquidity_pools_with_time  # Add this import if the function exists

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Step 1: Preprocess local CSV data
df = preprocess_data("data/EURCHF_5min.csv")

# Step 2: Detect trend using SMA
trend = detect_trend(df)
print(f"📊 SMA-based Detected Trend: {trend}")

# Step 3: Detect support and resistance levels
support_levels, resistance_levels = find_support_resistance(df)

# Step 4: Print support and resistance levels
print("\n📉 Support Levels:")
for time, price in support_levels:
    time_str = time.strftime('%Y-%m-%d %H:%M:%S') if hasattr(time, 'strftime') else str(time)
    print(f"  - {time_str} → {price:.5f}")

print("\n📈 Resistance Levels:")
for time, price in resistance_levels:
    time_str = time.strftime('%Y-%m-%d %H:%M:%S') if hasattr(time, 'strftime') else str(time)
    print(f"  - {time_str} → {price:.5f}")

# Step 5: Detect market structure swings
swings = detect_swings(df)

# Step 6: Label swings as HH, HL, LH, LL
labeled_swings = label_market_structure(swings)

# Step 7: Identify market trend based on labeled market structure swings
smc_trend = identify_market_trend_from_labels(labeled_swings)
print(f"\n🔍 Market Structure Detected Trend: {smc_trend}")

# Step 8: Filter swings in the last 10 hours
latest_time = df.index[-1]
cutoff_time = latest_time - pd.Timedelta(hours=10)
recent_swings = [s for s in labeled_swings if s['index'] >= cutoff_time]

print("\n🌀 Market Structure Swings in the Last 10 Hours:")
for s in recent_swings:
    idx_str = s['index'].strftime('%Y-%m-%d %H:%M:%S') if hasattr(s['index'], 'strftime') else str(s['index'])
    print(f"  - {idx_str} | {s['label']} ({s['type'].capitalize()}) at {s['price']:.5f}")

# Step 9: Detect Break Of Structure (BOS) events
labeled_swings_df = pd.DataFrame(labeled_swings)
# print(labeled_swings_df)

# Ensure index column exists for slicing purposes
if 'index' not in labeled_swings_df.columns:
    labeled_swings_df['index'] = labeled_swings_df.index

# Ensure proper index for the candles dataframe
df.reset_index(drop=False, inplace=True)  # Make timestamp a column, not index

# Run BOS detection
bos_events = detect_bos(labeled_swings_df, df)

print("\n⚡ Break of Structure (BOS) Events Detected:")
if bos_events:
    for bos in bos_events:
        ts = bos['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if hasattr(bos['timestamp'], 'strftime') else str(bos['timestamp'])
        print(f"  - {bos['type']} at {bos['price']:.5f} on {ts}")
else:
    print("  - No BOS events detected.")

# Step 10: Detect FVGs from your candlestick data (e.g., 'df')
fvg_df = detect_fvg(df)

print(f"Detected {len(fvg_df)} FVGs")
print(fvg_df.tail())

# Step 11: Detect OB's from the candel stick pattern
order_blocks = detect_order_blocks(df)

print(f"Detected {len(order_blocks)} Order Blocks")
print(order_blocks)

# Step 12: Find liquidity pools
# Assume `labeled_swings_df` contains your swing highs/lows
if 'timestamp' not in labeled_swings_df.columns:
    if 'index' in labeled_swings_df.columns:
        labeled_swings_df['timestamp'] = labeled_swings_df['index']
    else:
        print("ERROR: No timestamp or index column found in swings dataframe")

liquidity_pools_df = detect_liquidity_pools_with_time(labeled_swings_df)
print(liquidity_pools_df)