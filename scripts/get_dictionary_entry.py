import threading

import requests

from scripts.common import get_page, split


def get_dictionary_entries(dest_path: str, urls: list[str]) -> None:
    with open(dest_path, "w") as f:
        session = requests.Session()
        session_reset = 0  # One session per 1000 requests
        for url in urls:
            print(f"GET {url}")
            page = get_page(url, session)
            _, page = split(page, "<!--開始 デジタル大辞泉 -->\n")
            page, _ = split(page, "<!--終了 デジタル大辞泉-->")
            f.write(page)
            session_reset += 1
            if session_reset >= 1000:
                session_reset = 0
                session = requests.Session()


if __name__ == "__main__":
    THREADS_COUNT = 32

    # Count lines
    lines = 0
    with open("words_urls_formated.txt", "r") as f:
        for line in f:
            lines += 1

    # Prepare input urls lists for threads
    URLS_PER_THREAD = lines // THREADS_COUNT
    URLS_LISTS: list[list[str]] = []
    with open("words_urls_formated.txt", "r") as f:
        for i in range(THREADS_COUNT):
            URL_LIST: list[str] = []
            URLS_LISTS.append(URL_LIST)
            limit = (
                URLS_PER_THREAD
                if i + 1 < THREADS_COUNT
                else lines - (THREADS_COUNT - 1) * URLS_PER_THREAD
            )
            for j in range(limit):
                line = f.readline()
                if line == "":
                    break
                url = line.split(" ")[-1].strip()
                URL_LIST.append(url)

    # Start threads
    threads: list[threading.Thread] = []
    for i in range(THREADS_COUNT):
        thr = threading.Thread(
            target=get_dictionary_entries, args=(f"/tmp/de_{i}", URLS_LISTS[i])
        )
        threads.append(thr)

    for thr in threads:
        thr.start()

    for thr in threads:
        thr.join()

    with open("dictionary_entries.txt", "w") as f:
        for i in range(THREADS_COUNT):
            with open(f"/tmp/de_{i}", "r") as g:
                f.write(g.read())
