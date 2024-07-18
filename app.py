import os
import re
import time
from gtts import gTTS
from pydub import AudioSegment
from docx import Document
from tkinter import Tk, Text, Button, filedialog, END, INSERT
import pygame

# Dicionário para converter abreviações e algarismos romanos
roman_numerals = {
    "I-": "primeiro",
    "II-": "segundo",
    "III-": "terceiro",
    "IV-": "quarto",
    "V-": "quinto",
    "VI-": "sexto",
    "VII-": "sétimo",
    "VIII-": "oitavo",
    "IX-": "nono",
    "X-": "décimo"
}

def replace_abbreviations(text):
    """Substitui abreviações e algarismos romanos por texto completo"""
    text = re.sub(r'\bArt\.?\s*(\d+)', r'Artigo \1', text)
    for roman, full in roman_numerals.items():
        text = text.replace(roman, full)
    return text

def split_text(text, max_length=500):
    """Divide o texto em partes menores para evitar erros com o gTTS"""
    parts = []
    while len(text) > max_length:
        split_index = text.rfind(' ', 0, max_length)
        if split_index == -1:
            split_index = max_length
        parts.append(text[:split_index].strip())
        text = text[split_index:].strip()
    parts.append(text)
    return parts

def text_to_speech_with_highlight(text, output_filename="output.mp3"):
    """Converte o texto em áudio, salva em um arquivo e gera um log de destaque"""
    text_parts = split_text(text)
    temp_files = []
    log_filename = f"{os.path.splitext(output_filename)[0]}_highlight.log"
    
    with open(log_filename, "w") as log_file:
        for i, part in enumerate(text_parts):
            tts = gTTS(part, lang='pt')
            temp_filename = f"temp_{i}.mp3"
            tts.save(temp_filename)
            temp_files.append(temp_filename)
            log_file.write(f"Parte {i+1} começa às {time.time()} - '{part[:50]}...'\n")
    
    combined = AudioSegment.empty()
    for temp_file in temp_files:
        combined += AudioSegment.from_mp3(temp_file)
        os.remove(temp_file)
    
    combined.export(output_filename, format="mp3")
    print(f"Log de destaque gerado: {log_filename}")

    return log_filename

def docx_to_text(docx_filename):
    """Lê um arquivo .docx e retorna seu conteúdo como uma string"""
    doc = Document(docx_filename)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def load_docx():
    """Carrega um arquivo .docx e insere o texto na caixa de texto"""
    filepath = filedialog.askopenfilename(filetypes=[("Document files", "*.docx")])
    if filepath:
        text = docx_to_text(filepath)
        text = replace_abbreviations(text)
        text_box.delete(1.0, END)
        text_box.insert(INSERT, text)

def play_audio_with_highlight(log_filename, audio_filename):
    """Reproduz o áudio e destaca o texto conforme o log"""
    with open(log_filename, "r") as log_file:
        lines = log_file.readlines()
    
    highlight_intervals = []
    for line in lines:
        parts = line.strip().split(" - ")
        timestamp = float(parts[0].split(" ")[-1])
        text_preview = parts[1]
        highlight_intervals.append((timestamp, text_preview))
    
    pygame.mixer.init()
    pygame.mixer.music.load(audio_filename)
    pygame.mixer.music.play()
    
    start_time = time.time()
    for interval in highlight_intervals:
        while time.time() - start_time < interval[0]:
            time.sleep(0.1)
        text_preview = interval[1]
        start_idx = text_box.search(text_preview, 1.0, stopindex=END)
        end_idx = f"{start_idx}+{len(text_preview)}c"
        text_box.tag_add("highlight", start_idx, end_idx)
        text_box.tag_config("highlight", background="yellow")
        text_box.see(start_idx)

def generate_and_play():
    """Gera o áudio e inicia a reprodução com destaque"""
    text = text_box.get(1.0, END)
    output_filename = "output.mp3"
    log_filename = text_to_speech_with_highlight(text, output_filename)
    play_audio_with_highlight(log_filename, output_filename)

# Interface Gráfica com Tkinter
root = Tk()
root.title("Text to Speech with Highlight")

text_box = Text(root, wrap='word', width=80, height=20)
text_box.pack(pady=20)

load_button = Button(root, text="Load DOCX", command=load_docx)
load_button.pack(side='left', padx=10)

generate_button = Button(root, text="Generate and Play", command=generate_and_play)
generate_button.pack(side='right', padx=10)

root.mainloop()
