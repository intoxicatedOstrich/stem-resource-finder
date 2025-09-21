import streamlit as st
import pandas as pd
import numpy as np
import io

# from extract_thinker.markdown import MarkdownConverter
from extract_thinker import MarkdownConverter, DocumentLoaderPyPdf, DocumentLoaderLLMImage
from extract_thinker.llm import LLM
from extract_thinker.global_models import get_lite_model # gemini-2.5-flash-preview-05-20; Helper for model config
# source code: https://github.com/enoch3712/ExtractThinker/tree/main/extract_thinker

# Initialize
markdown_converter = MarkdownConverter()

# Load components later
pdf_loader = DocumentLoaderPyPdf() # Configure as needed
img_loader = DocumentLoaderLLMImage() # Configure as needed
# Use helper functions to get model configurations
# Replace with your actual logic for selecting/configuring models if needed
llm = LLM(get_lite_model())

# markdown_converter.load_document_loader(loader)
markdown_converter.load_llm(llm)

st.title('STEM Problem Progressor')

# class Prob_prompt:
prob = st.text_area("Enter your question here:")
file = st.file_uploader("Upload a PDF file or image of the problem:", type=["png", "jpg", "jpeg", "pdf"])


md_input = ""

if not str.isspace(prob):
    md_input = st.markdown(prob)

sight = True

# Display the uploaded image
if file is not None:
    if file.name.lower().endswith(".pdf"):
        sight = False
        markdown_converter.load_document_loader(pdf_loader)
    else:
        st.image(file, caption="Uploaded Image", use_container_width=True)
        markdown_converter.load_document_loader(img_loader)
    md_input = markdown_converter.to_markdown(file, vision=sight) 

    st.write(md_input)



# # Convert with vision enabled (processes text and images using LLM)
# markdown_pages_vision = markdown_converter.to_markdown(file, vision=True) 
# # Returns List[str]

# # Convert specific pages (1-indexed)
# markdown_specific_pages = markdown_converter.to_markdown(file, vision=True, pages=[1, 3, 5])
# # Returns List[str] with only the specified pages

# for i, page_md in enumerate(markdown_pages_vision):
#     print(f"--- Page {i+1} ---")
#     print(page_md)