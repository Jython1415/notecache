"""Tests for cache.py"""

import tempfile
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd
import hypothesis as hp
import hypothesis.strategies as st

import notecache

st_integer_or_text = st.one_of(st.integers(), st.text())
st_df_3x3 = st.just(pd.DataFrame(np.arange(1, 10).reshape(3, 3)))
st_any_object = st.one_of(
    st_integer_or_text,
    st_df_3x3,
    st.dictionaries(st_integer_or_text, st_integer_or_text),
)


def _assert_object_equals(left: Any, right: Any) -> None:
    """
    Checks if two objects based on `st_any_object` are equal. Has logic to
    make sure data frames are compared correctly.

    :param left: the first value to compare.
    :param right: the second value to compare.
    """

    if isinstance(left, pd.DataFrame):
        assert left.equals(right)
    elif isinstance(right, pd.DataFrame):
        assert right.equals(left)
    else:
        assert left == right


@hp.given(obj_to_store=st_any_object)
def test_load_object_storage(obj_to_store) -> None:
    """
    Tests the load function with various objects.
    """

    with tempfile.TemporaryDirectory(dir=Path.cwd()) as dir_name:
        folder = Path(dir_name)

        def generate(_) -> Any:
            return obj_to_store

        load1 = notecache.load(None, generate, "", folder=folder)
        load2 = notecache.load(None, generate, "", folder=folder)
        _assert_object_equals(obj_to_store, load1.object)
        _assert_object_equals(obj_to_store, load2.object)
        assert not load2.generated
        assert not load2.state_change


@hp.given(state=st_any_object)
def test_load_state_usage(state) -> None:
    """
    Tests the load function with various types of states
    """

    obj_to_store = "test_object"

    with tempfile.TemporaryDirectory(dir=Path.cwd()) as dir_name:
        folder = Path(dir_name)

        def generate(_) -> Any:
            return obj_to_store

        load1 = notecache.load(state, generate, "", folder=folder)
        load2 = notecache.load(state, generate, "", folder=folder)
        _assert_object_equals(obj_to_store, load1.object)
        _assert_object_equals(obj_to_store, load2.object)
        assert not load2.generated
        assert not load2.state_change


@hp.given(initial_state=st.integers())
def test_load_meaningful_generate_parameter(initial_state) -> None:
    """
    Tests the load function with a generate function that actually performs a
    computation.
    """

    with tempfile.TemporaryDirectory(dir=Path.cwd()) as dir_name:
        folder = Path(dir_name)
        expected_object = initial_state + 1

        def generate(state: int) -> int:
            return state + 1

        load1 = notecache.load(initial_state, generate, "", folder=folder)
        load2 = notecache.load(initial_state, generate, "", folder=folder)
        _assert_object_equals(expected_object, load1.object)
        _assert_object_equals(expected_object, load2.object)
        assert not load2.generated
        assert not load2.state_change


st_safe_text: st.SearchStrategy[str] = st.text(
    st.characters(
        whitelist_categories=(
            "Ll",
            "Lm",
            "Lo",
            "Lt",
            "Lu",
            "Mc",
            "Me",
            "Mn",
            "Nd",
            "Nl",
            "No",
            "Pc",
            "Pd",
            "Pe",
            "Pf",
            "Pi",
            "Po",
            "Ps",
            "Sc",
            "Sk",
            "Sm",
            "Zs",
        )
    )
)


@hp.given(id1=st_safe_text, id2=st_safe_text)
def test_load_unique_id_parameter(id1, id2) -> None:
    """
    Tests the load function with two objects and two IDs to determine if the
    objects are stored independently and can be retrieved independently.
    """

    hp.assume(id1 != id2)
    hp.assume("/" not in id1 and "/" not in id2)

    with tempfile.TemporaryDirectory(dir=Path.cwd()) as dir_name:
        folder = Path(dir_name)

        def generate(unique_id: str) -> Callable[[Any], str]:
            return lambda _: unique_id

        load1_id1 = notecache.load(None, generate(id1), id1, folder=folder)
        load1_id2 = notecache.load(None, generate(id2), id2, folder=folder)
        load2_id1 = notecache.load(None, generate(id1), id1, folder=folder)
        load2_id2 = notecache.load(None, generate(id2), id2, folder=folder)
        assert load1_id1.object == id1
        assert load2_id1.object == id1
        assert load1_id2.object == id2
        assert load2_id2.object == id2
        assert not load2_id1.generated
        assert not load2_id2.generated
        assert not load2_id1.state_change
        assert not load2_id2.state_change


def test_load_custom_reload_parameter() -> None:
    """
    Tests the load function with a non-default reload parameter to determine
    if the reload function is being used correctly.
    """

    with tempfile.TemporaryDirectory(dir=Path.cwd()) as dir_name:
        folder = Path(dir_name)

        def custom_reload(_, right) -> bool:
            return right >= 2

        def generate(_) -> int:
            return 1

        load1 = notecache.load(0, generate, "", folder=folder, reload=custom_reload)
        load2 = notecache.load(1, generate, "", folder=folder, reload=custom_reload)
        load3 = notecache.load(2, generate, "", folder=folder, reload=custom_reload)
        assert load1.object == load2.object
        assert load1.object == load3.object
        assert load1.generated
        assert not load1.state_change
        assert not load2.generated
        assert not load2.state_change
        assert load3.generated
        assert load3.state_change


def test_load_folder() -> None:
    """
    Tests the folder parameter of the load function.
    """

    with tempfile.TemporaryDirectory(dir=Path.cwd()) as parent_name:
        parent_dir = Path(parent_name)
        with (
            tempfile.TemporaryDirectory(dir=parent_dir) as dir1_name,
            tempfile.TemporaryDirectory(dir=parent_dir) as dir2_name,
        ):
            dir1 = Path(dir1_name)
            dir2 = Path(dir2_name)

            def generate(num: int) -> Callable[[Any], int]:
                return lambda _: num

            load1_dir1 = notecache.load(None, generate(1), "", folder=dir1)
            load1_dir2 = notecache.load(None, generate(2), "", folder=dir2)
            load2_dir1 = notecache.load(None, generate(1), "", folder=dir1)
            load2_dir2 = notecache.load(None, generate(2), "", folder=dir2)
            assert load1_dir1.object == 1
            assert load2_dir1.object == 1
            assert load1_dir2.object == 2
            assert load2_dir2.object == 2
            assert not load2_dir1.generated
            assert not load2_dir2.generated
            assert not load2_dir1.state_change
            assert not load2_dir2.state_change


def test_load_force_update() -> None:
    """
    Tests the force_update parameter of the load function
    """

    with tempfile.TemporaryDirectory(dir=Path.cwd()) as dir_name:
        folder = Path(dir_name)

        def generate(_) -> int:
            return 1

        load1 = notecache.load(None, generate, "", folder=folder)
        load2 = notecache.load(None, generate, "", folder=folder, force_update=True)
        assert load1.object == 1
        assert load2.object == 1
        assert load2.generated
        assert not load2.state_change
