# 🛡️ Clara — Assistente de Segurança Financeira

> **Sua aliada contra golpes digitais e na educação financeira. Simples, confiável e sempre ao seu lado.**

Clara é uma assistente virtual brasileira construída sobre o **IBM watsonx Orchestrate**, especializada em dois temas críticos para o dia a dia dos brasileiros: **prevenção de golpes digitais** e **educação financeira**.

---

## 🌐 Acesso

| Canal | URL |
|---|---|
| **Site público** | https://clara-website-37732a34.s3-web.eu-gb.cloud-object-storage.appdomain.cloud |
| **Plataforma** | https://eu-gb.watson-orchestrate.cloud.ibm.com |

---

## 📋 Sobre o projeto

### O que a Clara faz

**Área 1 — Análise de Golpes Digitais**
- Analisa mensagens suspeitas recebidas por SMS, e-mail ou WhatsApp
- Identifica padrões de phishing, smishing, vishing, PIX fraudulento, WhatsApp clonado, romance scam e outros
- Retorna uma análise estruturada com nível de risco (Baixo / Médio / Alto / Muito Alto), indicadores encontrados e orientações práticas
- Indica onde denunciar (Safernet, Banco Central, Polícia Civil, Procon)

**Área 2 — Educação Financeira**
- Responde dúvidas sobre taxa Selic, CDI, juros compostos, Tesouro Direto, CDB, poupança
- Orienta sobre gestão de dívidas, Desenrola Brasil, score de crédito
- Explica orçamento pessoal (método 50-30-20), crédito consignado, PIX seguro
- Adapta o nível de explicação ao conhecimento do usuário

### Guardrails de segurança
- Detecta e recusa processar dados pessoais sensíveis (CPF, senhas, números de cartão, tokens)
- Nunca garante resultados de investimentos
- Não presta aconselhamento jurídico formal
- Redireciona perguntas fora do escopo educadamente

---

## 🏗️ Arquitetura

```
Usuário
  │
  ▼
Site HTML/CSS (IBM Cloud Object Storage — eu-gb)
  │
  ▼
Webchat Widget (IBM watsonx Orchestrate)
  │
  ├─► Knowledge Base (clara_knowledge_base)
  │     ├── golpes-digitais-guia.txt
  │     └── educacao-financeira-guia.txt
  │
  ├─► Tool: busca_web
  │     └── Busca alertas em bcb.gov.br, febraban.org.br, safernet.org.br, cert.br
  │
  └─► LLM: ibm/granite-3-8b-instruct
```

---

## 📁 Estrutura do projeto

```
.
├── agents/
│   └── clara.yaml                        # Definição do agente Clara
├── tools/
│   └── busca_web.py                      # Tool de busca web (@tool Python)
├── knowledge-bases/
│   ├── clara-knowledge-base.yaml         # Configuração da KB vetorial
│   └── docs/
│       ├── golpes-digitais-guia.txt      # Conteúdo sobre golpes digitais
│       └── educacao-financeira-guia.txt  # Conteúdo sobre educação financeira
├── website/
│   ├── index.html                        # Site público com embed do webchat
│   └── style.css                         # Estilos do site
├── scripts/
│   ├── import-all.sh                     # Importa todos os recursos no watsonx Orchestrate
│   ├── delete-all.sh                     # Remove todos os recursos (ordem inversa)
│   └── deploy_cos.py                     # Deploy do site no IBM COS
├── agente-segfinan-config.md             # Documento de configuração completo
├── agent-segfinan-plan.md                # Plano de desenvolvimento
└── workspace_config.yaml                 # Configuração de pastas do ADK
```

---

## 🚀 Como executar localmente / reimplantar

### Pré-requisitos

- Python 3.11+
- IBM watsonx Orchestrate ADK (`pip install ibm-watsonx-orchestrate`)
- Conta IBM Cloud com instância do watsonx Orchestrate
- IBM Cloud API Key

### 1. Configurar o ambiente

```bash
# Criar e ativar o venv
python -m venv venv
source venv/bin/activate          # Linux/Mac
.\venv\Scripts\Activate.ps1       # Windows PowerShell

# Instalar dependências
pip install ibm-watsonx-orchestrate
```

### 2. Ativar o ambiente watsonx Orchestrate

```bash
# Adicionar o ambiente (primeira vez)
orchestrate env add -n wxo-hackathon \
  -u "https://api.eu-gb.watson-orchestrate.cloud.ibm.com/instances/224ae8b9-2618-44b2-8b87-58871f65a40a" \
  -t ibm_iam

# Ativar
orchestrate env activate wxo-hackathon -a "$IBM_CLOUD_API_KEY"
```

### 3. Importar todos os recursos

```bash
chmod +x scripts/import-all.sh
./scripts/import-all.sh
```

Isso importa na ordem correta: **Knowledge Base → Tool → Agente**

### 4. Verificar o deploy

```bash
orchestrate agents list
orchestrate knowledge-bases status -n clara_knowledge_base
orchestrate tools list
```

### 5. (Opcional) Reimplantar o site no IBM COS

```bash
# Configurar credenciais HMAC do COS como variáveis de ambiente
export COS_ACCESS_KEY_ID="<seu_access_key_id>"
export COS_SECRET_ACCESS_KEY="<seu_secret_access_key>"

# Deploy
python scripts/deploy_cos.py
```

---

## 🧹 Remover todos os recursos

```bash
chmod +x scripts/delete-all.sh
./scripts/delete-all.sh
```

---

## 🔧 Como atualizar a base de conhecimento

1. Edite os arquivos em [`knowledge-bases/docs/`](knowledge-bases/docs/)
2. Reimporte a KB:
   ```bash
   orchestrate knowledge-bases import -f knowledge-bases/clara-knowledge-base.yaml
   orchestrate knowledge-bases status -n clara_knowledge_base
   ```

---

## 🧪 Como testar a Clara

**Via UI:** Acesse https://eu-gb.watson-orchestrate.cloud.ibm.com → AI Agents → Clara → Chat

**Prompts de teste sugeridos:**

| Teste | Entrada | Resultado esperado |
|---|---|---|
| Phishing | `"Recebi e-mail da Receita Federal pedindo meu CPF"` | Nível de risco Alto, formato padronizado |
| Educação financeira | `"O que é taxa Selic?"` | Explicação didática com exemplo prático |
| Detecção de PII | `"Meu CPF é 123.456.789-00"` | Aviso de dados sensíveis + recusa de processar |
| Golpe recente | Descrever golpe não listado na KB | Aciona `busca_web`, cita fonte |
| Fora do escopo | `"Qual o melhor time de futebol?"` | Redirecionamento educado |

---

## 🛡️ Privacidade e conformidade

- A Clara **não armazena dados pessoais** dos usuários
- Em conformidade com a **LGPD (Lei 13.709/2018)**
- Nunca solicita nem processa CPF, senhas, dados bancários ou tokens
- O histórico de conversas fica na infraestrutura da IBM Cloud

---

## 📚 Fontes de conhecimento

| Categoria | Fontes |
|---|---|
| Golpes digitais | Banco Central, Febraban, Safernet, CERT.br, Polícia Civil, Serasa |
| Educação financeira | Banco Central (Cidadania Financeira), CVM, ENEF, Serasa Ensina, Tesouro Nacional |

---

## 🔗 Links úteis

- [IBM watsonx Orchestrate](https://www.ibm.com/products/watsonx-orchestrate)
- [ADK Documentation](https://developer.watson-orchestrate.ibm.com)
- [Safernet — Denunciar crime digital](https://new.safernet.org.br/denuncie)
- [Banco Central — Registrar reclamação](https://www.bcb.gov.br/estabilidadefinanceira/registrarreclamacao)
- [Febraban — Segurança digital](https://febraban.org.br/seguranca)

---

*Projeto desenvolvido com IBM watsonx Orchestrate ADK v2.20.0*
