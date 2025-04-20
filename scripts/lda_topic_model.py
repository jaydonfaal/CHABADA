import pandas as pd
from gensim import corpora, models
import ast
import os

def load_processed_descriptions(file_path):
    df = pd.read_csv(file_path)

    # Split the space-separated string into a list of tokens
    df['processed_description'] = df['processed_description'].astype(str).apply(lambda x: x.strip().split())

    return df

def train_lda(df, num_topics=20):
    texts = df['processed_description'].tolist()
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)
    
    return lda_model, corpus, dictionary

def save_topics(lda_model, language, num_words=10):
    lang_dir = os.path.join("..", "results", "lda", language)
    os.makedirs(lang_dir, exist_ok=True)

    with open(os.path.join(lang_dir, "topics.txt"), 'w', encoding='utf-8') as file:
        for idx, topic in lda_model.print_topics(-1, num_words=num_words):
            file.write(f"Topic {idx}: {topic}\n")



if __name__ == "__main__":
    languages = ['spanish', 'french']
    num_topics = 20

    for lang in languages:
        print(f"Processing {lang.capitalize()} descriptions...")

        df = load_processed_descriptions(f'preprocessed_descriptions/{lang}.csv')
        lda_model, corpus, dictionary = train_lda(df, num_topics=num_topics)

        save_topics(lda_model, lang)

        # Optionally save model and dictionary for later reuse
        lang_dir = os.path.join("results", "lda", lang)
        os.makedirs(lang_dir, exist_ok=True)

        lda_model.save(os.path.join(lang_dir, "lda.model"))
        dictionary.save(os.path.join(lang_dir, "dict.dict"))

        print(f"Finished {lang.capitalize()} topic modeling.")
