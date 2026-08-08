import time

import requests


def get_page(
    url: str, session: requests.Session | None = None, max_attempts: int = 10
) -> str:
    for i in range(max_attempts):
        r = None
        if session:
            try:
                r = session.get(url, timeout=2**i)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                session = requests.Session()
        else:
            try:
                r = requests.get(url, timeout=2**i)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                pass

        if r and r.status_code == 200:
            return r.text
        else:
            print(f"GET {url} failed (Attempt {i + 1}/{max_attempts}).")
            if i < max_attempts - 1:
                time.sleep(5)

    raise RuntimeError(
        f"GET {url} failed after {max_attempts} attempts. Aborting!"
    )


def split(src: str, split: str) -> tuple[str, str]:
    start = src.find(split)
    if start == -1:
        return (src, "")
    return (src[:start], src[start + len(split) :])


def cut_out(source: str, prefix: str, suffix: str) -> tuple[str, str]:
    _, tmp = split(source, prefix)
    return split(tmp, suffix)
