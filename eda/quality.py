def data_quality(df):
    return {
        "Missing Count": df.isnull().sum(),
        "Missing Percentage": (df.isnull().mean() * 100).round(2),
        "Duplicate Rows": df.duplicated().sum()
    }
