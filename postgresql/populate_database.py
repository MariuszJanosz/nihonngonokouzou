import sys

from sqlalchemy import text

from scripts.common import split

from .database import SessionLocal


def make_search_key(key: str) -> str:
    to_remove = (
        " !&'()+,-./:;<=>?@〇〈〉《》「」『』【】〔〕・ー＃＆（）＊＋－／＝｜‐"
    )
    res = ""
    i = 0
    while i < len(key):
        if (
            i + 12 < len(key)
            and key[i] == "<"
            and key[i + 1] == "s"
            and key[i + 2] == "u"
            and key[i + 3] == "p"
            and key[i + 4] == ">"
        ):
            i += 12
        elif key[i] in to_remove:
            i += 1
        else:
            res += key[i]
            i += 1
    return res


if __name__ == "__main__":
    if (
        len(sys.argv) != 2
        or sys.argv[1].split("/")[-1]
        != "dictionary_entries_formated_cleaned.txt"
    ):
        print(
            "USAGE: python populate_database.py <path_to_dictionary_entries_formated_cleaned>"
        )
        sys.exit(1)

    with SessionLocal() as session, open(sys.argv[1]) as f:
        lst = []
        for line in f:
            _, line = split(line, ">")
            key, line = split(line, "</h2>")
            _, line = split(line, ">読み方：")
            reading, entry = "", ""
            if line == "":
                entry = _
            else:
                reading, entry = split(line, "</p>")
            entry = entry.strip()
            search_key = make_search_key(key)
            lst.append({"key": key, "search_key": search_key, "reading": reading, "entry": entry})
        stmt = text(
                "INSERT INTO dictionary_entries (key, search_key, reading, entry) VALUES (:key, :search_key, :reading, :entry);"
        )
        session.execute(stmt, lst)
        session.commit()
