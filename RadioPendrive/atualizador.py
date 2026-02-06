import os
import json
import requests
import zipfile
import io
import shutil
import datetime
import socket

LOG_FILE = "atualizacao.log"

def registrar_log(mensagem):
    """Grava mensagens no arquivo de log com data e hora"""
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log.write(f"[{data}] {mensagem}\n")
    print(mensagem)

def verificar_conexao():
    """Verifica se há conexão com a internet"""
    try:
        socket.create_connection(("github.com", 80), timeout=5)
        return True
    except OSError:
        return False

# Carregar configurações
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

repo_url = config["repositorio"]
folders = config["pastas"]
local_repo = "repo_temp"

registrar_log("🔄 Iniciando atualização da Rádio Pendrive...")

# Verificar conexão com internet
if not verificar_conexao():
    registrar_log("❌ Sem conexão com a internet. Atualização cancelada.")
    exit()

# Montar URL do .zip do GitHub
zip_url = repo_url.replace("github.com", "codeload.github.com") + "/zip/refs/heads/main"

# Baixar arquivo ZIP
registrar_log("📥 Baixando arquivos do GitHub...")
response = requests.get(zip_url)
if response.status_code != 200:
    registrar_log(f"❌ Erro ao baixar repositório: {response.status_code}")
    exit()

# Extrair ZIP em memória
with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
    zip_ref.extractall(local_repo)

# Caminho da pasta dentro do zip
repo_folder = os.path.join(local_repo, "project-python-Radiopendrive-main")

# Sincronizar as pastas configuradas
novos_arquivos = 0
for folder in folders:
    source_path = os.path.join(repo_folder, folder)
    target_path = os.path.join(folder)

    if not os.path.exists(source_path):
        registrar_log(f"⚠️ Pasta {folder} não encontrada no repositório.")
        continue

    os.makedirs(target_path, exist_ok=True)

    for file in os.listdir(source_path):
        src_file = os.path.join(source_path, file)
        dst_file = os.path.join(target_path, file)

        if not os.path.exists(dst_file):
            shutil.copy2(src_file, dst_file)
            novos_arquivos += 1
            registrar_log(f"➕ Novo arquivo copiado: {file}")
        else:
            registrar_log(f"✅ Já atualizado: {file}")

# Limpar pasta temporária
shutil.rmtree(local_repo)

registrar_log(f"🎧 Atualização concluída! {novos_arquivos} novos arquivos adicionados.")
registrar_log("-" * 60 + "\n")
