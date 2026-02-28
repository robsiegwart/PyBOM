import pytest
from pybom.repl import BomRepl, run_repl
from pybom import BOM


@pytest.fixture
def repl(bom_folder):
    bom = BOM.from_folder(str(bom_folder))
    return BomRepl(bom=bom, directory=str(bom_folder))


def test_tree_command_prints_part(repl, capsys):
    repl.onecmd('tree')
    captured = capsys.readouterr()
    assert 'P1' in captured.out


def test_help_command_lists_tree(bom_folder):
    import io
    bom = BOM.from_folder(str(bom_folder))
    buf = io.StringIO()
    r = BomRepl(bom=bom, directory=str(bom_folder), stdout=buf)
    r.onecmd('help')
    assert 'tree' in buf.getvalue()


def test_quit_returns_true(repl):
    result = repl.onecmd('quit')
    assert result is True


def test_eof_returns_true(repl):
    result = repl.onecmd('EOF')
    assert result is True


def test_empty_line_does_nothing(repl, capsys):
    repl.onecmd('')
    captured = capsys.readouterr()
    assert captured.out == ''


def test_unknown_command_prints_message(repl, capsys):
    repl.onecmd('foobar')
    captured = capsys.readouterr()
    assert 'Unknown command' in captured.out


def test_run_repl_exits_on_missing_files(tmp_path):
    with pytest.raises(SystemExit) as exc:
        run_repl(directory=str(tmp_path))
    assert exc.value.code == 1


def test_parts_shows_bom_parts(repl, capsys):
    repl.onecmd('parts')
    captured = capsys.readouterr()
    # P1, P2, P5, P7 are in the assembly; P3, P4, P6 are not
    assert 'P1' in captured.out
    assert 'P2' in captured.out
    assert 'P3' not in captured.out


def test_parts_shows_name_column(repl, capsys):
    repl.onecmd('parts')
    captured = capsys.readouterr()
    assert 'Bearing' in captured.out  # P1's Name


def test_assemblies_shows_root(repl, capsys):
    repl.onecmd('assemblies')
    captured = capsys.readouterr()
    assert 'Assembly' in captured.out


def test_assemblies_shows_name_from_sheet(nested_bom_folder, capsys):
    bom = BOM.from_folder(str(nested_bom_folder))
    r = BomRepl(bom=bom, directory=str(nested_bom_folder))
    r.onecmd('assemblies')
    captured = capsys.readouterr()
    assert 'Sub Assembly' in captured.out


def test_summary_shows_parts_with_qty(repl, capsys):
    repl.onecmd('summary')
    captured = capsys.readouterr()
    assert 'P1' in captured.out
    assert '2' in captured.out  # P1 QTY=2 in the assembly
