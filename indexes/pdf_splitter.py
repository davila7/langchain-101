from langchain import OpenAI
from langchain.document_loaders import PagedPDFSplitter
import os

loader = PagedPDFSplitter("files/layout-parser-paper.pdf")
pages = loader.load_and_split()