import spacy

def analysText(language,content):
    if language=="en":
        nlp_analyse=spacy.load("en_core_web_sm")
        doc=nlp_analyse(content)

    elif language=="cn":
        nlp_analyse=spacy.load("zh_core_web_sm")
        doc=nlp_analyse(content)
    return NotImplementedError