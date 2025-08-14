import pandas as pd
from typing import List, Dict

def make_validation_excel(out_path: str, toc_entries: List[Dict], spec_entries: List[Dict]):
    toc_df = pd.DataFrame(toc_entries)
    spec_df = pd.DataFrame(spec_entries)

    if toc_df.empty:
        summary = pd.DataFrame({"metric": ["toc_sections_parsed"], "value": [0]})
        with pd.ExcelWriter(out_path, engine="openpyxl") as w:
            summary.to_excel(w, index=False, sheet_name="summary")
        return

    if spec_df.empty:
        summary = pd.DataFrame({"metric": ["toc_sections_parsed", "parsed_sections"], "value": [len(toc_df), 0]})
        with pd.ExcelWriter(out_path, engine="openpyxl") as w:
            summary.to_excel(w, index=False, sheet_name="summary")
        return

    missing = toc_df[~toc_df["section_id"].isin(spec_df["section_id"])]
    extra = spec_df[~spec_df["section_id"].isin(toc_df["section_id"])]
    common = set(toc_df["section_id"]).intersection(set(spec_df["section_id"]))

    summary = pd.DataFrame({
        "metric": ["toc_sections_parsed", "parsed_sections", "common_sections", "missing_in_parsed", "extra_in_parsed"],
        "value": [len(toc_df), len(spec_df), len(common), len(missing), len(extra)]
    })

    with pd.ExcelWriter(out_path, engine="openpyxl") as w:
        summary.to_excel(w, index=False, sheet_name="summary")
        if not missing.empty:
            missing.to_excel(w, index=False, sheet_name="missing_in_parsed")
        if not extra.empty:
            extra.to_excel(w, index=False, sheet_name="extra_in_parsed")
