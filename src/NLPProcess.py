import spacy
import re


def analysText(language, content):
    if language == "en":
        nlp_analyse = spacy.load("en_core_web_sm")
        doc = nlp_analyse(content)
        ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        ip = re.findall(ip_pattern, content)
        if ip.__len__() != 0:
            print("IP:", ip)
        else:
            print(content)

    elif language == "cn":
        nlp_analyse = spacy.load("zh_core_web_sm")
        doc = nlp_analyse(content)
