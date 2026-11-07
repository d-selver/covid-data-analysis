"""Optional charts for COVID-19 surveillance summaries."""

from pathlib import Path


def plot_country_cases(countries, output_path):
    """Save a horizontal bar chart of the ten countries with most reported cases."""
    import matplotlib.pyplot as plt

    top = sorted(countries, key=lambda row: row["cases"], reverse=True)[:10]
    if not top:
        raise ValueError("No country data available to plot")

    labels = [row["country"] for row in reversed(top)]
    values = [row["cases"] for row in reversed(top)]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(labels, values)
    ax.set_title("Top 10 countries by reported COVID-19 cases")
    ax.set_xlabel("Reported cases")
    ax.set_ylabel("Country")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def plot_age_group_cases(age_summary, output_path):
    """Save a bar chart of reported cases by age group."""
    import matplotlib.pyplot as plt

    cases = age_summary.get("cases_by_age_group", {})
    if not cases:
        raise ValueError("No age-group data available to plot")

    labels, values = list(cases.keys()), list(cases.values())
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(labels, values)
    ax.set_title("Reported COVID-19 cases by age group")
    ax.set_xlabel("Age group")
    ax.set_ylabel("Reported cases")
    ax.tick_params(axis="x", rotation=30)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path
