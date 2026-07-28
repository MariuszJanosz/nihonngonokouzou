import requests
import time


def get_page(url: str, session: requests.Session | None = None) -> str:
    if session:
        try:
            r = session.get(url, timeout=5)
        except requests.exceptions.Timeout:
            print(f"Blocked {url}, retrying...")
            del session
            time.sleep(5)
            session = requests.Session()
            return get_page(url, session)
    else:
        try:
            r = requests.get(url, timeout=5)
        except requests.exceptions.Timeout:
            print(f"Blocked {url}, retrying...")
            time.sleep(5)
            return get_page(url)

    if r.status_code != 200:
        print(f"Faild to GET {url}, got status code {r.status_code}, retrying...")
        time.sleep(5)
        return get_page(url)
    return r.text


def split(src: str, split: str) -> (str, str):
    start = src.find(split)
    if start == -1:
        return (src, "")
    return (src[:start], src[start + len(split):])
