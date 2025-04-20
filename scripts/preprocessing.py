import spacy
import pycld2 as cld2

# Load spaCy models
nlp_en = spacy.load("en_core_web_sm")
nlp_es = spacy.load("es_core_news_sm")
nlp_fr = spacy.load("fr_core_news_sm")

def detect_language(text):
    isReliable, textBytesFound, details = cld2.detect(text)
    return details[0][1]  # returns language code 'en', 'es', 'fr', etc.

def preprocess_description(text):
    lang = detect_language(text)
    if lang == 'en':
        doc = nlp_en(text)
    elif lang == 'es':
        doc = nlp_es(text)
    elif lang == 'fr':
        doc = nlp_fr(text)
    else:
        return []  # Skip unsupported languages
    
    lemmas = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return lemmas
