import yfinance as yf
import pandas as pd
from bhtp import yahoo


def detect_peaks(df, window=5, lag=2, price_col="High"):
    df = df.copy()
    df = df.sort_index()

    # Rolling max over the future window (shift back by lag to compare)
    rolling_max = df[price_col].shift(-lag).rolling(window=window, min_periods=window).max()
    # Detect peaks: current value == max in the future window
    df[f'is_peak_{window}'] = df[price_col] == rolling_max

    return df


def detect_peaks_rolling_max_lag(df, window=5, lag=2, price_col='High'):
    
    df = df.copy()
    df = df.sort_index()

    # Rolling max over the future window (shift back by lag to compare)
    #rolling_max = df[price_col].shift(-lag).rolling(window=window, min_periods=1).max()
    rolling_max = df[price_col].shift(-lag).rolling(window=window, min_periods=1).max()
    # Detect peaks: current value == max in the future window
    df['is_peak'] = df[price_col] == rolling_max
    df[f'Peak_{price_col}'] = df[price_col].where(df['is_peak'])

    return df


def assign_higher_high_segments(df, peak_col='is_peak_10'):
    df = df.copy()
    df['segment_id'] = pd.NA

    # Extract peak rows
    peaks = df[df[peak_col]].copy()
    peaks = peaks.sort_index()

    current_segment = []
    segment_counter = 0

    for i in range(len(peaks)):
        idx = peaks.index[i]
        high = peaks.loc[idx, 'High']

        if not current_segment:
            current_segment = [(idx, high)]
        else:
            _, last_high = current_segment[-1]
            if high > last_high:
                current_segment.append((idx, high))
            else:
                if len(current_segment) >= 2:
                    segment_counter += 1
                    for seg_idx, _ in current_segment:
                        df.loc[seg_idx, 'segment_id'] = segment_counter
                current_segment = [(idx, high)]

    # Final segment
    if len(current_segment) >= 2:
        segment_counter += 1
        for seg_idx, _ in current_segment:
            df.loc[seg_idx, 'segment_id'] = segment_counter

    return df


def add_segment_bounds(df, segment_col='segment_id'):
    df = df.copy()
    df['segment_low'] = pd.NA
    df['segment_high'] = pd.NA

    if segment_col not in df.columns:
        raise ValueError(f"Missing '{segment_col}' column. Run assign_higher_high_segments first.")

    grouped = df.dropna(subset=[segment_col]).groupby(segment_col)

    for seg_id, group in grouped:
        low = group['High'].min()
        high = group['High'].max()
        df.loc[group.index, 'segment_low'] = low
        df.loc[group.index, 'segment_high'] = high

    return df



if __name__ == "__main__":
    symbols = ['TSLA']
    data = yahoo.download_daily_data(symbols, start_dt='2020-01-01')
    data = yahoo.flatten_dataframe(data)
    #data = detect_peaks(data, window=5)
    data = detect_peaks(data, window=10)
    #data = detect_peaks(data, window=30)
    #data = detect_peaks(data, window=365)
    data = assign_higher_high_segments(data, peak_col='is_peak_10')
    data = add_segment_bounds(data)
    
    print(data)
    print("=============================")
    
    from bhtp import charts
    charts.view_chart(data)