# Project-Python-Radiopendrive



### 🧩 1. Estrutura do Pendrive

Organize seu pendrive assim:

/RadioPendrive <br>
 ├── musicas/ <br>
 ├── falas/ <br>
 ├── vinhetas/ <br>
 ├── noticias/ <br>
 ├── piadas/ <br>
 ├── atualizador.py <br>
 └── config.json <br>



### ⚙️ 2. Lógica do Atualizador

O script atualizador.py fará:
Detectar as pastas locais.
Acessar um repositório do GitHub (via API ou git clone/pull).
Comparar e copiar novos arquivos (sem apagar os já existentes).
Exibir log no terminal (“Baixando nova fala...”, “Música já atualizada” etc).



### 🧠 3. Exemplo de Configuração (config.json)

Esse arquivo guarda as URLs do GitHub (você pode alterar facilmente):



### 💻 4. Script Automático em Python

atualizador.py.
Ele usa a biblioteca gitpython para sincronizar com o GitHub.



### ⚙️ 5. Automação ao Conectar o Pendrive (opcional)

Se quiser que o script rode automaticamente ao conectar o pendrive:
No Windows, crie um arquivo autorun.inf.




