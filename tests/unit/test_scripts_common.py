from unittest.mock import Mock, patch

import pytest
import requests

from scripts.common import get_page, split


def make_response(status_code, text):
    response = Mock()
    response.status_code = status_code
    response.text = text
    return response


def make_session(*responses):
    session = Mock()
    session.get.side_effect = [x for x in responses]
    return session


@pytest.fixture
def mocked_sleep():
    with patch("scripts.common.time.sleep") as mocked_sleep:
        yield mocked_sleep


def test_get_page_hello(mocked_sleep):
    session = make_session(make_response(200, "hello"))
    assert get_page("https://example.com", session) == "hello"


def test_get_page_3rd_attempt(mocked_sleep):
    res404 = make_response(404, "")
    res200 = make_response(200, "3rd attempt")
    session = make_session(res404, res404, res200)
    assert get_page("https://example.com", session) == "3rd attempt"


def test_get_page_too_many_failures(mocked_sleep):
    res404 = make_response(404, "")
    session = make_session(res404, res404, res404, res404, res404)
    with pytest.raises(RuntimeError):
        get_page("https://example.com", session)


def test_get_page_no_session():
    with patch("scripts.common.requests.get") as mock_get:
        mock_get.return_value = make_response(200, "hello")
        assert get_page("https://example.com") == "hello"
        mock_get.assert_called_once_with("https://example.com", timeout=5)


def test_get_page_timeout_then_success(mocked_sleep):
    with patch("scripts.common.requests.get") as mock_get:
        mock_get.side_effect = [
            requests.exceptions.Timeout,
            make_response(200, "hello"),
        ]
        assert get_page("https://example.com") == "hello"
        mock_get.assert_called_with("https://example.com", timeout=5)
        assert mock_get.call_count == 2


def test_get_page_5x_timeout(mocked_sleep):
    with patch("scripts.common.requests.get") as mock_get:
        t = requests.exceptions.Timeout
        mock_get.side_effect = [t, t, t, t, t]
        with pytest.raises(RuntimeError):
            get_page("https://example.com")
        assert mock_get.call_count == 5


def test_get_page_session_timeout_then_success(mocked_sleep):
    with patch("scripts.common.requests.Session") as mock_session_constructor:
        s1 = Mock()
        s1.get.side_effect = [requests.exceptions.Timeout]
        s2 = make_session(make_response(200, "hello"))
        mock_session_constructor.return_value = s2
        assert get_page("https://example.com", s1) == "hello"
        mock_session_constructor.assert_called_once_with()
        assert s1.get.call_count == 1
        assert s2.get.call_count == 1


@pytest.mark.parametrize(
    "source,pattern,left,right",
    [
        ("aaaabbbb", "aaaa", "", "bbbb"),
        ("aaaabbbb", "aabb", "aa", "bb"),
        ("aaaabbbb", "bbbb", "aaaa", ""),
        ("aaaabbbb", "cccc", "aaaabbbb", ""),
        ("aabbaabb", "bb", "aa", "aabb"),
        ("aaaabbbb", "", "", "aaaabbbb"),
    ],
)
def test_split(source, pattern, left, right):
    assert split(source, pattern) == (left, right)
