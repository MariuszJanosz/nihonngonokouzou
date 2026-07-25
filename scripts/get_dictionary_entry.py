import requests
import threading


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


def get_dictionary_entries(dest_path: str, urls: list[str]) -> None:
    with open(dest_path, "w") as f:
        session = requests.Session()
        session_reset = 0 # One session per 1000 requests
        for url in urls:
            print(f"GET {url}")
            page = get_page(url, session)
            _, page = split(page, "<!--開始 デジタル大辞泉 -->\n")
            page, _ = split(page, "<!--終了 デジタル大辞泉-->")
            f.write(page)
            session_reset += 1
            if session_reset >= 1000:
                session_reset = 0
                del session
                session = requests.Session()


if __name__ == "__main__":
    THREADS_COUNT = 256
    
    # Count lines
    lines = 0
    with open("words_urls_formated.txt", "r") as f:
        for line in f:
            lines += 1

    # Prepare input urls lists for threads
    URLS_PER_THREAD = lines // THREADS_COUNT
    URLS_LISTS = []
    with open("words_urls_formated.txt", "r") as f:
        for i in range(THREADS_COUNT):
            URL_LIST = []
            URLS_LISTS.append(URL_LIST)
            for j in range(URLS_PER_THREAD):
                line = f.readline()
                if line == "":
                    break
                url = line.split(" ")[-1].strip()
                URL_LIST.append(url)

    # Start threads
    threads = []
    for i in range(THREADS_COUNT):
        thr = threading.Thread(target=get_dictionary_entries,
                               args=(f"/tmp/de_{i}", URLS_LISTS[i]))
        threads.append(thr)

    for thr in threads:
        thr.start()

    for thr in threads:
        thr.join()

    with open("dictionary_entries.txt", "w") as f:
        for i in range(THREADS_COUNT):
            with open(f"/tmp/de_{i}", "r") as g:
                f.write(g.read())
