# Resume Evaluation System using Generative AI and RAG

An AI-powered Resume Evaluation and Question-Answering application built with **Python, Flask, LangChain, Groq LLM, Hugging Face Embeddings, and FAISS**.

The application allows users to upload a resume in PDF format, extract its text, generate an AI-powered resume summary, and ask questions about the uploaded resume using Retrieval-Augmented Generation (RAG).

---

## 1. Project Overview

Recruiters and job seekers often need to understand a resume quickly. Manually reviewing long resumes and searching for specific information can take time.

This project uses Generative AI and RAG to make resume analysis easier.

### Main objectives

- Upload a resume in PDF format.
- Extract text from the uploaded PDF.
- Generate a structured resume summary using an LLM.
- Convert resume text into smaller chunks.
- Generate embeddings for semantic search.
- Store vectors in a FAISS vector database.
- Ask questions about the resume.
- Retrieve relevant information and generate AI answers.

## 2. Features

| Feature | Description |
|---|---|
| PDF Upload | Upload a resume in PDF format |
| Text Extraction | Extract resume text using PyPDF2 |
| Resume Summary | Generate an AI-based summary |
| Skills and Experience | Summarize skills, experience, education and achievements |
| Text Chunking | Split resume text into smaller chunks |
| Embeddings | Convert text into numerical representations |
| FAISS Vector Search | Retrieve relevant resume information |
| Resume Q&A | Ask questions about the uploaded resume |
| Web Interface | Use the application through a Flask interface |

**Note:** The current code creates a vector index for the uploaded resume and uses it for question answering. It does not currently implement a numerical ATS score, automated job-description matching, candidate ranking, or a downloadable evaluation report.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application framework |
| LangChain | LLM and RAG workflow |
| Groq | LLM inference |
| Hugging Face | Text embedding model |
| FAISS | Vector similarity search |
| PyPDF2 | PDF text extraction |
| python-dotenv | Environment variable management |
| HTML/CSS | Web interface |

### Models used in the current code

- **LLM:** `openai/gpt-oss-120b` through Groq.
- **Embedding model:** `sentence-transformers/all-MiniLM-L6-v2`.

## 4. Project Architecture

```text
                 USER
                   |
                   v
          Upload Resume PDF
                   |
                   v
          Flask Web Application
                   |
                   v
           PyPDF2 Extraction
                   |
                   v
             Resume Text
                   |
          +--------+---------+
          |                  |
          v                  v
    Resume Summary       Text Chunking
          |                  |
          v                  v
      Groq LLM           Embeddings
                             |
                             v
                       FAISS Vector DB
                             |
                             v
                      User Question
                             |
                             v
                      Similarity Search
                             |
                             v
                       Groq LLM
                             |
                             v
                        AI Answer
```

## 5. How the Project Works

### Step 1: Upload a resume

The user selects a PDF resume through the web interface.

The Flask application receives the file and saves it inside the `uploads/` folder.

### Step 2: Extract PDF text

PyPDF2 reads the uploaded PDF and extracts text from its pages.

The extracted text becomes the input for the AI analysis.

### Step 3: Generate a resume summary

The application sends the extracted resume text to the Groq LLM.

The prompt asks the model to summarize:

- Career objective
- Skills and expertise
- Professional experience
- Educational background
- Notable achievements

### Step 4: Split the text into chunks

The `CharacterTextSplitter` divides the resume into smaller text sections.

Current settings:

- Chunk size: 2000 characters
- Chunk overlap: 200 characters
- Separator: Newline (`\n`)

Chunking helps the retrieval system search smaller sections instead of processing the entire resume for every question.

### Step 5: Generate embeddings

The Hugging Face model `sentence-transformers/all-MiniLM-L6-v2` converts text chunks into numerical vectors.

These vectors represent the meaning of the text.

### Step 6: Store vectors in FAISS

FAISS stores the embeddings and supports similarity search.

The current application saves the index in the `vector_index/` directory.

### Step 7: Ask questions

The user can open the question-answering page and ask questions such as:

- What programming languages are mentioned?
- What is the candidate's educational background?
- Does the candidate have Python experience?
- What projects are listed in the resume?
- What is the candidate's professional experience?

The application retrieves relevant chunks and passes the question to the Groq LLM to generate an answer.

---

## 6. Project Folder Structure

The repository currently contains the following main items:

```text
Resume-Evaluation/
│
├── app.py
│
├── requirements.txt
│
├── templates/
│   ├── index.html
│   ├── results.html
│   ├── ask.html
│   └── qa_results.html
│
├── uploads/
│
├── vector_index/
│
├── templates.code-workspace
│
├── .gitignore
│
└── README.md
```

The HTML filenames above illustrate the template roles used by the application. Check your local `templates/` folder for the exact filenames in your copy.

### Important files and folders

- `app.py`: Main Flask application, PDF extraction, resume summary, vector creation and question-answering logic.
- `requirements.txt`: Python package dependencies.
- `templates/`: HTML pages rendered by Flask.
- `uploads/`: Stores uploaded PDF files.
- `vector_index/`: Stores the FAISS vector index.
- `.gitignore`: Specifies files and folders Git should ignore.
- `README.md`: Project documentation.

---

## 7. Prerequisites

Install the following before running the project:

1. Python 3.10 or later.
2. Visual Studio Code (recommended).
3. Git.
4. Internet connection.
5. A Groq API key.

Useful links:

- Python: https://www.python.org/downloads/
- VS Code: https://code.visualstudio.com/
- Git: https://git-scm.com/downloads
- Groq Console: https://console.groq.com/
- Hugging Face: https://huggingface.co/
- FAISS: https://github.com/facebookresearch/faiss

---

## 8. Clone the GitHub Repository

Open PowerShell or the VS Code terminal.

Run:

```powershell
git clone https://github.com/komalkumari88-kk/Resume-Evaluation.git
```

Move into the project folder:

```powershell
cd Resume-Evaluation
```

Check the files:

```powershell
dir
```

---

## 9. Create a Python Virtual Environment

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the environment's Python directly:

```powershell
.\venv\Scripts\python.exe -m pip install --upgrade pip
```

Check Python:

```powershell
python --version
```

---

## 10. Install Project Dependencies

Install the dependencies listed in the repository:

```powershell
python -m pip install -r requirements.txt
```

If installation completes successfully, continue to the API-key setup.

If you see an import error for a package, check whether that package is included in `requirements.txt` before installing it separately.

---

## 11. Configure the Groq API Key

The application needs a Groq API key to communicate with the LLM.

### Step 1

Open the Groq Console:

https://console.groq.com/

Create or sign in to your account and generate an API key.

### Step 2

Create a file named `.env` in the root project folder.

The project structure should look like this:

```text
Resume-Evaluation/
│
├── .env
├── app.py
├── requirements.txt
└── ...
```

### Step 3

Add the following inside `.env`:

```env
GROQ_API_KEY=your_actual_groq_api_key
```

Replace the example value with your own key.

**Security:** Never upload `.env` or your API key to GitHub. Do not paste your secret key into screenshots or public documentation.

---

## 12. Check the .gitignore File

Make sure your `.gitignore` includes:

```gitignore
.env
venv/
__pycache__/
*.pyc
uploads/
vector_index/
```

This prevents local secrets, environment files, uploaded resumes and generated vector indexes from being committed accidentally.

Only commit sample files that contain no real personal information.

---

## 13. Run the Application

From the project root, execute:

```powershell
python app.py
```

The application runs using Flask.

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

You should see the application's home page if the Flask server starts successfully and the required template files exist.

To stop the server, press:

```text
CTRL + C
```

---

## 14. How to Test the Project

### Test 1: Open the home page

Open:

```text
http://127.0.0.1:5000/
```

Check that the resume upload page appears.

### Test 2: Upload a PDF

1. Select a sample PDF resume.
2. Click the upload button.
3. Wait for the application to extract the text.
4. Check the generated resume summary.

Use a sample or your own test resume only with permission.

### Test 3: Ask questions

Open the question-answering page.

Try these example questions:

```text
What are the technical skills in this resume?

What is the candidate's educational qualification?

Which programming languages are mentioned?

What projects has the candidate completed?

Does the candidate have work experience?
```

Check whether the generated answers match the uploaded resume.

### Test 4: Check generated folders

After uploading a resume, check whether the application has created:

```text
uploads/
vector_index/
```

The `uploads/` folder contains the uploaded PDF. The `vector_index/` folder contains the FAISS index generated by the application.

---

## 15. Important Code Explanation

### PDF extraction

The function `extract_text_from_pdf()` uses `PyPDF2.PdfReader` to read each page and collect extracted text.

### Text splitting

The `CharacterTextSplitter` divides the extracted resume text into chunks with overlap.

### Embeddings

`HuggingFaceEmbeddings` uses the MiniLM model to convert each chunk into a vector representation.

### FAISS

`FAISS.from_texts()` creates the vector store, and `save_local()` saves it locally.

### Resume analysis

`PromptTemplate` defines the instructions for the resume summary. `LLMChain` sends the prompt and resume text to the configured LLM.

### Question answering

`RetrievalQA` connects the retriever with the LLM. The retriever searches for the four most relevant chunks using similarity search.

---

## 16. Troubleshooting

| Problem | What to check |
|---|---|
| `GROQ_API_KEY not found` | Check that `.env` exists and contains the key |
| `ModuleNotFoundError` | Activate the environment and install requirements |
| Flask page not found | Check the route and template filenames |
| PDF text is empty | Check whether the PDF contains selectable text |
| FAISS index not found | Upload a resume first to generate the index |
| Groq API error | Check the API key, model availability, rate limits and account access |
| Port already in use | Stop the other process or configure a different port |

### Important code correction

The upload route in the current `app.py` uses `redirect()` and `url_for()`, but these names are not included in the visible Flask import statement.

Change:

```python
from flask import Flask, render_template, request
```

To:

```python
from flask import Flask, render_template, request, redirect, url_for
```

Save the file before testing the upload route.

---

## 17. Security and Privacy

Resumes contain personal information. Follow these precautions:

- Use test resumes when demonstrating the project.
- Do not upload real candidate resumes to a public repository.
- Keep the Groq API key inside `.env`.
- Add `.env` to `.gitignore`.
- Do not share uploaded resumes without permission.
- Avoid deploying the development Flask server with debug mode enabled.
- Review the FAISS deserialization setting before loading indexes from untrusted sources. The current code uses `allow_dangerous_deserialization=True`; only load indexes that you trust.
- Consider deleting uploaded files after processing.

---

## 18. Future Improvements

The following are possible enhancements, not features confirmed in the current implementation:

1. Add ATS-style resume scoring.
2. Compare resumes with job descriptions.
3. Extract and categorize technical and soft skills.
4. Identify missing skills for a selected job role.
5. Add a downloadable PDF evaluation report.
6. Support multiple resume uploads.
7. Add source references to answers.
8. Add candidate comparison.
9. Add authentication and user history.
10. Deploy the application using a production-ready server.

---

## 19. Screenshots to Add to GitHub

Create a folder named `screenshots/` and add your own screenshots.

Suggested screenshots:

| Screenshot | What to capture |
|---|---|
| 1. Home Page | Resume Evaluation home page |
| 2. PDF Upload | Selecting a resume PDF |
| 3. Resume Summary | AI-generated resume summary |
| 4. Question Page | Asking a question about the resume |
| 5. AI Answer | Displayed question-answering result |
| 6. Terminal | Successful Flask application startup |
| 7. Project Structure | Files and folders in VS Code |

Use screenshots from your actual running application. Do not use sample images as proof that a feature works.

---

## 20. GitHub: Upload Your README Changes

After saving `README.md`, open PowerShell in the project root.

Check the changes:

```powershell
git status
```

Stage the README:

```powershell
git add README.md
```

Commit:

```powershell
git commit -m "Add detailed project README"
```

Push to GitHub:

```powershell
git push origin main
```

Refresh your repository page:

https://github.com/komalkumari88-kk/Resume-Evaluation

Your README should now appear on the repository home page.

---

## 21. Learning Outcomes

By completing and understanding this project, you can learn:

- Python web application development.
- Flask routing and HTML templates.
- PDF text extraction.
- Prompt engineering.
- LLM integration using Groq.
- LangChain chains and retrievers.
- Text embeddings.
- Vector databases and FAISS.
- Retrieval-Augmented Generation (RAG).
- API key and environment variable management.
- Git and GitHub project documentation.

---

## 22. Conclusion

The Resume Evaluation System demonstrates how Generative AI and Retrieval-Augmented Generation can be used to analyze resume content and answer questions about it.

It combines PDF processing, text embeddings, vector search, LangChain and a Groq-powered language model in a Flask application.

This project is a practical introduction to building AI-powered applications using Python and RAG.

---

**Repository:** https://github.com/komalkumari88-kk/Resume-Evaluation

**Author:** Komal Kumari
