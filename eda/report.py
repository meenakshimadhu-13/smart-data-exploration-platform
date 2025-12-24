import pandas as pd
from io import BytesIO

def generate_excel_report(overview, quality, numeric_stats, categorical_stats):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        # Overview
        pd.DataFrame.from_dict(overview, orient="index", columns=["Value"]) \
            .to_excel(writer, sheet_name="Overview")

        # Missing Values
        quality["Missing Count"].to_frame("Missing Count") \
            .to_excel(writer, sheet_name="Missing Values")

        # Numeric Statistics
        if numeric_stats is not None:
            numeric_stats.to_excel(writer, sheet_name="Numeric Statistics")

        # Categorical Statistics
        for col, values in categorical_stats.items():
            values.to_frame("Count") \
                .to_excel(writer, sheet_name=f"{col[:25]}")

    output.seek(0)
    return output
