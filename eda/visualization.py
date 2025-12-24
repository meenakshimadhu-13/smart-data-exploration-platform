import matplotlib.pyplot as plt
import seaborn as sns

def sample_data(df, max_rows=20000):
    if len(df) > max_rows:
        return df.sample(max_rows, random_state=42)
    return df

def plot_numeric(df, column, plot_type):
    fig, ax = plt.subplots()
    if plot_type == "Histogram":
        df[column].plot(kind="hist", bins=30, ax=ax)
    elif plot_type == "Box Plot":
        sns.boxplot(x=df[column], ax=ax)
    elif plot_type == "Line Plot":
        df[column].plot(kind="line", ax=ax)
    ax.set_title(f"{plot_type} of {column}")
    return fig

def plot_categorical(df, column):
    fig, ax = plt.subplots()
    df[column].value_counts().head(10).plot(kind="bar", ax=ax)
    ax.set_title(f"Top Categories in {column}")
    return fig
