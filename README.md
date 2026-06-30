<div align="center">

# 🔍 Document Similarity Search

A dynamic web app that converts user-provided documents into numeric vectors using **Bag of Words** and **TF-IDF**, then ranks them by **Cosine Similarity** against a user query.

[![Live Preview](https://img.shields.io/badge/Live%20Preview-Visit%20Site-FF3D00?style=for-the-badge)](https://your-deploy-link.onrender.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Atharva%20Phatangare-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/atharva-phatangare)
[![GitHub](https://img.shields.io/badge/GitHub-atharva--9423-black?style=for-the-badge&logo=github)](https://github.com/atharva-9423)
![Python](https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge&logo=python)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?style=for-the-badge)

</div>

---

## 🧠 Why This Matters

This project is the literal **retrieval engine inside RAG (Retrieval Augmented Generation)** systems, built by hand. When an AI chatbot "searches its knowledge base" to answer a question, this exact mechanism — vectorize the query, compare it to stored document vectors, rank by cosine similarity — is what's happening under the hood.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📂 **Dynamic Datasets** | Upload PDF files, type articles manually, or load a sample dataset on the fly. |
| 🔢 **Bag of Words** | Converts text into raw word-count vectors. |
| ⭐ **TF-IDF** | Weighs words by importance, down-weighting common stop words. |
| 📐 **Cosine Similarity** | Measures the angle between query and document vectors (0.0 to 1.0). |
| 🏆 **Ranked Results** | Side-by-side visual comparison of BoW vs TF-IDF rankings. |
| 🌗 **Dark Mode** | Seamless transition between Light and Dark themes. |
| 🎨 **Swiss-Style UI** | Monochrome design with a single accent color, optimized for minimal scrolling. |

---

## 🔬 How It Works

```
1. DATASET    →  User uploads PDFs or types text. The app extracts text and
                  prepares it for the pipeline.

2. VECTORIZE  →  Documents are converted into vectors using CountVectorizer (BoW)
                  and TfidfVectorizer (TF-IDF).

3. QUERY      →  The user's search query is converted into a vector
                  using the SAME vocabulary as the documents.

4. COMPARE    →  cosine_similarity(query_vector, document_vectors)
                  measures how closely the query "points" in the same
                  direction as each document.

5. RANK       →  Documents are sorted by similarity score (0 to 1).
                  Score closer to 1 = more relevant.
```

### Bag of Words vs TF-IDF — The Key Difference

**Bag of Words** counts how many times each word appears. Simple, but treats every word as equally important — so common words can dominate the score.

**TF-IDF (Term Frequency–Inverse Document Frequency)** down-weights words that appear in many documents (less distinctive) and up-weights words that are rare but frequent in one specific document (more distinctive). This usually produces more accurate rankings and is the industry standard for traditional keyword search.

---

## 🚀 How To Run

**Step 1** — Install dependencies:
```bash
pip install flask scikit-learn pypdf
```

**Step 2** — Clone and run:
```bash
git clone https://github.com/atharva-9423/UnProf_Pyai_10.git
cd UnProf_Pyai_10
python3 app.py
```

**Step 3** — Open in browser:
```
http://localhost:5001
```

---

## 📁 File Structure

```
📂 UnProf_Pyai_10/
├── app.py                ← Flask backend (PDF extraction, vectorization, search API)
├── requirements.txt      ← Python dependencies (flask, scikit-learn, pypdf)
├── templates/
│   └── index.html        ← Swiss-style frontend with Dark Mode & Modals
├── test_dataset.md       ← Harder dataset + edge-case test queries 
└── README.md
```

---

## 📅 Internship Context

Built as part of **Day 10 — Text Vectorization** of my Python & AI Internship at **UnProf**, Phase 2: NLP & Text AI.

Concepts covered: Bag of Words, TF-IDF, Cosine Similarity, PDF Text Extraction — the foundation of search engines, recommendation systems, and RAG-based chatbots.

---

<div align="center">

Made with ❤️ by **Atharva Phatangare**

[![LinkedIn](https://img.shields.io/badge/Let's%20Connect-LinkedIn-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/atharva-phatangare)
[![GitHub](https://img.shields.io/badge/More%20Projects-GitHub-black?style=for-the-badge&logo=github)](https://github.com/atharva-9423)

</div>
