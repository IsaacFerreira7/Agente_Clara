#!/usr/bin/env bash
# import-all.sh — Importa todos os recursos do agente Clara no watsonx Orchestrate
# Ordem: knowledge-base → tools → agent

set -e

# Detecta o venv (raiz do projeto primeiro, depois raiz do repositório)
if [ -f "./venv/bin/activate" ]; then
  source ./venv/bin/activate
elif [ -f "../venv/bin/activate" ]; then
  source ../venv/bin/activate
fi

echo "============================================"
echo " Importando recursos do agente Clara"
echo "============================================"

echo ""
echo "[1/3] Importando Knowledge Base..."
orchestrate knowledge-bases import -f knowledge-bases/clara-knowledge-base.yaml

echo ""
echo "[2/3] Importando Tools..."
orchestrate tools import -k python -f tools/busca_web.py

echo ""
echo "[3/3] Importando Agente Clara..."
orchestrate agents import -f agents/clara.yaml

echo ""
echo "============================================"
echo " Importação concluída com sucesso!"
echo " Agente 'clara' está disponível na plataforma."
echo "============================================"
