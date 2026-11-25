import json
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Autor: Carlos Adriano
# Data: 25/11/2026
# Descrição: Exporta indicadores CSV, resumo JSON e gráfico SGD.
def report(rows, directory: Path):
    directory.mkdir(parents=True, exist_ok=True)
    table = pd.json_normalize(rows)
    table.to_csv(directory / "strategy_metrics.csv", index=False)
    (directory / "decision_summary.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    valid = table.dropna(subset=["sgd"])
    if not valid.empty:
        fig, ax = plt.subplots()
        ax.bar(valid["prompt_id"], valid["sgd"])
        ax.set_ylim(0, 100)
        ax.set_ylabel("SGD")
        fig.savefig(directory / "sgd.png", bbox_inches="tight")
        plt.close(fig)
