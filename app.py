from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
import PyPDF2

from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from langchain_classic.chains import RetrievalQA
from langchain_text_splitters import CharacterTextSplitter

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
# pyrefly: ignore [missing-import]
from langchain_community.vectorstores import FAISS


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Please add GROQ_API_KEY to your .env file."
    )


# ============================================================
# TEXT SPLITTER
# ============================================================

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=2000,
    chunk_overlap=200,
    length_function=len,
)


# ============================================================
# EMBEDDINGS
# ============================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ============================================================
# GROQ LLM
# ============================================================

llm = ChatGroq(
    model_name="openai/gpt-oss-120b",
    temperature=0,
    groq_api_key=GROQ_API_KEY,
)


# ============================================================
# RAG QUESTION ANSWERING
# ============================================================

def perform_qa(query):

    db = FAISS.load_local(
        "vector_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    rqa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    result = rqa.invoke(query)

    return result["result"]


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# FILE UPLOAD CONFIGURATION
# ============================================================

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(pdf_path):

    with open(pdf_path, "rb") as file:

        reader = PyPDF2.PdfReader(file)

        text = ""

        for page_num in range(len(reader.pages)):

            page_text = reader.pages[page_num].extract_text()

            if page_text:
                text += page_text

    return text


# ============================================================
# RESUME ANALYSIS PROMPT
# ============================================================

resume_summary_template = """

Role:
You are an AI Career Coach.

Task:
Given the candidate's resume, provide a comprehensive summary
that includes the following key aspects:

- Career Objective
- Skills and Expertise
- Professional Experience
- Educational Background
- Notable Achievements

Instructions:

Provide a concise summary of the resume, focusing on the
candidate's skills, experience, and career trajectory.

Ensure the summary is well-structured, clear, and highlights
the candidate's strengths in alignment with industry standards.

Resume:

{resume}

"""


resume_prompt = PromptTemplate(
    input_variables=["resume"],
    template=resume_summary_template,
)


# ============================================================
# RESUME ANALYSIS CHAIN
# ============================================================

resume_analysis_chain = LLMChain(
    llm=llm,
    prompt=resume_prompt,
)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def index():

    return render_template("index.html")


# ============================================================
# UPLOAD RESUME
# ============================================================

@app.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:

        return redirect(url_for("index"))

    file = request.files["file"]

    if file.filename == "":

        return redirect(url_for("index"))

    if file:

        # ----------------------------------------------------
        # Save uploaded PDF
        # ----------------------------------------------------

        filename = secure_filename(file.filename)

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(file_path)


        # ----------------------------------------------------
        # Extract PDF text
        # ----------------------------------------------------

        resume_text = extract_text_from_pdf(file_path)


        # ----------------------------------------------------
        # Split resume into chunks
        # ----------------------------------------------------

        splitted_text = text_splitter.split_text(resume_text)


        # ----------------------------------------------------
        # Create FAISS vector database
        # ----------------------------------------------------

        vectorstore = FAISS.from_texts(
            splitted_text,
            embeddings
        )


        # ----------------------------------------------------
        # Save FAISS index
        # ----------------------------------------------------

        vectorstore.save_local("vector_index")


        # ----------------------------------------------------
        # Analyze resume using Groq
        # ----------------------------------------------------

        resume_analysis = resume_analysis_chain.run(
            resume=resume_text
        )


        # ----------------------------------------------------
        # Display results
        # ----------------------------------------------------

        return render_template(
            "results.html",
            resume_analysis=resume_analysis
        )


# ============================================================
# ASK QUESTION
# ============================================================

@app.route("/ask", methods=["GET", "POST"])
def ask_query():

    if request.method == "POST":

        query = request.form["query"]

        result = perform_qa(query)

        return render_template(
            "qa_results.html",
            query=query,
            result=result
        )

    return render_template("ask.html")


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)