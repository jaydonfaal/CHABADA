import os
import pandas as pd
from gensim import models, corpora
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def load_topic_vectors(lang):
    print(f"\nProcessing language: {lang}")

    # Load LDA model & dictionary
    lda_model_path = os.path.join("results", "lda", lang, "lda.model")
    dict_path = os.path.join("results", "lda", lang, "dict.dict")

    lda_model = models.LdaModel.load(lda_model_path)
    dictionary = corpora.Dictionary.load(dict_path)

    # Load CSV of preprocessed descriptions
    data_path = os.path.join("preprocessed_descriptions", f"{lang}.csv")
    df = pd.read_csv(data_path)

    # Ensure tokens are in list format
    df['processed_description'] = df['processed_description'].apply(lambda x: x.split() if isinstance(x, str) else x)
    texts = df['processed_description'].tolist()
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Extract topic vectors
    topic_vectors = []
    for doc_bow in corpus:
        topic_dist = lda_model.get_document_topics(doc_bow, minimum_probability=0)
        vector = [prob for _, prob in sorted(topic_dist)]
        topic_vectors.append(vector)

    return df, topic_vectors

def cluster_and_save(df, topic_vectors, lang, num_clusters=10):
    # K-Means Clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(topic_vectors)

    # Evaluate clustering quality
    sil_score = silhouette_score(topic_vectors, labels)
    print(f"Silhouette Score for {lang}: {sil_score:.4f}")

    # Add cluster labels to DataFrame
    df['cluster'] = labels

    # Ensure output folder exists
    output_dir = os.path.join("results", "clusters")
    os.makedirs(output_dir, exist_ok=True)

    # Save CSV
    output_path = os.path.join(output_dir, f"{lang}_clusters.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved clusters to: {output_path}")

if __name__ == "__main__":
    languages = ['spanish', 'french']  # Add 'french' once Spanish works

    for lang in languages:
        try:
            df, topic_vectors = load_topic_vectors(lang)
            cluster_and_save(df, topic_vectors, lang)
        except Exception as e:
            print(f"Error processing {lang}: {e}")
