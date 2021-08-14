def MakeStopwordList(txt_path=None):
    if txt_path:
        stopword_list = set()
        with open(txt_path, "r", encoding="utf-8") as f:
            for l in f:
                if l != "\n":
                    stopword_list.add(l.replace("\n", ""))
        return stopword_list
