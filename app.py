# app.py
# This is the MAIN file of our project. Running this file starts the web app.
# It connects pdf_reader.py (extracts PDF text) with gemini_helper.py (talks to AI)
# and displays everything using Streamlit (a library that builds web UIs with pure Python).

# Import streamlit and give it a short nickname "st" (this is the standard convention).
import streamlit as st

# Import our own function from pdf_reader.py to extract text from a PDF.
from pdf_reader import extract_text_from_pdf

# Import our own functions from gemini_helper.py to talk to the Gemini AI model.
from gemini_helper import generate_summary, answer_question, explain_simply


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

# st.set_page_config() customizes the browser tab title and layout.
# This must be the FIRST streamlit command in the script.
# layout="wide" gives us more horizontal space to work with.
st.set_page_config(page_title="Smart Notes Agent", page_icon="📄", layout="wide")

# -----------------------------
# CUSTOM COLORFUL STYLING
# -----------------------------
# Streamlit lets us inject raw CSS using st.markdown() with unsafe_allow_html=True.
# "unsafe_allow_html" just means "trust this HTML/CSS, don't escape it as plain text."
# We use this ONE time near the top to define colors/styles for the whole app.
st.markdown("""
    <style>
    /* Change the overall page background to a soft gradient */
    .stApp {
        background: linear-gradient(180deg, #f6f5ff 0%, #ffffff 100%);
    }

    /* Style the main title area with a colorful gradient card */
    .title-card {
        background: linear-gradient(90deg, #7F77DD 0%, #D4537E 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
    }
    .title-card h1 {
        color: white !important;
        margin: 0;
    }
    .title-card p {
        color: #f0eaff;
        margin: 0.3rem 0 0 0;
    }

    /* Colorful section headers - each feature gets its own accent color */
    .section-summary {
        background-color: #E1F5EE;
        border-left: 6px solid #1D9E75;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        margin: 1.5rem 0 0.8rem 0;
    }
    .section-question {
        background-color: #E6F1FB;
        border-left: 6px solid #378ADD;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        margin: 1.5rem 0 0.8rem 0;
    }
    .section-explain {
        background-color: #FAEEDA;
        border-left: 6px solid #BA7517;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        margin: 1.5rem 0 0.8rem 0;
    }
    .section-summary h3, .section-question h3, .section-explain h3 {
        margin: 0;
        color: #2C2C2A;
    }

    /* Make buttons colorful and rounded */
    .stButton > button {
        background: linear-gradient(90deg, #7F77DD 0%, #534AB7 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #534AB7 0%, #3C3489 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Build the colorful title banner using our "title-card" CSS class above.
st.markdown("""
    <div class="title-card">
        <h1>📄 Smart Notes Agent</h1>
        <p>Upload a PDF, get a summary, ask questions, and understand tricky topics — all in simple English.</p>
    </div>
""", unsafe_allow_html=True)


# -----------------------------
# SESSION STATE SETUP
# -----------------------------
# Streamlit reruns the ENTIRE script every time you click a button or interact with the page.
# Normal variables would be wiped out each time. "session_state" is Streamlit's way of
# remembering values (like a memory box) between these reruns, for one user's session.

# We check if "pdf_text" already exists in memory. If not, we create it as an empty string.
# This will store the extracted PDF text so we don't need to re-extract it every rerun.
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""


# -----------------------------
# STEP 1: UPLOAD PDF
# -----------------------------

# st.file_uploader() shows a file upload button in the UI.
# type=["pdf"] restricts uploads to only PDF files.
uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

# We only try to process the file if the user has actually uploaded one.
if uploaded_file is not None:

    # We use a "spinner" to show a loading message while extraction happens.
    # This gives the user feedback that something is happening in the background.
    with st.spinner("Reading your PDF..."):

        # Call our function from pdf_reader.py to get the text out of the PDF.
        extracted_text = extract_text_from_pdf(uploaded_file)

        # Save the extracted text into session_state so it survives page reruns
        # (e.g., when the user later clicks "Summarize" or asks a question).
        st.session_state.pdf_text = extracted_text

    # st.success() shows a green confirmation box.
    st.success("PDF uploaded and text extracted successfully!")

    # st.expander() creates a collapsible section, so the raw text doesn't clutter the page.
    with st.expander("Click to view extracted text"):
        # We only show the first 3000 characters to avoid overwhelming the page.
        st.write(st.session_state.pdf_text[:3000])


# -----------------------------
# STEP 2: GENERATE SUMMARY
# -----------------------------

st.markdown('<div class="section-summary"><h3>📝 Get a Summary</h3></div>', unsafe_allow_html=True)

# st.button() displays a clickable button. It returns True only in the run
# where the user just clicked it, otherwise False.
if st.button("Summarize PDF"):

    # We check that there IS extracted text before calling the AI.
    # This avoids sending an empty document to Gemini.
    if st.session_state.pdf_text == "":
        # st.warning() shows a yellow warning box.
        st.warning("Please upload a PDF first.")
    else:
        # Show a spinner while waiting for Gemini's response (API calls take a few seconds).
        with st.spinner("Generating summary..."):
            # Call our AI function from gemini_helper.py.
            summary = generate_summary(st.session_state.pdf_text)

        # Display the AI's summary in a nicely formatted markdown block.
        st.subheader("Summary")
        st.markdown(summary)


# -----------------------------
# STEP 3: ASK A QUESTION
# -----------------------------

st.markdown('<div class="section-question"><h3>❓ Ask a Question About the PDF</h3></div>', unsafe_allow_html=True)

# st.text_input() creates a single-line text box for the user to type into.
user_question = st.text_input("Type your question here")

# Another button, this time for submitting the question.
if st.button("Get Answer"):

    if st.session_state.pdf_text == "":
        st.warning("Please upload a PDF first.")
    elif user_question.strip() == "":
        # .strip() removes extra spaces; this checks if the box was left empty.
        st.warning("Please type a question.")
    else:
        with st.spinner("Thinking..."):
            answer = answer_question(st.session_state.pdf_text, user_question)

        st.subheader("Answer")
        st.markdown(answer)


# -----------------------------
# STEP 4: EXPLAIN A DIFFICULT TOPIC SIMPLY
# -----------------------------

st.markdown('<div class="section-explain"><h3>💡 Explain a Difficult Topic Simply</h3></div>', unsafe_allow_html=True)

# Another text box, this time for the topic the user finds confusing.
topic_input = st.text_input("Enter a topic or term from the PDF you want explained simply")

if st.button("Explain Simply"):

    if st.session_state.pdf_text == "":
        st.warning("Please upload a PDF first.")
    elif topic_input.strip() == "":
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Simplifying..."):
            explanation = explain_simply(st.session_state.pdf_text, topic_input)

        st.subheader("Simple Explanation")
        st.markdown(explanation)
