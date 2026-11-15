# Plano — Agente de Segurança Financeira no IBM watsonx Orchestrate

## Visão Geral

**Objetivo:** Criar a configuração completa de um agente de IA no IBM watsonx Orchestrate capaz de:
1. Identificar e ajudar a prevenir golpes digitais (phishing, smishing, vishing, etc.).
2. Educar o usuário sobre finanças pessoais de forma didática e acessível.

**Público-alvo:** População brasileira em geral, usuários não técnicos.

**Idioma padrão:** Português do Brasil (pt-BR).

**Entregáveis deste plano:**
- Nome e identidade do agente
- System prompt / instruções principais
- Guidelines de comportamento e segurança
- Definições de skills (RAG + web search)
- Estrutura e configuração da base de conhecimento (RAG)
- Documento final consolidado pronto para uso no watsonx Orchestrate

---

## Sub-tarefa 1 — Nome, Identidade e Persona do Agente

**Status:** [x] concluído

### Intent
Definir o nome, a persona e a voz do agente. Uma identidade clara orienta toda a redação do system prompt e cria consistência na experiência do usuário.

### Expected Outcomes
- Nome do agente definido e justificado.
- Persona descrita (tom, estilo, valores).
- Tagline/descrição curta para exibição na interface do Orchestrate.

### Todo List
1. Escolher nome que transmita confiança, proteção e acessibilidade em pt-BR.
2. Redigir a persona em 3–5 frases (tom amigável, reassegurador, didático).
3. Escrever descrição curta (máx. 160 caracteres) para uso na interface.
4. Registrar tudo na seção correspondente do documento final.

### Relevant Context
- Público não técnico → nome simples, sem jargões.
- Tom: "amigo experiente que explica de forma simples, sem ser condescendente".

---

## Sub-tarefa 2 — System Prompt Principal

**Status:** [x] concluído

### Intent
Redigir o system prompt que será carregado como contexto inicial do agente no watsonx Orchestrate. Este prompt define o papel, as capacidades, as restrições e o fluxo de raciocínio do agente.

### Expected Outcomes
- System prompt completo em pt-BR, pronto para colar no campo "Agent Instructions" do Orchestrate.
- Cobre: identidade, escopo, dois domínios (golpes + educação financeira), restrições de dados pessoais, e instruções de uso das skills.

### Todo List
1. Definir o bloco de identidade (quem é o agente, o que faz).
2. Definir o bloco de escopo e limitações (o que o agente NÃO faz).
3. Redigir instruções para o domínio de detecção de golpes:
   - Como aceitar e analisar mensagens suspeitas.
   - Como estruturar a resposta de análise (indicadores → explicação → recomendação).
   - Quando e como acionar RAG e web search.
4. Redigir instruções para o domínio de educação financeira:
   - Como adaptar o nível de explicação ao usuário.
   - Como usar exemplos práticos.
   - Tópicos cobertos: planejamento, juros, crédito, dívidas, investimentos, orçamento, segurança financeira.
5. Redigir o bloco de segurança de dados pessoais (aviso ativo + recusa de processamento).
6. Redigir instruções de formato de resposta (markdown leve, listas, emojis com moderação).
7. Revisar e consolidar o prompt em um bloco único coerente.

### Relevant Context
- Plataforma: IBM watsonx Orchestrate — system prompt inserido no campo "Agent Instructions".
- O modelo subjacente (ex.: Llama 3 ou Granite) deve receber instruções claras e sem ambiguidade.
- Dados pessoais proibidos: CPF, números de conta, senhas, tokens.

---

## Sub-tarefa 3 — Guidelines de Comportamento e Guardrails

**Status:** [x] concluído

### Intent
Produzir um conjunto de regras de comportamento (guidelines) e guardrails explícitos que complementam o system prompt, cobrindo casos extremos, segurança e qualidade das respostas.

### Expected Outcomes
- Lista de guidelines numerados e prontos para uso.
- Seção específica de guardrails de privacidade/segurança.
- Orientações de escalada (quando indicar ajuda profissional ou autoridades).

### Todo List
1. Escrever guidelines gerais (linguagem, tom, estrutura de resposta).
2. Escrever guidelines de detecção de golpes (o que classificar, como graduar o risco: baixo/médio/alto).
3. Escrever guidelines de educação financeira (como adaptar complexidade, quando sugerir consultar um especialista).
4. Escrever guardrails de privacidade (detecção de PII na entrada, mensagem de recusa padrão).
5. Escrever guideline de escalada (Banco Central, Procon, Polícia Civil, Safernet).
6. Escrever guideline de limitações do agente (não presta aconselhamento jurídico ou médico, não acessa contas).

### Relevant Context
- Regulatório BR: LGPD (Lei 13.709/2018) — não processar dados pessoais sem consentimento.
- Órgãos de referência: Banco Central do Brasil, CVM, Procon, Safernet, Polícia Civil (delegacia de crimes virtuais).

---

## Sub-tarefa 4 — Definição de Skills (Ferramentas do Agente)

**Status:** [x] concluído

### Intent
Especificar as duas skills que o agente usará — RAG retrieval e web search — com seus parâmetros, triggers e instruções de uso, no formato compatível com o watsonx Orchestrate.

### Expected Outcomes
- Especificação da skill de RAG (nome, descrição, quando chamar, parâmetros).
- Especificação da skill de web search (nome, descrição, quando chamar, parâmetros, fontes prioritárias).
- Orientação de como registrar cada skill no Orchestrate.

### Todo List
1. Definir skill **RAG — Base de Conhecimento Anti-Golpes e Finanças**:
   - Nome, descrição funcional.
   - Trigger: quando o usuário apresenta mensagem suspeita ou pergunta factual sobre golpes/finanças.
   - Parâmetros: query string, top-k, filtro por categoria (golpes | finanças).
2. Definir skill **Web Search — Alertas e Notícias Atualizadas**:
   - Nome, descrição funcional.
   - Trigger: quando o conteúdo suspeito é muito recente ou não está na base RAG.
   - Parâmetros: query, fontes preferenciais (Banco Central, Safernet, Febraban, Procon).
   - Restrições: não usar como única fonte; sempre citar origem.
3. Documentar o fluxo de decisão de qual skill acionar.
4. Descrever como configurar cada skill na interface do Orchestrate (seção "Skills & Tools").

### Relevant Context
- watsonx Orchestrate suporta OpenAPI skills e built-in tools.
- RAG pode ser configurado via Watson Discovery ou watsonx.ai vector store.
- Web search pode usar o built-in search tool do Orchestrate ou um skill customizado via OpenAPI.

---

## Sub-tarefa 5 — Estrutura da Base de Conhecimento RAG

**Status:** [x] concluído

### Intent
Definir a arquitetura, as fontes de conteúdo e a estratégia de chunking/indexação da base de conhecimento que alimentará o RAG do agente.

### Expected Outcomes
- Lista de fontes de conteúdo recomendadas por categoria.
- Estratégia de chunking e metadados sugeridos.
- Orientação de configuração no watsonx.ai / Watson Discovery.
- Processo sugerido de atualização periódica da base.

### Todo List
1. Listar fontes para a categoria **golpes digitais**:
   - Alertas do Banco Central, Febraban, Safernet, CERT.br, boletins da Polícia Civil.
2. Listar fontes para a categoria **educação financeira**:
   - Materiais do Banco Central (Cidadania Financeira), CVM Educacional, ENEF, Serasa, SPC.
3. Definir estrutura de metadados por documento (categoria, fonte, data, tipo de golpe/tema financeiro).
4. Recomendar estratégia de chunking (tamanho de chunk, overlap, preservação de contexto).
5. Descrever configuração no watsonx.ai vector store (embedding model, índice, filtros de metadados).
6. Propor cadência de atualização da base (ex.: mensal ou mediante novo alerta).

### Relevant Context
- Watson Discovery ou watsonx.ai Retrieval Augmented Generation (RAG) pipeline.
- Embedding recomendado para pt-BR: modelos multilíngues (ex.: multilingual-e5, IBM Slate).

---

## Sub-tarefa 6 — Documento Final Consolidado

**Status:** [x] concluído

### Intent
Reunir todos os artefatos produzidos nas sub-tarefas anteriores em um único documento de configuração (`agente-segfinan-config.md`) organizado, pronto para ser usado por um administrador do watsonx Orchestrate.

### Expected Outcomes
- Arquivo `agente-segfinan-config.md` com todas as seções.
- Índice claro para navegação.
- Checklist de configuração passo a passo no Orchestrate.

### Todo List
1. Criar o arquivo `agente-segfinan-config.md`.
2. Inserir seções na ordem: Identidade → System Prompt → Guidelines & Guardrails → Skills → RAG.
3. Adicionar checklist de configuração no Orchestrate (passo a passo).
4. Revisar coesão e consistência entre todas as seções.
5. Garantir que todos os blocos de texto prontos para colar (system prompt, descrições de skill) estejam claramente delimitados.
