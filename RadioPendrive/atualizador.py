import os
import json
import requests
import zipfile
import io
import shutil

# Carregar configurações
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

repo_url = config["repositorio"]
folders = config["pastas"]
local_repo = "repo_temp"

print("🔄 Iniciando atualização da Rádio Pendrive...")

# Montar URL do .zip (GitHub entrega assim)
zip_url = repo_url.replace("github.com", "codeload.github.com") + "/zip/refs/heads/main"

# Baixar arquivo ZIP
print("📥 Baixando arquivos do GitHub...")
response = requests.get(zip_url)
if response.status_code != 200:
    print("❌ Erro ao baixar repositório:", response.status_code)
    exit()

# Extrair ZIP em memória
with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
    zip_ref.extractall(local_repo)

# O GitHub cria uma pasta com nome "project-python-Radiopendrive-main"
repo_folder = os.path.join(local_repo, "project-python-Radiopendrive-main")

# Sincronizar as pastas configuradas
for folder in folders:
    source_path = os.path.join(repo_folder, folder)
    target_path = os.path.join(folder)

    if not os.path.exists(source_path):
        print(f"⚠️ Pasta {folder} não encontrada no repositório.")
        continue

    os.makedirs(target_path, exist_ok=True)

    for file in os.listdir(source_path):
        src_file = os.path.join(source_path, file)
        dst_file = os.path.join(target_path, file)

        if not os.path.exists(dst_file):
            print(f"➕ Novo arquivo encontrado: {file}")
            shutil.copy2(src_file, dst_file)
        else:
            print(f"✅ Já atualizado: {file}")

# Limpar repositório temporário
shutil.rmtree(local_repo)
print("🎧 Atualização concluída com sucesso!")
