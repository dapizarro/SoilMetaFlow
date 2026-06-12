import json
from pathlib import Path
import pandas as pd

rows = []
for fp in snakemake.input:
    p = Path(fp)
    with open(p) as handle:
        data = json.load(handle)
    before = data["summary"]["before_filtering"]
    after = data["summary"]["after_filtering"]
    sample_unit = p.stem
    rows.append({
        "sample_unit": sample_unit,
        "total_reads_before": before.get("total_reads"),
        "total_bases_before": before.get("total_bases"),
        "q30_rate_before": before.get("q30_rate"),
        "gc_content_before": before.get("gc_content"),
        "total_reads_after": after.get("total_reads"),
        "total_bases_after": after.get("total_bases"),
        "q30_rate_after": after.get("q30_rate"),
        "gc_content_after": after.get("gc_content"),
        "retained_reads_pct": round(after.get("total_reads", 0) / before.get("total_reads", 1) * 100, 3)
    })

out = Path(snakemake.output[0])
out.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(out, sep="\t", index=False)
