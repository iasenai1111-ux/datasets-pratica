# BD.xlsx: vendas de uma rede de lojas

Base **fictícia** em modelo estrela, para praticar modelagem e DAX no Power BI.

| Aba | Tipo | Linhas | Conteúdo |
|---|---|---:|---|
| `fVendas` | Fato | 3.000 | Vendas de 2019 e 2020, com data e hora da venda e da entrega |
| `Metas` | Fato | 4 lojas × 24 meses | Metas mensais em formato largo (precisa de *unpivot*) |
| `dFuncionario` | Dimensão | 12 | Vendedores, com dados de RH |
| `dLoja` | Dimensão | 4 | Lojas e cidades |
| `dProdutos` | Dimensão | 20 | Produtos e categorias |

## O que dá para praticar

- **Power Query:** promover cabeçalhos, separar data e hora, transformar a aba `Metas` de colunas em linhas
- **Modelagem:** relacionamentos fato-dimensão e tabela calendário
- **DAX básico:** `SUMX`, `AVERAGEX`, `COUNTROWS`, `DISTINCTCOUNT`, `DIVIDE`
- **DAX intermediário:** `CALCULATE`, `FILTER`, `ALL`, `ALLEXCEPT`, `USERELATIONSHIP`
- **Inteligência de tempo:** `DATESYTD`, `SAMEPERIODLASTYEAR`

## Números para conferir

| Indicador | Valor |
|---|---:|
| Faturamento total | R$ 4.656.688,50 |
| Lucro | R$ 2.000.953,50 |
| Pedidos | 3.000 |
| Ticket médio | R$ 1.552,23 |
| Faturamento 2019 | R$ 2.166.630 |
| Faturamento 2020 | R$ 2.490.058 |

Se a sua medida de faturamento (`valor_unitario × quantidade`) der outro valor, revise o cálculo ou os relacionamentos.

## Origem

Gerada pelo script [`gerar_bd.py`](gerar_bd.py), com semente fixa. Nomes, produtos, preços e valores são inventados.
