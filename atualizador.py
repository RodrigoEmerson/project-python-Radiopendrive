import os
import json
import git
import shutil

# Carregar configurações
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

repo_url = config["repositorio"]
folders = config["pastas"]
local_repo = "repo_temp"

print("🔄 Iniciando atualização da Rádio Pendrive...")

# Se o repositório temporário existir, atualiza. Caso contrário, clona.
if os.path.exists(local_repo):
    print("➡️ Atualizando repositório existente...")
    repo = git.Repo(local_repo)
    repo.remotes.origin.pull()
else:
    print("📥 Clonando repositório...")
    git.Repo.clone_from(repo_url, local_repo)

# Sincronizar as pastas configuradas
for folder in folders:
    source_path = os.path.join(local_repo, folder)
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

print("🎧 Atualização concluída com sucesso!")
