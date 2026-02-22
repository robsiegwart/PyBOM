import subprocess
import sys

def test_cli_single_file(simple_xlsx, tmp_path):
    proc = subprocess.run(
        [sys.executable, "-m", "pybom", "-f", str(simple_xlsx), "summary"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "P1" in proc.stdout
