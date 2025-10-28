# Kotobuddy

A **Command-Line Japanese Language Study App**, built with [Textual UI](https://textual.textualize.io/).  
Paste in Japanese text, click words to view definitions, and save them as flashcards.  
Review flashcards using a built-in **SRS (Spaced Repetition System)** to reinforce long-term retention.
s on being able to review vocabulary such as verbs, nouns, and adjective. It does not currently have proper handling for Japanese particles and conjugations




https://github.com/user-attachments/assets/ab5682b7-5a06-4862-9677-429c12f8a251




## ✨ Features

- Tokenizes Japanese text into clickable words using **Fugashi** + **IPADic**
- Retrieves definitions via **Jamdict** (Japanese–English dictionary)
- Save words as flashcards for later review
- Review cards using a simple **SRS** loop
- Fully interactive **Textual UI** in your terminal

---

## ⚙️ Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/yourusername/kotobuddy.git
cd kotobuddy
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If you prefer to install manually instead of using `requirements.txt`, make sure you have:

```bash
pip install textual fugashi ipadic jamdict jamdict-data
```

> 💡 **Note:** You do **not** need to install MeCab separately — Fugashi bundles a working version for most systems.

---

## Dependency Notes

This project uses **Fugashi**, a Python wrapper around **MeCab**, for morphological analysis and tokenization.

By default, Fugashi often integrates with **UniDic**, which provides fine-grained, linguistically detailed tokenization.  
However, this project intentionally uses **IPADic**, as it offers **simpler and more user-friendly (coarse-grained)** tokenization better suited for learners.

> ⚠️ **Note:**  
> **IPADic** is no longer actively maintained, whereas **UniDic** is.  
> If you plan to modify or extend this project, you may wish to reconfigure Fugashi to use UniDic depending on your use case.

---

## 📚 Resources & Further Reading

- [How to Tokenize Japanese in Python](https://www.dampfkraft.com/nlp/how-to-tokenize-japanese.html) – excellent overview of Japanese tokenization concepts  
- [Fugashi GitHub Repository](https://github.com/polm/fugashi?tab=readme-ov-file) – for details on setup, dictionaries, and usage

---

## 🪄 Example Usage

```bash
textual run main.py
```

Paste in Japanese text and explore words interactively.  
Click any word to view its definition or save it to your flashcard deck.

---
