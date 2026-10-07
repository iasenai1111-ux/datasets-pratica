# Datasets de prática

Conjuntos de dados **fictícios** para treinar Python, Power BI e IA. Use à vontade em exercícios e em projetos de portfólio.

| Arquivo | Linhas | Para praticar |
|---|---|---|
| [`dados/vendas.csv`](dados/vendas.csv) | 2.000 | Primeiros dashboards, medidas DAX, agrupamentos no pandas |
| [`dados/vendas_sujo.csv`](dados/vendas_sujo.csv) | 525 | Limpeza de dados no Power Query ou no pandas |
| [`dados/campanhas_marketing.csv`](dados/campanhas_marketing.csv) | 2.190 | Métricas de marketing: CTR, CPC, CPA e ROAS |
| [`dados/comentarios.csv`](dados/comentarios.csv) | 300 | Classificação de texto e análise de sentimento |
| [`bd-vendas-lojas/BD.xlsx`](bd-vendas-lojas) | 3.000 vendas | Modelo estrela completo para modelagem e DAX no Power BI |

## Desafio: limpe o `vendas_sujo.csv`

O arquivo é uma amostra do `vendas.csv` com problemas colocados de propósito, do tipo que aparece em planilha de empresa. Seu objetivo é deixá-lo pronto para análise.

O que você vai encontrar:

- Separador `;` e vírgula como separador decimal
- Datas em três formatos diferentes
- Texto com maiúsculas, minúsculas e espaços sobrando
- A mesma região escrita de dois jeitos (`Sudeste` e `SE`)
- Preço como texto, com `R$`
- Número escrito por extenso na coluna de quantidade
- Valores vazios e linhas duplicadas

**Como conferir:** depois de limpo, cada `id_pedido` deve aparecer uma única vez (500 pedidos) e bater com a linha correspondente do `vendas.csv`.

## Como usar

**Power BI:** Obter dados → Web → cole o link *Raw* do arquivo.

**Python:**

```python
import pandas as pd

url = "https://raw.githubusercontent.com/iasenai1111-ux/datasets-pratica/main/dados/vendas.csv"
vendas = pd.read_csv(url, parse_dates=["data"])
```

## Como os dados foram gerados

Tudo sai do script [`scripts/gerar_dados.py`](scripts/gerar_dados.py), com semente fixa. Rodar de novo produz exatamente os mesmos arquivos. Nomes, valores e comentários são inventados e não representam pessoas ou empresas reais.
