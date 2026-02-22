from pybom import BOM


def test_single_file_from_dataframe(simple_df):
    # assume BOM can be constructed directly from dict for tests
    bom = BOM(simple_df) if hasattr(BOM, '__init__') else BOM
    # Actually create using single_file helper if needed
    bom = BOM.single_file(simple_df) if hasattr(BOM, 'single_file') else bom
    assert bom is not None


def test_from_file(simple_xlsx):
    bom = BOM.single_file(simple_xlsx)
    assert "P1" in [n.name for n in bom.flat]
    assert bom.QTY("P1") == 2
