import streamlit as st
from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def split_text_into_chunks(text, chunk_size=150):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def search_relevant_chunks(question, chunks):
    question_words = set(question.lower().split())
    scored_chunks = []

    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        score = len(question_words.intersection(chunk_words))
        scored_chunks.append((score, chunk))

    scored_chunks.sort(reverse=True, key=lambda x: x[0])

    best_chunks = [
        chunk for score, chunk in scored_chunks
        if score > 0
    ]

    return best_chunks[:3]


def show_document_chat():
    st.title("📄 Document Chat")

    st.write("Upload a PDF and ask questions from your notes.")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)

        if text:
            chunks = split_text_into_chunks(text)

            st.success("PDF uploaded and text extracted successfully!")

            with st.expander("View Extracted Text"):
                st.write(text[:3000])

            question = st.text_input("Ask a question from the PDF")

            if st.button("Get Answer"):
                if question:
                    relevant_chunks = search_relevant_chunks(question, chunks)

                    if relevant_chunks:
                        st.subheader("Relevant Answer from PDF")

                        for chunk in relevant_chunks:
                            st.write(chunk)
                            st.divider()
                    else:
                        st.warning("No relevant answer found in the PDF.")
                else:
                    st.warning("Please enter a question.")
        else:
            st.error("Could not extract text from this PDF.")
    else:
        st.info("Please upload a PDF to start.")