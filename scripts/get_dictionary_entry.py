import sys

import requests


def get_page(url: str, session: requests.Session | None = None) -> str:
    if session:
        r = session.get(url)
    else:
        r = requests.get(url)

    if r.status_code != 200:
        raise Exception(f"Faild to GET {url}")
    return r.text


def split(src: str, split: str) -> (str, str):
    start = src.find(split)
    if start == -1:
        return (src, "")
    return (src[:start], src[start + len(split):])


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: python get_dictionary_entry.py <URL>")
        raise Exception("Incorrect number of arguments")

    page = get_page(sys.argv[1])
    print(page)
