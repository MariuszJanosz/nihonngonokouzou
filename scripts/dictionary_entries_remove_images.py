if __name__ == "__main__":
    with (
        open("dictionary_entries.txt") as f,
        open("dictionary_entries_no_images.txt", "w") as g,
    ):
        div_count = 0
        for line in f:
            if line.strip() == "<div class=SgkdjImg>":
                div_count = 1

            if div_count == 0:
                g.write(line)

            if line.strip() != "<div class=SgkdjImg>" and div_count != 0:
                div_count += line.count("<div") - line.count("</div>")

            assert div_count >= 0
