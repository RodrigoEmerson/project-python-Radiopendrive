import os
import json
import requests
import zipfile
import io
import shutil
import datetime
import time

LOG_FILE = "atualizacao.log"

def registrar_log(mensagem):
    """Grava mensagens no arquivo de log com data e hora"""
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log.write(f"[{data}] {mensagem}\n")
    print(mensagem)

def verificar_conexao():
    """Testa a conexão via HTTPS"""
    try:
        r = requests.get("https://github.com", timeout=5)
        return r.status_code == 200
    except requests.RequestException:
        return False

# Caminho absoluto do script
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, "config.json")

# Carregar configurações
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

repo_url = config["repositorio"].replace(".git", "")
folders = config["pastas"]
local_repo = os.path.join(base_dir, "repo_temp")

registrar_log("🔄 Iniciando atualização da Rádio Pendrive...")

if not verificar_conexao():
    registrar_log("❌ Sem conexão com a internet. Atualização cancelada.")
    exit()

zip_url = repo_url.replace("github.com", "codeload.github.com") + "/zip/refs/heads/main"

registrar_log(f"📥 Baixando arquivos de {zip_url} ...")
response = requests.get(zip_url)
if response.status_code != 200:
    registrar_log(f"❌ Erro ao baixar repositório: {response.status_code}")
    exit()

# Limpa diretório temporário antes de extrair
if os.path.exists(local_repo):
    shutil.rmtree(local_repo)

# Extrai ZIP
with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
    zip_ref.extractall(local_repo)

# Detecta automaticamente a pasta principal extraída
repo_folder = None
for item in os.listdir(local_repo):
    path = os.path.join(local_repo, item)
    if os.path.isdir(path):
        repo_folder = path
        break

if not repo_folder:
    registrar_log("❌ Não foi possível localizar a pasta principal no ZIP extraído.")
    exit()

registrar_log(f"📂 Pasta raiz detectada: {repo_folder}")

novos_arquivos = 0

for folder in folders:
    source_path = os.path.join(repo_folder, folder)
    target_path = os.path.join(base_dir, folder)

    if not os.path.exists(source_path):
        registrar_log(f"⚠️ Pasta {folder} não encontrada dentro do repositório.")
        continue

    os.makedirs(target_path, exist_ok=True)

    # Percorre todas as subpastas
    for root, dirs, files in os.walk(source_path):
        # Calcula o caminho relativo (ex: musicas/01/)
        relative_path = os.path.relpath(root, source_path)
        target_subdir = os.path.join(target_path, relative_path)

        os.makedirs(target_subdir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_subdir, file)

            try:
                if not os.path.exists(dst_file):
                    shutil.copy2(src_file, dst_file)
                    novos_arquivos += 1
                    registrar_log(f"➕ Novo arquivo copiado: {folder}/{relative_path}/{file}")
                else:
                    registrar_log(f"✅ Já atualizado: {folder}/{relative_path}/{file}")
            except Exception as e:
                registrar_log(f"⚠️ Erro ao copiar {folder}/{relative_path}/{file}: {e}")


shutil.rmtree(local_repo)
registrar_log(f"🎧 Atualização concluída! {novos_arquivos} novos arquivos adicionados.")
registrar_log("-" * 60 + "\n")
registrar_log("⏳ Aguardando 10 segundos antes de fechar...")
time.sleep(10)