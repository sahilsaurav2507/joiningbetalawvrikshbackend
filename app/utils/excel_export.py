import pandas as pd
from typing import List

def export_to_excel(rows: List[dict], filename: str) -> str:
    df = pd.DataFrame(rows)
    df.to_excel(filename, index=False)
    return filename 