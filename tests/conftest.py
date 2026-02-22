import pandas as pd
import pytest


@pytest.fixture
def simple_df():
    # define a parts list and one assembly
    parts_list = pd.DataFrame(
        [
            {"PN": "P1", "Name": "Bearing"},
            {"PN": "P2", "Name": "Board"},
            {"PN": "P3", "Name": "Bracket"},
            {"PN": "P4", "Name": "Shaft"},
            {"PN": "P5", "Name": "Screw"},
            {"PN": "P6", "Name": "Wheel"},
            {"PN": "P7", "Name": "Nut"}
        ]
    )
    A1 = pd.DataFrame(
        [
            {"PN": "P2", "QTY": 1},
            {"PN": "P1", "QTY": 2},
            {"PN": "P5", "QTY": 2},
            {"PN": "P7", "QTY": 2},
        ]
    )
    return {"Parts list": parts_list, "Assembly": A1}


@pytest.fixture
def simple_xlsx(tmp_path, simple_df):
    fn = tmp_path / "bom.xlsx"
    with pd.ExcelWriter(fn, engine="openpyxl") as w:
        for name, df in simple_df.items():
            df.to_excel(w, sheet_name=name, index=False)
    return fn