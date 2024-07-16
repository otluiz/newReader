# newReader

## Descrição
newReader é uma aplicação que converte texto de documentos `.docx` em áudio, utilizando a tecnologia de Text-to-Speech (TTS). O projeto inclui funcionalidades para substituir abreviações e termos específicos através de um "bag of words", além de uma interface web para facilitar o uso.

## Motivo do Projeto

Olá colegas,

O motivo de ter criado este projeto é porque as plataformas de leitura de texto para áudio, para quem estuda, cobram um absurdo caso seu arquivo de áudio gerado tenha mais que alguns minutos. Então nós estamos criando este projeto que teoricamente não tem limite de geração de arquivo de áudio, vai depender somente do seu limite de espaço em disco.

Convidamos os colegas programadores (e não só) a contribuírem com nosso projeto.

A interface Web ainda está para ser criada e uma versão Mobile está no nosso escopo.

## Funcionalidades
- Conversão de texto de documentos `.docx` (por enquanto) em áudio.
- Substituição de abreviações e termos através de um "bag of words".
- Interface web para upload de arquivos e download do áudio gerado(ainda por implementar).
- Destaque de texto sincronizado com a reprodução do áudio (em desenvolvimento).

## Estrutura do Projeto

```plaintext
newReader/
│
├── app_v2.py
├── app_v3.py
├── app_v4.py
├── app_v5.py
├── app_v6.py
├── app.py
├── templates/
│   └── index.html
├── static/
│   └── styles.css
├── project_files/
│   └── (various project files)
├── bags/
│   └── (bag of words files)
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/otluiz/newReader.git
   cd newReader

2. Crie um ambiente virtual:

   python3 -m venv virtual_ambient
   source virtual_ambient/bin/activate

3. Instale as dependências:

   pip install -r requirements.txt

# USO
	
	Execute o servidor Flask:
	python app_v6.py
