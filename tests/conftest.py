import pandas as pd
import pytest


@pytest.fixture
def simple_df():
    # One assembly, flat (no sub-assemblies)
    parts_list = pd.DataFrame([
        {"PN": "P1", "Name": "Bearing"},
        {"PN": "P2", "Name": "Board"},
        {"PN": "P3", "Name": "Bracket"},
        {"PN": "P4", "Name": "Shaft"},
        {"PN": "P5", "Name": "Screw"},
        {"PN": "P6", "Name": "Wheel"},
        {"PN": "P7", "Name": "Nut"},
    ])
    assembly = pd.DataFrame([
        {"PN": "P2", "QTY": 1},
        {"PN": "P1", "QTY": 2},
        {"PN": "P5", "QTY": 2},
        {"PN": "P7", "QTY": 2},
    ])
    return {"Parts list": parts_list, "Assembly": assembly}


@pytest.fixture
def simple_xlsx(tmp_path, simple_df):
    fn = tmp_path / "bom.xlsx"
    with pd.ExcelWriter(fn, engine="openpyxl") as w:
        for name, df in simple_df.items():
            df.to_excel(w, sheet_name=name, index=False)
    return fn


@pytest.fixture
def nested_df():
    # Top assembly references a sub-assembly (Sub) used 2 times.
    # Expected aggregates: P1=1, P2=3*2=6, P3=1*2=2
    parts_list = pd.DataFrame([
        {"PN": "P1", "Name": "Bearing"},
        {"PN": "P2", "Name": "Board"},
        {"PN": "P3", "Name": "Bracket"},
    ])
    top = pd.DataFrame([
        {"PN": "P1", "QTY": 1},
        {"PN": "Sub", "QTY": 2},
    ])
    sub = pd.DataFrame([
        {"PN": "P2", "QTY": 3},
        {"PN": "P3", "QTY": 1},
    ])
    return {"Parts list": parts_list, "Top": top, "Sub": sub}


@pytest.fixture
def bom_folder(tmp_path, simple_df):
    # Multi-file layout: Parts list.xlsx + Assembly.xlsx
    with pd.ExcelWriter(tmp_path / "Parts list.xlsx", engine="openpyxl") as w:
        simple_df["Parts list"].to_excel(w, index=False)
    with pd.ExcelWriter(tmp_path / "Assembly.xlsx", engine="openpyxl") as w:
        simple_df["Assembly"].to_excel(w, index=False)
    return tmp_path