if __name__ == "__main__":
    with open("words_urls.txt", "r") as f:
        with open("words_urls_formated.txt", "w") as g:
            for line in f:
                url = line[13: line.find("\"", 13)]
                word = line[line.find("crosslink>") + 10: line.find("</a></li>")]
                g.write(word + " " + url + "\n")
