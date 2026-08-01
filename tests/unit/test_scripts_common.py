from unittest.mock import Mock, patch

import requests

from scripts.common import get_page, split


def _mock_response(status_code, text):
    response = Mock()
    response.status_code = status_code
    response.text = text
    return response


def _mock_session(responses):
    session = Mock()
    session.get.side_effect = [x for x in responses]
    return session


def test_get_page_hello():
    session = _mock_session([_mock_response(200, "hello")])
    with patch("scripts.common.time.sleep"):
        assert get_page("https://example.com", session) == "hello"


def test_get_page_3rd_attempt():
    res404 = _mock_response(404, "")
    res200 = _mock_response(200, "3rd attempt")
    session = _mock_session([res404, res404, res200])
    with patch("scripts.common.time.sleep"):
        assert get_page("https://example.com", session) == "3rd attempt"


def test_get_page_too_many_failures():
    res404 = _mock_response(404, "")
    session = _mock_session([res404, res404, res404, res404, res404])
    try:
        with patch("scripts.common.time.sleep"):
            get_page("https://example.com", session)
    except Exception as e:  # noqa
        assert type(e) == RuntimeError
        return

    assert False


def test_get_page_no_session():
    with patch("scripts.common.requests.get") as mock_get:
        mock_get.return_value = _mock_response(200, "hello")
        assert get_page("https://example.com") == "hello"
        mock_get.assert_called_once_with("https://example.com", timeout=5)


def test_get_page_timeout_then_success():
    with (
        patch("scripts.common.requests.get") as mock_get,
        patch("scripts.common.time.sleep"),
    ):
        mock_get.side_effect = [
            requests.exceptions.Timeout,
            _mock_response(200, "hello"),
        ]
        assert get_page("https://example.com") == "hello"
        mock_get.assert_called_with("https://example.com", timeout=5)
        assert mock_get.call_count == 2


def test_get_page_5x_timeout():
    with (
        patch("scripts.common.requests.get") as mock_get,
        patch("scripts.common.time.sleep"),
    ):
        t = requests.exceptions.Timeout
        mock_get.side_effect = [t, t, t, t, t]
        try:
            get_page("https://example.com")
        except Exception as e:  # noqa
            assert type(e) == RuntimeError
            assert mock_get.call_count == 5
            return

        assert False


def test_get_page_session_timeout_then_success():
    with (
        patch("scripts.common.requests.Session") as mock_session_constructor,
        patch("scripts.common.time.sleep"),
    ):
        s1 = Mock()
        s1.get.side_effect = [requests.exceptions.Timeout]
        s2 = _mock_session([_mock_response(200, "hello")])
        mock_session_constructor.return_value = s2
        assert get_page("https://example.com", s1) == "hello"
        mock_session_constructor.assert_called_once_with()
        assert s1.get.call_count == 1
        assert s2.get.call_count == 1


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
