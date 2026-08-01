from scripts.common import split


def test_get_page():
    assert False  # TODO


def test_split_beginning():
    a, b = split("aaaabbbb", "aaaa")
    assert a == ""
    assert b == "bbbb"


def test_split_middle():
    a, b = split("aaaabbbb", "aabb")
    assert a == "aa"
    assert b == "bb"


def test_split_end():
    a, b = split("aaaabbbb", "bbbb")
    assert a == "aaaa"
    assert b == ""


def test_split_first_appearance():
    a, b = split("aabbaabb", "bb")
    assert a == "aa"
    assert b == "aabb"


def test_split_no_matching():
    a, b = split("aaaabbbb", "cccc")
    assert a == "aaaabbbb"
    assert b == ""


def test_split_empty_pattern():
    a, b = split("aaaabbbb", "")
    assert a == ""
    assert b == "aaaabbbb"
