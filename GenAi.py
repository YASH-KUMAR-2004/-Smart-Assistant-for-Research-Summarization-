import fitz  # PyMuPDF
import spacy
import gradio as gr
from transformers import pipeline
from difflib import SequenceMatcher

# Load NLP and models
nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")
qg_model = pipeline("text2text-generation", model="google/flan-t5-large")

# === UTILS ===
def extract_text_from_pdf(pdf_file):
    try:
        doc = fitz.open(pdf_file.name)
        return " ".join([page.get_text() for page in doc])
    except Exception as e:
        return f"[Error extracting text: {str(e)}]"

def split_sentences(text):
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 10]

def chunk_text(text, max_tokens=400):
    words = text.split()
    chunks = []
    current_chunk = []
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def generate_challenge_questions(text, n=3):
    sents = split_sentences(text)[:n]
    return [(s, qg_model(f"Generate a question from: {s}", max_new_tokens=64)[0]['generated_text']) for s in sents]

def evaluate_answer_chunked(user_ans, context, question):
    chunks = chunk_text(context, max_tokens=400)
    best_score = 0
    best_answer = ""
    matching_chunk = ""
    highest_similarity = 0

    for chunk in chunks:
        result = qa_model(question=question, context=chunk)
        answer = result['answer']
        score = result.get('score', 0.0)
        similarity = SequenceMatcher(None, user_ans.lower(), answer.lower()).ratio()

        if similarity > 0.6 and score > best_score:
            best_score = score
            best_answer = answer
            matching_chunk = chunk
            highest_similarity = similarity

    if best_answer:
        return f"✅ Correct!\nExpected: {best_answer}\n📌 Found in: \"{matching_chunk[:300]}...\""
    else:
        return f"❌ Incorrect.\nNo strong match found.\n💡 Hint: Try rephrasing or rechecking your answer."

def qa_with_chunked_context(question, context):
    chunks = chunk_text(context, max_tokens=400)
    best_score = 0
    best_answer = ""
    for chunk in chunks:
        result = qa_model(question=question, context=chunk)
        if result.get('score', 0.0) > best_score:
            best_score = result['score']
            best_answer = result['answer']
    return best_answer

# Store questions between calls (global state in Colab runtime)
stored_challenge_questions = []

# === MAIN FUNCTION ===
def handle_action(pdf_file, action, user_input):
    global stored_challenge_questions

    if not pdf_file:
        return "⚠ Please upload a PDF."

    text = extract_text_from_pdf(pdf_file)
    if text.startswith("[Error"):
        return text

    try:
        if action == "Summarize":
            chunks = chunk_text(text, max_tokens=400)
            all_summaries = []
            for i, chunk in enumerate(chunks):
                summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
                all_summaries.append(summary)
            combined = " ".join(all_summaries)
            final_summary = summarizer(combined, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
            return f"📝 Final Summary (150 words):\n{final_summary}"

        elif action == "Question Answering":
            if not user_input.strip():
                return "❗ Please enter a question."
            answer = qa_with_chunked_context(user_input, text)
            return f"💬 Answer: {answer}\n📌 Answer derived from the document."

        elif action == "Challenge Me":
            if user_input.strip().lower() == "show":
                if not stored_challenge_questions:
                    return "❗ No challenge questions generated yet. Please reset and try again."
                return "🧠 Challenge Questions:\n\n" + "\n\n".join([f"Q{i+1}: {q}" for i, (_, q) in enumerate(stored_challenge_questions)]) + "\n\n✍ To answer, enter: Q<number> | Your Answer"
            elif "|" in user_input:
                parts = user_input.split('|')
                if len(parts) == 2:
                    q_id = parts[0].strip().lower().replace("q", "")
                    user_ans = parts[1].strip()
                    if q_id.isdigit() and 0 < int(q_id) <= len(stored_challenge_questions):
                        idx = int(q_id) - 1
                        question = stored_challenge_questions[idx][1]
                        feedback = evaluate_answer_chunked(user_ans, text, question)
                        return f"🧠 Challenge Question: {question}\n🧑 Your Answer: {user_ans}\n\n📣 Feedback: {feedback}"
                    else:
                        return "❗ Invalid question number. Use format like: Q1 | Your Answer"
            else:
                stored_challenge_questions = generate_challenge_questions(text)
                return "✅ Challenge questions generated. Type show to view them."

        else:
            return "⚠ Invalid action."

    except Exception as e:
        return f"[Processing Error: {str(e)}]"

# === GRADIO UI ===
demo = gr.Interface(
    fn=handle_action,
    inputs=[
        gr.File(label="📄 Upload PDF", file_types=[".pdf"]),
        gr.Radio(["Summarize", "Question Answering", "Challenge Me"], label="Choose Action"),
        gr.Textbox(label="❓ Your input (QA or Challenge Evaluation)")
    ],
    outputs=gr.Text(label="🧠 Output"),
    title="📚 GenAI Assistant (Challenge Q&A Mode Enabled)",
    description="Upload a PDF and choose to summarize it, ask a question, generate challenge questions, or evaluate your answers. For Challenge Mode: type 'show' to get questions, then answer with Q1 | Your Answer."
)

demo.launch(share=True)