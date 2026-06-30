# 🧪 Hard Test Dataset & Edge Cases

This document contains a specialized dataset and a set of queries designed to stress-test the vectorization pipeline. By using documents that share common vocabulary (e.g., "Python", "code", "model"), we can clearly see the difference between simple **Bag of Words** (raw counting) and **TF-IDF** (weighted importance).

---

## 📚 The Hard Corpus

These 5 articles are designed with deliberate overlap. Notice how Documents 1 & 2 share programming terms, and Documents 3 & 4 both heavily use the word "model" in completely different contexts.

| ID | Title | Content |
| :---: | :--- | :--- |
| **1** | **Python Web Development** | Python is a popular language for building web applications using frameworks like Flask and Django. Developers write code to handle requests, manage databases, and build REST APIs. Python's simple syntax makes it easy to write clean, readable code for web projects. |
| **2** | **Python for Data Science** | Python is widely used in data science for analyzing and processing large datasets. Libraries like Pandas and NumPy allow developers to write code that cleans data, performs calculations, and prepares data for machine learning models. Python makes data science accessible. |
| **3** | **Machine Learning Models** | A machine learning model learns patterns from training data to make predictions on new data. Common model types include decision trees, neural networks, and support vector machines. Training a good model requires clean data, feature engineering, and careful evaluation. |
| **4** | **Startup Business Basics** | Every startup needs a clear business model to succeed. A business model explains how a company creates value, reaches customers, and generates revenue. Founders must validate their business model before scaling their startup. |
| **5** | **Climate Change and Environment** | Climate change refers to long-term shifts in global temperatures and weather patterns caused by human activity. Rising carbon emissions from fossil fuels are the primary driver of climate change, leading to extreme weather events and rising sea levels. |

---

## 🎯 Test Queries

To see the full potential of the engine, paste these queries into the search bar when the above dataset is loaded. Pay close attention to the **Method Comparison Note** in the UI to see when TF-IDF outsmarts Bag of Words!

### 1. Disambiguation (Overlap Test)
> **Query:** `python code for cleaning datasets`
* **Expected Top Match:** Python for Data Science
* **Why it's hard:** Tests if the system can tell apart two Python documents (web dev vs data science) that both heavily share the words "python" and "code". TF-IDF should easily identify "cleaning" and "datasets" as the uniquely important factors here.

### 2. High Precision Match
> **Query:** `how do I build a flask api`
* **Expected Top Match:** Python Web Development
* **Why it's hard:** Tests precision. The words "flask" and "api" only appear in Document 1, so the score should point incredibly strongly toward it, ignoring the data science Python doc entirely.

### 3. Contextual Overlap (ML Context)
> **Query:** `training a neural network model`
* **Expected Top Match:** Machine Learning Models
* **Why it's hard:** Both Document 3 (ML) and Document 4 (Business) use the word "model" repeatedly. Adding "neural network" and "training" should cleanly disambiguate the intent toward machine learning.

### 4. Contextual Overlap (Business Context)
> **Query:** `business model for a new company`
* **Expected Top Match:** Startup Business Basics
* **Why it's hard:** Tests the *opposite* ambiguity of Query #3. The word "model" appears again, but "business" and "company" should correctly route the engine to the startup document this time.

### 5. Synonym Handling
> **Query:** `global warming and rising temperatures`
* **Expected Top Match:** Climate Change and Environment
* **Why it's hard:** Tests synonym handling. The query uses "global warming" and "rising temperatures", which don't exactly match the document text ("climate change", "rising sea levels"). Because TF-IDF and BoW are purely keyword-based, the partial overlap word ("rising") must carry the entire match!

### 6. The Negative Case
> **Query:** `what is the capital of France`
* **Expected Top Match:** *No relevant match (Score near 0.000)*
* **Why it's hard:** Tests the negative baseline. A completely unrelated query should return very low or zero similarity for *all* documents, proving the system doesn't just confidently force a bad match.

### 7. Single Ambiguous Keyword
> **Query:** `model`
* **Expected Top Match:** *Ambiguous (Doc 3 or Doc 4)*
* **Why it's hard:** A single ambiguous word with absolutely no surrounding context. This is the clearest demonstration of TF-IDF's true value — it will slightly favor whichever document uses the word "model" more frequently *relative to its total length*, whereas Bag of Words will just give a naive raw count.
