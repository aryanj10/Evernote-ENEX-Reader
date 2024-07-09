import streamlit as st
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import os

def parse_enex(file):
    tree = ET.parse(file)
    root = tree.getroot()
    notes = []
    for note in root.findall('note'):
        title = note.find('title').text if note.find('title') is not None else 'No Title'
        created = note.find('created').text if note.find('created') is not None else 'No Date'
        content = note.find('content').text if note.find('content') is not None else 'No Content'
        
        author_tag = note.find('note-attributes/author')
        author = author_tag.text if author_tag is not None else 'Unknown Author'
        
        soup = BeautifulSoup(content, 'html.parser')
        text_content = soup.get_text()
        
        notes.append({
            'title': title,
            'created': created,
            'author': author,
            'content': text_content
        })
    return notes

st.title("ENEX File Uploader")
st.write("Upload an ENEX file to extract and display the notes.")

uploaded_file = st.file_uploader("Choose an ENEX file", type="enex")

if uploaded_file is not None:
    notes = parse_enex(uploaded_file)
    for note in notes:
        st.header(note['title'])
        st.subheader(f"Created: {note['created']}")
        st.subheader(f"Author: {note['author']}")
        st.write(note['content'])
        st.write("---")
