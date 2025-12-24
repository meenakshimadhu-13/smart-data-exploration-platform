import numpy as np

def get_column_types(df):
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()
    return numeric_cols, categorical_cols

def numeric_statistics(df, numeric_cols):
    return df[numeric_cols].describe()

def categorical_statistics(df, categorical_cols):
    stats = {}
    for col in categorical_cols:
        stats[col] = df[col].value_counts().head(10)
    return stats
