def MakeStopwordList(txt_path=None):
    if txt_path:
        stopword_list = []
        with open(txt_path, "r", encoding="utf-8") as f:
            for l in f:
                if l != "\n":
                    stopword_list.append(l.replace("\n", ""))
        return stopword_list