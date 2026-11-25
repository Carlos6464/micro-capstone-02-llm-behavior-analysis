import random
import math
from collections import defaultdict


def review_queue(records, seed=42):
    required = [r for r in records if r["human_review_required"]]
    strata = defaultdict(list)
    for r in records:
        if not r["human_review_required"]:
            strata[r["prompt_id"], r["category"]].append(r)
    rng = random.Random(seed)
    for key in sorted(strata):
        group = sorted(strata[key], key=lambda r: r["execution_id"])
        required.extend(rng.sample(group, math.ceil(len(group) * 0.2)))
    return required
