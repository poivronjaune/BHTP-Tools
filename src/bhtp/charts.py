import matplotlib.pyplot as plt

def view_chart(df):
    plt.figure(figsize=(12, 6))

    # Plot the full High series
    plt.plot(df.index, df['High'], label='High', color='black')

    # Detect peak indicator columns
    peak_columns = sorted([col for col in df.columns if col.startswith('is_peak')])

    # Setup colors and point sizes
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']
    base_size = 120
    size_step = 20

    # Precompute the number of peaks per row
    peak_counts = df[peak_columns].sum(axis=1)

    # Loop over each peak column and plot with vertical offset
    for i, col in enumerate(peak_columns):
        color = colors[i % len(colors)]
        size = base_size - i * size_step

        # Find where this peak is True
        is_peak_here = df[col]

        for idx in df[is_peak_here].index:
            high = df.loc[idx, 'High']
            overlap_count = peak_counts.loc[idx]

            # Determine offset based on the order of this peak among all peaks
            col_order = sum(df.loc[idx, peak_columns[:i]])  # How many True before this one
            offset = 0.15 * (overlap_count - col_order - 1)  # Stagger upward

            plt.scatter(
                idx,
                high + offset,
                label=col if idx == df[is_peak_here].index[0] else "",
                color=color,
                s=size,
                zorder=3,
                alpha=0.7,
                edgecolors='k'
            )

    # Draw down arrow and count for overlapping peaks
    overlapping_peaks = df[peak_counts > 1]

    for idx, row in overlapping_peaks.iterrows():
        high = row['High']
        count = int(peak_counts.loc[idx])

        # Arrow
        plt.annotate(
            '↓',
            (idx, high + 0.5 + 0.15 * count),
            color='black',
            fontsize=12,
            ha='center',
            va='bottom',
            zorder=4
        )

        # Number
        plt.annotate(
            str(count),
            (idx, high + 0.8 + 0.15 * count),
            color='black',
            fontsize=10,
            ha='center',
            va='bottom',
            zorder=4,
            weight='bold'
        )

    # === NEW: Draw lines for each segment ===
    if 'segment_id' in df.columns:
        segments = df.dropna(subset=['segment_id']).groupby('segment_id')
        for seg_id, group in segments:
            group = group.sort_index()
            if len(group) >= 2:
                start_idx = group.index[0]
                end_idx = group.index[-1]
                start_val = group.loc[start_idx, 'High']
                end_val = group.loc[end_idx, 'High']

                plt.plot(
                    [start_idx, end_idx],
                    [start_val, end_val],
                    color='green',
                    linestyle='--',
                    linewidth=2,
                    label='Trend Segment' if seg_id == segments.ngroups else ""
                )

    plt.legend()
    plt.title('Rolling Peak Detections (with Segments & Overlap Info)')
    plt.xlabel('Date')
    plt.ylabel('High Price')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def view_chart_2(df):
    # Hard coded for 3 peaks (5, 10, 30)
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['High'], label='High')
    # plt.scatter(df.index, df['Peak_High'], color='red', label='Peaks5', zorder=3)

    # Find all columns that are peak indicators
    peak_columns = [col for col in df.columns if col.startswith('is_peak')]

    # Define a color map for peak markers
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']
    
    base_size = 120  # starting point size
    size_step = 20   # how much smaller each next point gets

    for i, col in enumerate(peak_columns):
        color = colors[i % len(colors)]
        size = base_size - i * size_step
        peak_df = df[df[col]]
        #plt.scatter(peak_df.index, peak_df['High'], label=col, color=color, zorder=3)
        plt.scatter(
            peak_df.index,
            peak_df['High'],
            label=col,
            color=color,
            s=size,
            zorder=3,
            alpha=0.7,
            #edgecolors='k'
        )

    # Identify rows with more than one peak
    peak_counts = df[peak_columns].sum(axis=1)
    overlapping_peaks = df[peak_counts > 1]

    # Plot down arrows above overlapping peaks
    for idx, row in overlapping_peaks.iterrows():
        plt.annotate(
            '↓',
            (idx, row['High'] + 0.5),  # 0.5 offset; adjust based on your price scale
            color='black',
            fontsize=12,
            ha='center',
            va='bottom',
            zorder=4
        )

    plt.legend()
    plt.title('Rolling Peak Detections')
    plt.show()


def view_chart3(df):
    plt.figure(figsize=(12, 6))

    # Plot the High line
    plt.plot(df.index, df['High'], label='High', color='black')

    # Find all is_peak columns
    peak_columns = [col for col in df.columns if col.startswith('is_peak')]
    peak_columns = sorted(peak_columns)

    # Colors and marker sizes
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']
    base_size = 200
    size_step = 50

    # Plot each peak layer
    for i, col in enumerate(peak_columns):
        color = colors[i % len(colors)]
        size = base_size - i * size_step
        peak_df = df[df[col]]
        plt.scatter(
            peak_df.index,
            peak_df['High'],
            label=col,
            color=color,
            s=size,
            zorder=3,
            #alpha=0.7,
            #edgecolors='k'
        )

    # Identify rows with more than one peak
    peak_counts = df[peak_columns].sum(axis=1)
    overlapping_peaks = df[peak_counts > 1]

    for idx, row in overlapping_peaks.iterrows():
        high = row['High']
        count = int(peak_counts.loc[idx])

        # Plot arrow
        plt.annotate(
            '↓',
            (idx, high + 0.5),  # Arrow position
            color='black',
            fontsize=12,
            ha='center',
            va='bottom',
            zorder=4
        )

        # Plot number above the arrow
        plt.annotate(
            str(count),
            (idx, high + 1.2),  # Number above arrow
            color='black',
            fontsize=10,
            ha='center',
            va='bottom',
            zorder=4,
            weight='bold'
        )

    plt.legend()
    plt.title('Rolling Peak Detections (with Overlap Arrows and Counts)')
    plt.xlabel('Date')
    plt.ylabel('High Price')
    plt.grid(True)
    plt.tight_layout()
    plt.show()    

def view_chart3_bk(df):
    plt.figure(figsize=(12, 6))

    # Plot the full High series
    plt.plot(df.index, df['High'], label='High', color='black')

    # Detect peak indicator columns
    peak_columns = sorted([col for col in df.columns if col.startswith('is_peak')])

    # Setup colors and point sizes
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']
    base_size = 120
    size_step = 20

    # Precompute the number of peaks per row
    peak_counts = df[peak_columns].sum(axis=1)

    # Loop over each peak column and plot with vertical offset
    for i, col in enumerate(peak_columns):
        color = colors[i % len(colors)]
        size = base_size - i * size_step

        # Find where this peak is True
        is_peak_here = df[col]

        for idx in df[is_peak_here].index:
            high = df.loc[idx, 'High']
            overlap_count = peak_counts.loc[idx]

            # Determine offset based on the order of this peak among all peaks
            # Example: if this is the 2nd peak out of 3, apply smaller offset
            col_order = sum(df.loc[idx, peak_columns[:i]])  # How many True before this one
            offset = 0.15 * (overlap_count - col_order - 1)  # Stagger upward

            plt.scatter(
                idx,
                high + offset,
                label=col if idx == df[is_peak_here].index[0] else "",  # Avoid duplicate labels
                color=color,
                s=size,
                zorder=3,
                alpha=0.7,
                edgecolors='k'
            )

    # Draw down arrow and count for overlapping peaks
    overlapping_peaks = df[peak_counts > 1]

    for idx, row in overlapping_peaks.iterrows():
        high = row['High']
        count = int(peak_counts.loc[idx])

        # Arrow
        plt.annotate(
            '↓',
            (idx, high + 0.5 + 0.15 * count),
            color='black',
            fontsize=12,
            ha='center',
            va='bottom',
            zorder=4
        )

        # Number
        plt.annotate(
            str(count),
            (idx, high + 0.8 + 0.15 * count),
            color='black',
            fontsize=10,
            ha='center',
            va='bottom',
            zorder=4,
            weight='bold'
        )

    plt.legend()
    plt.title('Rolling Peak Detections (with Vertical Offsets & Overlap Counts)')
    plt.xlabel('Date')
    plt.ylabel('High Price')
    plt.grid(True)
    plt.tight_layout()
    plt.show()    