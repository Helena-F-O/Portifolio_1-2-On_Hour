#!/bin/bash

# Nome da sessão tmux
SESSION_NAME="minha_sessao"

# Verifica se a aplicação está rodando na porta 5000 e a mata se necessário
if sudo lsof -i :5000 > /dev/null; then
    echo "Encerrando processo na porta 5000..."
    sudo kill $(lsof -t -i :5000)
fi

# Acessa o diretório do projeto
cd ~/Portifolio_1-2-On_Hour || { echo "Diretório não encontrado!"; exit 1; }

# Ativa o ambiente virtual
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Ambiente virtual não encontrado! Certifique-se de que está configurado corretamente."
    exit 1
fi

# Realiza o git pull para puxar as alterações mais recentes
git pull origin main || { echo "Erro ao realizar git pull!"; exit 1; }

# Verifica se a sessão tmux já existe
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "Sessão tmux já existe. Reutilizando..."
    # Entra na sessão e executa o comando
    tmux send-keys -t $SESSION_NAME "source venv/bin/activate && python app.py" Enter
else
    echo "Criando uma nova sessão tmux..."
    # Cria a sessão e ativa o ambiente antes de rodar o app
    tmux new-session -d -s $SESSION_NAME "source venv/bin/activate && python app.py"
fi

# Verifica se a aplicação foi iniciada
echo "Aplicação reiniciada com sucesso!"
