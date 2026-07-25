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
    with open("words_urls_formated.txt", "r") as f:
        with open("dictionary_entries.txt", "w") as g:
            session = requests.Session()
            session_reset = 0 # One session per 1000 requests
            for line in f:
                url = line.split(" ")[-1].strip()
                print(f"GET {url}")
                page = get_page(url, session)
                _, page = split(page, "<!--開始 デジタル大辞泉 -->\n")
                page, _ = split(page, "<!--終了 デジタル大辞泉-->")
                g.write(page)

                session_reset += 1
                if session_reset >= 1000:
                    session_reset = 0
                    del session
                    session = requests.Session()
