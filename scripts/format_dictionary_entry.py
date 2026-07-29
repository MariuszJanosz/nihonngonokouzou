from common import split


def extract_dictionary_entries(file: str) -> [str]:
    dictionary_entries = []
    # Extract dictionary entries
    with open(file) as f:
        div_count = 0
        de = ""
        for line in f:
            if de != "":
                de += line.strip()
                if line.strip() == "<div class=Sgkdj>":
                    div_count = 1
                else:
                    div_count += line.count("<div") - line.count("</div>")
                    assert div_count >= 0
                    if div_count == 0:
                        dictionary_entries.append(de)
                        de = ""

            if line.find("<h2 class=midashigo title=") != -1:
                de += line.strip()

    # Remove white spaces
    for i in range(len(dictionary_entries)):
        de = dictionary_entries[i]
        e = ""
        for line in de.splitlines():
            e += line.strip()
        e += "\n"
        dictionary_entries[i] = e

    # Sort and dedup
    dictionary_entries.sort()
    deduped = [dictionary_entries[0]]
    i = 1
    while i < len(dictionary_entries):
        if dictionary_entries[i - 1] != dictionary_entries[i]:
            deduped.append(dictionary_entries[i])
        i += 1
    dictionary_entries = deduped

    return dictionary_entries


if __name__ == "__main__":
    dictionary_entries = extract_dictionary_entries("dictionary_entries_no_images.txt")
    with open("dictionary_entries_formated.txt", "w") as f:
        for de in dictionary_entries:
            f.write(de)
