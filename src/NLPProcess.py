import spacy

def analysText(language):
    if language=="en":
        nlp_analyse=spacy.load("en_core_web_sm")

    elif language=="cn":
        nlp_analyse=spacy.load("zh_core_web_sm")
    return NotImplementedError