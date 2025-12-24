def dataset_overview(df):
    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Memory Usage (MB)": round(df.memory_usage(deep=True).sum() / 1024**2, 2),
        "Column Names": list(df.columns)
    }
