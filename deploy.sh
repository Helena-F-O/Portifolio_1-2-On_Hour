#!/bin/bash

# Verifica se a aplicação está rodando na porta 5000 e a mata se necessário
sudo lsof -i :5000
sudo kill $(lsof -t -i :5000)
# Você também pode usar o PID diretamente
# sudo kill 28235

# Acessa o diretório do projeto
cd ~/Portifolio_1-2-On_Hour

# Ativa o ambiente virtual
source venv/bin/activate

# Realiza o git pull para puxar as alterações mais recentes
git pull origin main

# Reinicia a aplicação Flask
# Você pode usar tmux para rodar a aplicação em uma nova sessão
tmux new-session -d -s minha_sessao 'python app.py'

# Verifica se a aplicação foi iniciada
echo "Aplicação reiniciada com sucesso!"
