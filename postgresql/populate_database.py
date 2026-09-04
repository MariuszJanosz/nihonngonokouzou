import sys

from sqlalchemy import text

from scripts.common import split

from .database import SessionLocal

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
            lst.append({"key": key, "reading": reading, "entry": entry})
        stmt = text(
            "INSERT INTO dictionary_entries (key, reading, entry) VALUES (:key, :reading, :entry);"
        )
        session.execute(stmt, lst)
        session.commit()
