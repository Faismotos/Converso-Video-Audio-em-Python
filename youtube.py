"""
PROJETO: YouTube Downloader Pro
AUTOR: Tiago Facimoto
DATA: 15/03/2026
DESCRIÇÃO: Aplicativo gráfico para download de vídeos e 
           áudios do YouTube utilizando yt-dlp e CustomTkinter.
"""

import os
import yt_dlp
import customtkinter as ctk
from tkinter import messagebox

# Configuração do caminho da Área de Trabalho (Desktop)
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# Configurações visuais do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def validar_url(url):
    """Verifica se o link inserido começa com os protocolos corretos."""
    return url.startswith("http://") or url.startswith("https://")

def baixar_video():
    """Lógica para processar e baixar o vídeo na qualidade selecionada."""
    url = entry_url.get().strip()
    qualidade = qualidade_var.get()

    if not url:
        messagebox.showerror("Erro", "Cole um link do YouTube")
        return

    if not validar_url(url):
        messagebox.showerror("Erro", "URL inválida. Use http:// ou https://")
        return

    # Mapeamento de resoluções para IDs específicos do YouTube
    formatos = {
        "144p": "17", "240p": "36", "360p": "18", "480p": "135",
        "720p": "22", "1080p": "137", "2160p": "313"
    }

    # Define a qualidade baseada na escolha do usuário
    quality_id = formatos.get(qualidade)
    output_format = f"{quality_id}+bestaudio/best" if quality_id else "bestvideo+bestaudio/best"

    opcoes = {
        'format': output_format,
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(desktop, '%(title)s.%(ext)s'),
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])
        messagebox.showinfo("Sucesso", "Download concluído!")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha no download: {e}")

def baixar_mp3():
    """Lógica para extrair apenas o áudio e converter para MP3."""
    url = entry_url.get().strip()

    if not url or not validar_url(url):
        messagebox.showerror("Erro", "Verifique o link do YouTube")
        return

    opcoes = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(desktop, '%(title)s.%(ext)s'),
        'nocheckcertificate': True,
    }

    try:
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])
        messagebox.showinfo("Sucesso", "MP3 baixado!")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha no download: {e}")

# --- Configuração da Interface Gráfica (GUI) ---
app = ctk.CTk()
app.title("YouTube Downloader Pro | By Tiago Facimoto") # Nome do autor no título
app.geometry("500x320")
app.resizable(False, False)

# Widgets da tela
titulo = ctk.CTkLabel(app, text="YouTube Downloader", font=("Arial", 22, "bold"))
titulo.pack(pady=20)

entry_url = ctk.CTkEntry(app, width=400, placeholder_text="Cole o link do YouTube aqui...")
entry_url.pack(pady=10)

qualidade_var = ctk.StringVar(value="720p")
menu = ctk.CTkOptionMenu(
    app, 
    values=["144p", "240p", "360p", "480p", "720p", "1080p", "2160p"],
    variable=qualidade_var
)
menu.pack(pady=10)

# Botões de ação
botao_download = ctk.CTkButton(app, text="Baixar Vídeo", command=baixar_video, fg_color="green", hover_color="#013220")
botao_download.pack(pady=5)

botao_mp3 = ctk.CTkButton(app, text="Baixar MP3 (Áudio)", command=baixar_mp3)
botao_mp3.pack(pady=5)

# Rodapé de créditos no app
creditos = ctk.CTkLabel(app, text="Desenvolvido por Tiago Facimoto", font=("Arial", 10))
creditos.pack(side="bottom", pady=5)

app.mainloop()