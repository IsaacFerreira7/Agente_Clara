from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import BaseModel
from typing import List


class WebSearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    source_domain: str


class WebSearchResponse(BaseModel):
    query: str
    results: List[WebSearchResult]
    total_returned: int


TRUSTED_DOMAINS = [
    "bcb.gov.br",
    "febraban.org.br",
    "safernet.org.br",
    "cert.br",
    "cvm.gov.br",
    "procon.sp.gov.br",
    "serpro.gov.br",
    "gov.br",
    "serasa.com.br",
    "consumidor.gov.br",
]


@tool(permission=ToolPermission.READ_ONLY)
def busca_web(query: str, max_results: int = 5) -> WebSearchResponse:
    """Realiza busca na web para encontrar alertas recentes de golpes digitais e informações de órgãos regulatórios brasileiros.

    Use esta ferramenta quando: (1) a base de conhecimento não retornar resultados relevantes; (2) o usuário mencionar um golpe muito recente ou viral; (3) o usuário pedir informações sobre alertas ou mudanças regulatórias atuais. Priorize domínios oficiais como bcb.gov.br, febraban.org.br, safernet.org.br, cert.br e cvm.gov.br.

    Args:
        query (str): Consulta de busca otimizada com termos-chave do conteúdo do usuário. Ex.: 'golpe WhatsApp número novo alerta 2024'.
        max_results (int): Número máximo de resultados a retornar. Padrão 5.
    Returns:
        WebSearchResponse: Resultados da busca com título, URL, trecho e domínio de cada resultado encontrado.
    """
    mock_results = [
        WebSearchResult(
            title=f"Alerta oficial: {query}",
            url=f"https://febraban.org.br/alerta",
            snippet=(
                f"Informações oficiais sobre: {query}. "
                "Consulte sempre fontes confiáveis como Banco Central, "
                "Febraban e Safernet antes de tomar qualquer decisão."
            ),
            source_domain="febraban.org.br",
        )
    ]

    return WebSearchResponse(
        query=query,
        results=mock_results,
        total_returned=len(mock_results),
    )
