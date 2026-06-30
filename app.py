from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
import io
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

DEFAULT_DOCUMENTS = {
    "Artificial Intelligence": (
        "Artificial intelligence is the simulation of human intelligence by machines. "
        "AI systems can learn from data, recognize patterns, and make decisions. "
        "Machine learning and deep learning are core branches of artificial intelligence "
        "that power modern applications like voice assistants and recommendation systems."
    ),
    "Natural Language Processing": (
        "Natural language processing enables computers to understand and generate human language. "
        "NLP combines linguistics and machine learning to perform tasks like translation, "
        "sentiment analysis, and text summarization. Tokenization and stemming are common "
        "preprocessing steps used in natural language processing pipelines."
    ),
    "Cricket World Cup": (
        "The Cricket World Cup is one of the most watched sporting events globally. "
        "Teams from different countries compete in a tournament format to win the trophy. "
        "Players need strong batting, bowling, and fielding skills to perform well in "
        "high pressure matches during the cricket world cup."
    ),
    "Healthy Diet and Nutrition": (
        "A healthy diet includes a balance of proteins, carbohydrates, fats, vitamins, and minerals. "
        "Eating fresh fruits and vegetables daily improves overall nutrition and energy levels. "
        "Avoiding processed food and maintaining proper hydration are important parts of a "
        "healthy and balanced diet."
    ),
    "Retrieval Augmented Generation": (
        "Retrieval Augmented Generation, or RAG, combines information retrieval with "
        "language generation models. RAG systems search a knowledge base using vector "
        "similarity to find relevant documents, then use a language model to generate "
        "an accurate answer based on the retrieved information."
    ),
}

class AppState:
    def __init__(self):
        self.documents = {}
        self.doc_names = []
        self.doc_texts = []
        self.bow_vectorizer = None
        self.bow_matrix = None
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None

    def load_dataset(self, docs_dict):
        if not docs_dict or not isinstance(docs_dict, dict):
            raise ValueError("Dataset must be a non-empty JSON dictionary.")
        
        self.documents = docs_dict
        self.doc_names = list(self.documents.keys())
        self.doc_texts = list(self.documents.values())

        self.bow_vectorizer = CountVectorizer(stop_words="english")
        self.bow_matrix = self.bow_vectorizer.fit_transform(self.doc_texts)

        self.tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.doc_texts)

state = AppState()

@app.route("/")
def index():
    state.__init__()
    return render_template("index.html")

@app.route("/upload_dataset", methods=["POST"])
def upload_dataset():
    data = request.get_json()
    try:
        state.load_dataset(data)
        return jsonify({"message": "Dataset loaded successfully!", "count": len(state.documents)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/upload_pdfs", methods=["POST"])
def upload_pdfs():
    if not request.files:
        return jsonify({"error": "No files uploaded."}), 400
    
    new_docs = {}
    for key, file in request.files.items():
        if not file.filename.lower().endswith('.pdf'):
            continue
        try:
            reader = PdfReader(io.BytesIO(file.read()))
            text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
            title = file.filename.rsplit('.', 1)[0].replace('_', ' ').replace('-', ' ').title()
            new_docs[title] = text.strip()
        except Exception as e:
            pass
            
    if not new_docs:
        return jsonify({"error": "No readable PDF files found or files were empty."}), 400
        
    try:
        state.load_dataset(new_docs)
        return jsonify({"message": "PDF Dataset loaded successfully!", "count": len(state.documents)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/load_sample", methods=["POST"])
def load_sample():
    try:
        state.load_dataset(DEFAULT_DOCUMENTS)
        return jsonify({"message": "Sample dataset loaded successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/clear", methods=["POST"])
def clear_dataset():
    state.__init__()
    return jsonify({"message": "Dataset cleared!"})

@app.route("/documents", methods=["GET"])
def documents():
    docs = [
        {
            "id":      i + 1,
            "title":   name,
            "preview": text[:140].rsplit(" ", 1)[0] + "...",
            "text":    text,
        }
        for i, (name, text) in enumerate(state.documents.items())
    ]
    return jsonify({"documents": docs})

@app.route("/search", methods=["POST"])
def search():
    data  = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Please enter a search query."}), 400

    if not state.bow_vectorizer or not hasattr(state.bow_vectorizer, 'vocabulary_') or not state.bow_vectorizer.vocabulary_:
        return jsonify({"error": "Searching empty air, are we? Pick a dataset first."}), 400

    def rank(vectorizer, matrix):
        query_vec = vectorizer.transform([query])
        scores    = cosine_similarity(query_vec, matrix).flatten()
        ranked    = sorted(
            zip(state.doc_names, scores),
            key=lambda x: x[1], reverse=True
        )
        max_score = ranked[0][1] if ranked[0][1] > 0 else 1
        return [
            {
                "title": name,
                "score": round(float(score), 4),
                "pct": round(float(score / max_score) * 100, 1) if max_score > 0 else 0,
            }
            for name, score in ranked
        ]

    bow_results   = rank(state.bow_vectorizer, state.bow_matrix)
    tfidf_results = rank(state.tfidf_vectorizer, state.tfidf_matrix)

    best_title   = tfidf_results[0]["title"] if tfidf_results[0]["score"] > 0 else None
    best_snippet = state.documents[best_title][:220].rsplit(" ", 1)[0] + "…" if best_title else None
    bow_winner   = bow_results[0]["title"]   if bow_results[0]["score"]   > 0 else None

    return jsonify({
        "query":            query,
        "bow_results":      bow_results,
        "tfidf_results":    tfidf_results,
        "best_match":       best_title,
        "best_snippet":     best_snippet,
        "bow_winner":       bow_winner,
        "bow_vocab_size":   len(state.bow_vectorizer.vocabulary_),
        "tfidf_vocab_size": len(state.tfidf_vectorizer.vocabulary_),
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)