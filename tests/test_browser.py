import pandas as pd
import pytest

from pybom import BOM
from pybom.browser import AssemblyScreen, BomBrowserApp, PartScreen


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def app(bom_folder):
    '''BomBrowserApp loaded from the standard flat bom_folder fixture.'''
    bom = BOM.from_folder(str(bom_folder))
    return BomBrowserApp(bom)



@pytest.fixture
def nested_app(nested_bom_folder):
    bom = BOM.from_folder(str(nested_bom_folder))
    return BomBrowserApp(bom)


# ---------------------------------------------------------------------------
# Initial state
# ---------------------------------------------------------------------------


async def test_initial_screen_is_assembly(app):
    async with app.run_test() as pilot:
        assert isinstance(app.screen, AssemblyScreen)


async def test_list_contains_root_children(app):
    # bom_folder assembly has 4 parts: P2, P1, P5, P7
    async with app.run_test() as pilot:
        from textual.widgets import ListItem
        items = app.screen.query(ListItem)
        assert len(items) == 4


async def test_subtitle_shows_bom_pn(app):
    async with app.run_test() as pilot:
        assert app.sub_title == 'Assembly'


# ---------------------------------------------------------------------------
# Part detail view
# ---------------------------------------------------------------------------


async def test_enter_on_part_pushes_part_screen(app):
    async with app.run_test() as pilot:
        await pilot.press('enter')  # first item (P2) is a part
        assert isinstance(app.screen, PartScreen)


async def test_part_screen_subtitle_contains_pn(app):
    async with app.run_test() as pilot:
        await pilot.press('enter')
        assert 'P2' in app.sub_title


async def test_part_screen_content_contains_pn(app):
    async with app.run_test() as pilot:
        await pilot.press('enter')
        from textual.widgets import Static
        content = app.screen.query_one(Static).content
        assert 'P2' in content


async def test_part_screen_content_contains_name(app):
    async with app.run_test() as pilot:
        await pilot.press('enter')  # P2 → Name: Board
        from textual.widgets import Static
        content = app.screen.query_one(Static).content
        assert 'Board' in content


# ---------------------------------------------------------------------------
# Navigation — back
# ---------------------------------------------------------------------------


async def test_escape_from_part_returns_to_assembly(app):
    async with app.run_test() as pilot:
        await pilot.press('enter')
        await pilot.press('escape')
        assert isinstance(app.screen, AssemblyScreen)


async def test_left_arrow_from_part_returns_to_assembly(app):
    async with app.run_test() as pilot:
        await pilot.press('enter')
        await pilot.press('left')
        assert isinstance(app.screen, AssemblyScreen)


async def test_escape_at_root_does_nothing(app):
    async with app.run_test() as pilot:
        await pilot.press('escape')
        assert isinstance(app.screen, AssemblyScreen)


async def test_q_quits(app):
    async with app.run_test() as pilot:
        await pilot.press('q')
    # If we reach here the app exited cleanly


# ---------------------------------------------------------------------------
# Assembly drill-down (nested fixture)
# ---------------------------------------------------------------------------


async def test_enter_on_assembly_pushes_assembly_screen(nested_app):
    # Top has [P1, Sub]; Sub is at index 1 — press Down then Enter
    async with nested_app.run_test() as pilot:
        await pilot.press('down')   # move selection to Sub
        await pilot.press('enter')
        assert isinstance(nested_app.screen, AssemblyScreen)


async def test_assembly_subtitle_updates_on_drill(nested_app):
    async with nested_app.run_test() as pilot:
        await pilot.press('down')
        await pilot.press('enter')
        assert nested_app.sub_title == 'Top > Sub'


async def test_escape_from_sub_assembly_returns_to_root(nested_app):
    async with nested_app.run_test() as pilot:
        await pilot.press('down')
        await pilot.press('enter')
        await pilot.press('escape')
        await pilot.pause()  # allow on_screen_resume to fire
        assert isinstance(nested_app.screen, AssemblyScreen)
        assert nested_app.sub_title == 'Top'


async def test_assembly_name_shown_in_list(nested_app):
    # The Sub assembly has sheet name 'Sub Assembly' — it should appear as its Name
    async with nested_app.run_test() as pilot:
        from textual.widgets import ListItem, Label
        labels = [lbl.content for lbl in nested_app.screen.query(Label)]
        assert any('Sub Assembly' in lbl for lbl in labels)
