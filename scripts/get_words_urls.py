import requests

BASE_URL = "https://www.weblio.jp/category/dictionary/sgkdj/"
URL_TAILS = [
        "aa", "ii", "uu", "ee", "oo",
        "ka", "ki", "ku", "ke", "ko",
        "sa", "shi","su", "se", "so",
        "ta", "chi","tsu","te", "to",
        "na", "ni", "nu", "ne", "no",
        "ha", "hi", "fu", "he", "ho",
        "ma", "mi", "mu", "me", "mo",
        "ya",       "yu",       "yo",
        "ra", "ri", "ru", "re", "ro",
        "wa",                   "wo", "nn",
        "ga", "gi", "gu", "ge", "go",
        "za", "zi", "zu", "ze", "zo",
        "da", "di", "du", "de", "do",
        "ba", "bi", "bu", "be", "bo",
        "pa", "pi", "pu", "pe", "po",
        "a",  "b",  "c",  "d",  "e",
        "f",  "g",  "h",  "i",  "j",
        "k",  "l",  "m",  "n",  "o",
        "p",  "q",  "r",  "s",  "t",
        "u",  "v",  "w",  "x",  "y",
        "z",  "sign",
        "1",  "2",  "3",  "4",  "5",
        "6",  "7",  "8",  "9",  "0"
        ]


def get_page(url: str, session: requests.Session) -> str:
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
    session = requests.Session()
    with open("words_urls.txt", "w") as f:
        for tail in URL_TAILS:
            page_number = 1
            words = []
            while True:
                url = BASE_URL + tail + f"/{page_number}"
                page_number += 1
                print(f"GET {url}")
                page = get_page(url, session)
                _, page = split(page, "<ul class=CtgryUlL>\n")
                left_column, page = split(page, "</ul>\n")
                if left_column == "":
                    break
                words.append(left_column)
                _, page = split(page, "<ul class=CtgryUlR>\n")
                right_column, page = split(page, "</ul>\n")
                words.append(right_column)
            words = "".join(words)
            f.write(words)
