from .common import remove_html_comment, remove_html_element

if __name__ == "__main__":
    with (
        open("dictionary_entries_formated.txt") as f,
        open("dictionary_entries_formated_cleaned.txt", "w") as g,
    ):
        g.writelines(
            remove_html_comment(
                remove_html_element(
                    remove_html_element(remove_html_element(line, "a"), "div"),
                    "span",
                ),
                False,
            )[0]
            for line in f
        )
