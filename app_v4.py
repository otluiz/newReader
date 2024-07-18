import os
import re
import time
from gtts import gTTS
from pydub import AudioSegment
from docx import Document
from tkinter import Tk, Text, Button, filedialog, END, INSERT, DISABLED, NORMAL, PhotoImage, Toplevel, Label
import pygame

# Configurações do projeto
PROJECT_DIR = "project_files"
ICON_PATH = os.path.join(PROJECT_DIR, "play_icon.png")

# Criação do diretório do projeto
if not os.path.exists(PROJECT_DIR):
    os.makedirs(PROJECT_DIR)

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
    "X-": "décimo",
    "XI-": "décimo primeiro",
    "XII-": "décimo segundo",
    "XIII-": "décimo terceiro",
    "XIV-": "décimo quarto",
    "XV-": "décimo quinto",
    "XVI-": "décimo sexto",
    "XVII-": "décimo sétimo",
    "XVIII-": "décimo oitavo",
    "XIX-": "décimo nono",
    "XX-": "vigésimo",
    "XXI-": "vigésimo primeiro",
    "XXII-": "vigésimo segundo",
    "XXIII-": "vigésimo terceiro",
    "XXIV-": "vigésimo quarto",
    "XXV-": "vigésimo quinto",
    "XXVI-": "vigésimo sexto",
    "XXVII-": "vigésimo sétimo",
    "XXVIII-": "vigésimo oitavo",
    "XXIX-": "vigésimo nono",
    "XXX-": "trigésimo"
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
    log_filename = os.path.join(PROJECT_DIR, f"{os.path.splitext(output_filename)[0]}_highlight.log")
    
    start_time = time.time()
    with open(log_filename, "w") as log_file:
        for i, part in enumerate(text_parts):
            tts = gTTS(part, lang='pt')
            temp_filename = os.path.join(PROJECT_DIR, f"temp_{i}.mp3")
            tts.save(temp_filename)
            temp_files.append(temp_filename)
            log_file.write(f"{time.time() - start_time:.2f}\n")
    
    combined = AudioSegment.empty()
    for temp_file in temp_files:
        combined += AudioSegment.from_mp3(temp_file)
        os.remove(temp_file)
    
    output_filepath = os.path.join(PROJECT_DIR, output_filename)
    combined.export(output_filepath, format="mp3")
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
        generate_button.config(state=NORMAL)
        play_button.config(state=DISABLED)

def play_audio_with_highlight(log_filename, audio_filename):
    """Reproduz o áudio e destaca o texto conforme o log"""
    with open(log_filename, "r") as log_file:
        lines = log_file.readlines()
    
    highlight_intervals = []
    for line in lines:
        timestamp = line.strip()
        highlight_intervals.append(float(timestamp))
    
    pygame.mixer.init()
    pygame.mixer.music.load(audio_filename)
    pygame.mixer.music.play()
    
    start_time = time.time()
    for interval in highlight_intervals:
        while time.time() - start_time < interval:
            time.sleep(0.1)
        # Use um método de destaque com base em intervalos ou outra lógica necessária para destacar o texto corretamente

def generate_audio():
    """Gera o áudio e o log de destaque"""
    text = text_box.get(1.0, END)
    output_filename = "output.mp3"
    log_filename = os.path.join(PROJECT_DIR, "output_highlight.log")
    
    if not (os.path.exists(output_filename) and os.path.exists(log_filename)):
        log_filename = text_to_speech_with_highlight(text, output_filename)
    
    play_button.config(state=NORMAL)

def play_audio():
    """Inicia a reprodução do áudio com destaque"""
    output_filename = os.path.join(PROJECT_DIR, "output.mp3")
    log_filename = os.path.join(PROJECT_DIR, "output_highlight.log")
    play_audio_with_highlight(log_filename, output_filename)

# Interface Gráfica com Tkinter
root = Tk()
root.title("Text to Speech with Highlight")

text_box = Text(root, wrap='word', width=100, height=30)
text_box.pack(pady=20)

load_button = Button(root, text="Load DOCX", command=load_docx)
load_button.pack(side='left', padx=10)

generate_button = Button(root, text="Generate Audio", command=generate_audio, state=DISABLED)
generate_button.pack(side='left', padx=10)

# Função para criar um tooltip
def create_tooltip(widget, text):
    tooltip = Toplevel(widget)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry("+0+0")
    label = Label(tooltip, text=text, background="yellow", relief="solid", borderwidth=1)
    label.pack()
    tooltip.withdraw()

    def enter(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        tooltip.wm_geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def leave(event):
        tooltip.withdraw()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

try:
    play_icon = PhotoImage(file=ICON_PATH)
    play_icon = play_icon.subsample(20, 20)  # Ajuste o tamanho do ícone conforme necessário
    play_button = Button(root, command=play_audio, state=DISABLED, image=play_icon)
    create_tooltip(play_button, "Play")
except Exception as e:
    print(f"Erro ao carregar ícone: {e}")
    play_button = Button(root, text="Play", command=play_audio, state=DISABLED)
    create_tooltip(play_button, "Play")

play_button.pack(side='right', padx=10)

root.mainloop()
