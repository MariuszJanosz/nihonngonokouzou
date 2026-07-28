if __name__ == "__main__":
    with open("dictionary_entries.txt") as f:
        with open("dictionary_entries_no_images.txt", "w") as g:
            inside_img = False
            for line in f:
                if line.find("<div class=SgkdjImg>") != -1:
                    inside_img = True

                if not inside_img:
                    g.write(line)

                if line.strip() == "</div>":
                    inside_img = False
