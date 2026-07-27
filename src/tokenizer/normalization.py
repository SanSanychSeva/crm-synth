def normalize(text):

    text = text.lower()

    text = " ".join(
        text.split()
    )

    return text