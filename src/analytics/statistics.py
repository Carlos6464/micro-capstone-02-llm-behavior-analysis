import numpy as np


def paired_bootstrap(baseline, candidate, iterations=10000, seed=42):
    if set(baseline) != set(candidate) or not baseline:
        raise ValueError("Casos não pareados.")
    delta = np.array([candidate[k] - baseline[k] for k in sorted(baseline)])
    rng = np.random.default_rng(seed)
    samples = rng.choice(delta, size=(iterations, len(delta)), replace=True).mean(axis=1)
    return {"delta": float(delta.mean()), "ci95": np.percentile(samples, [2.5, 97.5]).tolist()}
