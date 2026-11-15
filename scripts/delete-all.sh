#!/usr/bin/env bash
# delete-all.sh — Remove todos os recursos do agente Clara do watsonx Orchestrate
# Ordem inversa: agent → tools → knowledge-base

set -e

# Detecta o venv
if [ -f "./venv/bin/activate" ]; then
  source ./venv/bin/activate
elif [ -f "../venv/bin/activate" ]; then
  source ../venv/bin/activate
fi

echo "============================================"
echo " Removendo recursos do agente Clara"
echo "============================================"

echo ""
echo "[1/3] Removendo Agente..."
orchestrate agents remove -n clara --kind native || true

echo ""
echo "[2/3] Removendo Tools..."
orchestrate tools remove -n busca_web || true

echo ""
echo "[3/3] Removendo Knowledge Base..."
orchestrate knowledge-bases remove -n clara_knowledge_base || true

echo ""
echo "============================================"
echo " Remoção concluída."
echo "============================================"
