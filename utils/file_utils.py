def open_file_chunk(path):
    with open(path, "r") as f:
        train_data = []
        sentence = []
        for line in f:
            if line.strip() == "":
                if len(sentence) > 0:
                    train_data.append(sentence)
                    sentence = []
            else:
                word, _, pos = line.strip().split()
                sentence.append((word, pos))
        if len(sentence) > 0:
            train_data.append(sentence)
    return train_data
