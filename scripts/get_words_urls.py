import requests

from scripts.common import cut_out, get_page

BASE_URL: str = "https://www.weblio.jp/category/dictionary/sgkdj/"
# fmt: off
URL_TAILS: list[str] = [
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
# fmt: on


if __name__ == "__main__":
    with open("words_urls.txt", "w") as f:
        for tail in URL_TAILS:
            session = requests.Session()
            page_number = 1
            words: list[str] = []
            while True:
                url = BASE_URL + tail + f"/{page_number}"
                page_number += 1
                print(f"GET {url}")
                page = get_page(url, session)
                left_column, page = cut_out(
                    page, "<ul class=CtgryUlL>\n", "</ul>\n"
                )
                if left_column == "":
                    break
                words.append(left_column)
                right_column, page = cut_out(
                    page, "<ul class=CtgryUlR>\n", "</ul>\n"
                )
                words.append(right_column)
            words_str = "".join(words)
            f.write(words_str)
