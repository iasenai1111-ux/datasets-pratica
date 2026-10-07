"""Gera os datasets de prática. Todos os dados são fictícios.
Uso: python scripts/gerar_dados.py  (a semente fixa garante o mesmo resultado)"""
import numpy as np, pandas as pd
from pathlib import Path

rng = np.random.default_rng(42)
OUT = Path(__file__).resolve().parent.parent / "dados"
OUT.mkdir(exist_ok=True)

# ---------- 1. vendas.csv (limpo) ----------
produtos = {
    "Notebook 14": ("Informática", 3200), "Mouse sem fio": ("Informática", 85),
    "Teclado mecânico": ("Informática", 310), "Monitor 24": ("Informática", 890),
    "Cadeira ergonômica": ("Móveis", 1150), "Mesa de escritório": ("Móveis", 740),
    "Fone bluetooth": ("Áudio", 260), "Caixa de som": ("Áudio", 420),
    "Webcam HD": ("Acessórios", 190), "Suporte para notebook": ("Acessórios", 120),
}
regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
vendedores = ["Ana", "Bruno", "Carla", "Diego", "Elisa", "Fábio", "Gabi", "Hugo"]
n = 2000
datas = pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D")
prod = rng.choice(list(produtos), n)
vendas = pd.DataFrame({
    "id_pedido": np.arange(10001, 10001 + n),
    "data": datas,
    "produto": prod,
    "categoria": [produtos[p][0] for p in prod],
    "regiao": rng.choice(regioes, n, p=[.42, .2, .2, .1, .08]),
    "vendedor": rng.choice(vendedores, n),
    "quantidade": rng.integers(1, 6, n),
    "preco_unitario": [produtos[p][1] for p in prod],
    "desconto_pct": rng.choice([0, 5, 10, 15], n, p=[.55, .2, .15, .1]),
}).sort_values("data").reset_index(drop=True)
vendas["id_pedido"] = np.arange(10001, 10001 + n)
vendas["total"] = (vendas.quantidade * vendas.preco_unitario * (1 - vendas.desconto_pct / 100)).round(2)
vendas.to_csv(OUT / "vendas.csv", index=False, date_format="%Y-%m-%d")

# ---------- 2. vendas_sujo.csv (para Power Query / pandas) ----------
s = vendas.sample(500, random_state=1).copy().astype(object)
fmt = rng.choice(["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%y"], len(s), p=[.6, .25, .15])
s["data"] = [pd.Timestamp(d).strftime(f) for d, f in zip(s["data"], fmt)]
def baguncar(txt):
    r = rng.random()
    if r < .15: return txt.upper()
    if r < .30: return txt.lower()
    if r < .45: return "  " + txt + " "
    return txt
for c in ["produto", "regiao", "vendedor"]:
    s[c] = [baguncar(v) for v in s[c]]
s["regiao"] = [("SE" if v.strip().lower() == "sudeste" and rng.random() < .2 else v) for v in s["regiao"]]
s["preco_unitario"] = ["R$ " + f"{v:.2f}".replace(".", ",") for v in s["preco_unitario"]]
s["total"] = [f"{v:.2f}".replace(".", ",") for v in s["total"]]
s["quantidade"] = [("duas" if (q == 2 and rng.random() < .1) else q) for q in s["quantidade"]]
for c, p in [("vendedor", .05), ("desconto_pct", .08), ("categoria", .04)]:
    m = rng.random(len(s)) < p
    s.loc[m, c] = np.nan
s = pd.concat([s, s.sample(25, random_state=2)]).sample(frac=1, random_state=3)
s.to_csv(OUT / "vendas_sujo.csv", index=False, sep=";")

# ---------- 3. campanhas_marketing.csv ----------
canais = {  # canal: (invest. médio/dia, CPM, CTR, taxa conv., ticket)
    "Google Ads": (900, 38, .045, .050, 210), "Instagram": (700, 22, .014, .022, 180),
    "Facebook": (500, 18, .011, .020, 170), "LinkedIn": (400, 95, .008, .030, 420),
    "TikTok": (350, 12, .016, .010, 130), "E-mail": (80, 6, .030, .045, 190),
}
linhas = []
for d in pd.date_range("2025-01-01", "2025-12-31"):
    saz = 1 + .35 * (d.month in (11, 12)) + .15 * (d.month == 5)
    for canal, (inv, cpm, ctr, cv, ticket) in canais.items():
        invest = inv * saz * rng.normal(1, .15)
        imp = invest / cpm * 1000 * rng.normal(1, .1)
        cli = imp * ctr * rng.normal(1, .12)
        conv = max(0, cli * cv * rng.normal(1, .2))
        linhas.append([d.date(), canal, round(invest, 2), int(imp), int(cli), int(conv),
                       round(int(conv) * ticket * rng.normal(1, .1), 2)])
camp = pd.DataFrame(linhas, columns=["data", "canal", "investimento", "impressoes", "cliques", "conversoes", "receita"])
camp.to_csv(OUT / "campanhas_marketing.csv", index=False)

# ---------- 4. comentarios.csv (rotulado) ----------
temas = {
    "entrega": "a entrega", "atendimento": "o atendimento", "preço": "o preço",
    "qualidade": "a qualidade do produto", "site": "o site",
}
modelos = {
    "positivo": ["Adorei {t}, superou o que eu esperava.", "{T} foi excelente, recomendo.",
                 "Muito bom, {t} me surpreendeu.", "Parabéns, {t} está ótimo.", "Gostei bastante de {t}.",
                 "Nota 10 para {t}!", "{T} resolveu meu problema rapidinho.", "Voltarei a comprar, {t} valeu a pena.",
                 "Não tenho do que reclamar de {t}.", "Achei que ia ser ruim, mas {t} foi show."],
    "negativo": ["Péssimo, {t} me decepcionou.", "{T} foi horrível, não recomendo.",
                 "Que decepção com {t}.", "{T} deixou muito a desejar.", "Nunca mais compro, {t} é ruim demais.",
                 "Tive problema com {t} e ninguém resolveu.", "{T} não é nada bom.", "Esperava mais de {t}.",
                 "Não gostei de {t}.", "Já foi ótimo, hoje {t} está uma bagunça."],
    "neutro":   ["Alguém sabe como funciona {t}?", "{T} mudou este mês?", "Queria mais informações sobre {t}.",
                 "{T} foi normal, nada de mais.", "Ainda estou avaliando {t}.", "Qual o prazo para {t}?",
                 "Vi que {t} foi atualizado.", "{T} é igual ao da outra loja.", "Onde encontro detalhes sobre {t}?",
                 "Recebi hoje, depois comento sobre {t}."],
}
lin = []
for i in range(300):
    sent = rng.choice(list(modelos), p=[.4, .35, .25]); tema = rng.choice(list(temas))
    t = temas[tema]; txt = rng.choice(modelos[sent]).format(t=t, T=t[0].upper() + t[1:])
    txt = txt.replace(" de o ", " do ").replace(" de a ", " da ")
    lin.append([i + 1, txt, sent, tema])
pd.DataFrame(lin, columns=["id", "comentario", "sentimento", "tema"]).to_csv(OUT / "comentarios.csv", index=False)
print("ok", len(vendas), len(s), len(camp), len(lin))
