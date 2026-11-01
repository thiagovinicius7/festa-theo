#!/usr/bin/env python3
"""
Resumo diário das confirmações da festa do Avatar Theo.

Uso:
  python3 relatorio/resumo.py --senha SENHA_DO_RELATORIO [--saida pasta]
  python3 relatorio/resumo.py --demo            (dados de exemplo, sem Firebase)

Gera, na pasta de saída:
  resumo.png   infográfico (1080 px de largura) com a arte do convite
  email.html   corpo do e-mail em HTML (mesma arte, sem imagens)
  resumo.json  totais, para o texto do e-mail
"""
import argparse, base64, datetime as dt, html, json, os, sys, urllib.request
from zoneinfo import ZoneInfo

PROJETO = "festa-theo-3f43d"
API_KEY = "AIzaSyAgr7MKgTeja8hCbkhPbVy70WB6fYDqb1Y"
EMAIL_RELATORIO = "relatorio@festa-theo-3f43d.firebaseapp.com"
BASE = f"https://firestore.googleapis.com/v1/projects/{PROJETO}/databases/(default)/documents"
TZ = ZoneInfo("America/Sao_Paulo")
AQUI = os.path.dirname(os.path.abspath(__file__))


def req(url, dados=None, token=None):
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = "Bearer " + token
    r = urllib.request.Request(url, data=json.dumps(dados).encode() if dados is not None else None, headers=h)
    with urllib.request.urlopen(r, timeout=30) as resp:
        return json.load(resp)


def valor(v):
    for k in ("stringValue", "booleanValue", "timestampValue"):
        if k in v:
            return v[k]
    if "integerValue" in v:
        return int(v["integerValue"])
    if "mapValue" in v:
        return {k: valor(x) for k, x in v["mapValue"].get("fields", {}).items()}
    return None


def doc(d):
    return {k: valor(v) for k, v in d.get("fields", {}).items()}


def busca(senha):
    tok = req(f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}",
              {"email": EMAIL_RELATORIO, "password": senha, "returnSecureToken": True})["idToken"]
    respostas, pagina = [], None
    while True:
        url = f"{BASE}/festaTheo8?pageSize=300" + (f"&pageToken={pagina}" if pagina else "")
        r = req(url, token=tok)
        respostas += [doc(d) for d in r.get("documents", [])]
        pagina = r.get("nextPageToken")
        if not pagina:
            break
    # capa e textos são públicos
    capa, textos = None, {}
    try:
        c = doc(req(f"{BASE}/festaTheo8Config/capa"))
        if c.get("partes"):
            capa = "".join(doc(req(f"{BASE}/festaTheo8Config/capa-{i}")).get("img", "") for i in range(1, c["partes"] + 1))
        else:
            capa = c.get("img")
    except Exception:
        pass
    try:
        textos = doc(req(f"{BASE}/festaTheo8Config/textos")).get("textos", {}) or {}
    except Exception:
        pass
    return respostas, capa, textos


def demo():
    agora = dt.datetime.now(dt.timezone.utc)
    r = [
        {"nome": "Marilu Leote", "vai": True, "criancas": 0, "adolescentes": 0, "adultos": 2, "total": 2, "recado": "Amo você.", "quando": (agora - dt.timedelta(days=3)).isoformat()},
        {"nome": "Família Souza", "vai": True, "criancas": 2, "adolescentes": 1, "adultos": 2, "total": 5, "recado": "", "quando": (agora - dt.timedelta(hours=5)).isoformat()},
        {"nome": "Tio Carlos", "vai": False, "criancas": 0, "adolescentes": 0, "adultos": 0, "total": 0, "recado": "", "quando": (agora - dt.timedelta(hours=2)).isoformat()},
    ]
    capa, textos = None, {}
    try:  # capa e textos reais (públicos), só os números são de exemplo
        c = doc(req(f"{BASE}/festaTheo8Config/capa"))
        capa = "".join(doc(req(f"{BASE}/festaTheo8Config/capa-{i}")).get("img", "") for i in range(1, c.get("partes", 0) + 1)) or c.get("img")
        textos = doc(req(f"{BASE}/festaTheo8Config/textos")).get("textos", {}) or {}
    except Exception:
        pass
    return r, capa, textos


def fonte(nome):
    with open(os.path.join(AQUI, "fonts", nome), "rb") as f:
        return "data:font/ttf;base64," + base64.b64encode(f.read()).decode()


def monta_html(respostas, capa, textos):
    agora = dt.datetime.now(TZ)
    festa_txt = textos.get("dataHora") or "2026-11-30T16:00"
    festa = dt.datetime.fromisoformat(festa_txt).replace(tzinfo=TZ)
    dias = max(0, (festa.date() - agora.date()).days)
    vao = [r for r in respostas if r.get("vai")]
    nao = [r for r in respostas if not r.get("vai")]
    soma = lambda k: sum(int(r.get(k) or 0) for r in vao)
    t = {"adultos": soma("adultos"), "adolescentes": soma("adolescentes"), "criancas": soma("criancas"), "total": soma("total"),
         "respostas_vao": len(vao), "respostas_nao": len(nao), "dias": dias}

    def quando(r):
        try:
            return dt.datetime.fromisoformat(r["quando"].replace("Z", "+00:00"))
        except Exception:
            return dt.datetime(2000, 1, 1, tzinfo=dt.timezone.utc)
    limite = agora - dt.timedelta(hours=24)
    novos = sorted([r for r in respostas if quando(r) >= limite], key=quando, reverse=True)
    t["novos"] = [{"nome": r["nome"], "vai": r.get("vai"), "total": r.get("total", 0)} for r in novos]

    nome_festa = f'{textos.get("av", "AVATAR")} {textos.get("nm", "Theo")}'
    hora = textos.get("infoHora", "16h")
    local = textos.get("infoLocal", "Sítio Geranium")
    capa_html = f'<div class="capa"><img src="{capa}"></div>' if capa and capa.startswith("data:image/") else ""
    if novos:
        linhas = "".join(
            f'<li><span>{html.escape(r["nome"])}</span><b>{"+" + str(r.get("total", 0)) if r.get("vai") else "não vai"}</b></li>'
            for r in novos[:8])
        extra = f'<li class="mais">e mais {len(novos) - 8}…</li>' if len(novos) > 8 else ""
        novos_html = f'<div class="bloco"><h3>Novas respostas nas últimas 24h</h3><ul>{linhas}{extra}</ul></div>'
    else:
        novos_html = '<div class="bloco"><h3>Novas respostas nas últimas 24h</h3><p class="vazio">Nenhuma nova resposta hoje.</p></div>'
    falta = "É hoje! 🎉" if dias == 0 else ("Falta 1 dia" if dias == 1 else f"Faltam {dias} dias")

    pagina = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Cinzel;src:url({fonte("Cinzel.ttf")})}}
@font-face{{font-family:Kaushan;src:url({fonte("KaushanScript.ttf")})}}
@font-face{{font-family:Nunito;src:url({fonte("Nunito.ttf")})}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;font-family:Nunito;color:#3a2414;background:linear-gradient(180deg,#d7ebf5 0%,#f1e3c2 30%,#f0c98a 75%,#d9a06a 100%)}}
.wrap{{padding:56px 60px 60px;position:relative}}
.lant{{position:absolute;top:0;width:70px}}.lant.e{{left:40px}}.lant.d{{right:40px}}
.faixa{{display:table;margin:0 auto;font-family:Cinzel;font-weight:700;letter-spacing:.2em;font-size:22px;color:#fff8e8;background:#b3322a;
  padding:10px 34px;clip-path:polygon(6% 0,94% 0,100% 50%,94% 100%,6% 100%,0 50%)}}
.av{{text-align:center;font-family:Cinzel;font-weight:900;letter-spacing:.3em;font-size:40px;color:#7e1f19;margin-top:26px}}
.nm{{text-align:center;font-family:Kaushan;font-size:150px;line-height:.95;color:#b3322a;text-shadow:5px 5px 0 #f3d58a}}
.sub{{text-align:center;font-weight:800;font-size:28px;margin-top:6px}}
.capa{{width:300px;margin:28px auto 0;border:5px solid #d9a441;border-radius:10px;overflow:hidden;box-shadow:0 0 0 8px #fff8e8,0 0 0 11px #b3322a}}
.capa img{{width:100%;display:block}}
.perg{{background:#fff8e8;border:3px solid #e2c690;border-radius:8px;margin:44px 10px 0;padding:34px 34px 30px;position:relative;box-shadow:0 18px 34px #3a24142a}}
.perg:before,.perg:after{{content:"";position:absolute;left:-16px;right:-16px;height:22px;border-radius:12px;background:linear-gradient(180deg,#a8382e,#7e1f19)}}
.perg:before{{top:-16px}}.perg:after{{bottom:-16px}}
.total{{text-align:center}}
.total b{{display:block;font-family:Cinzel;font-weight:900;font-size:150px;line-height:1;color:#b3322a}}
.total span{{font-family:Cinzel;font-weight:700;font-size:30px;letter-spacing:.08em;color:#7e1f19}}
.grupos{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:30px}}
.g{{border-radius:18px;padding:22px 10px;text-align:center;color:#fff;box-shadow:0 6px 0 rgba(0,0,0,.18)}}
.g b{{display:block;font-family:Cinzel;font-weight:900;font-size:76px;line-height:1}}
.g span{{font-weight:800;font-size:24px}}
.g small{{display:block;font-size:17px;opacity:.9;margin-top:2px}}
.fogo{{background:#e2552b}}.terra{{background:#5f8a3a}}.agua{{background:#2f7fc1}}
.linha{{display:flex;justify-content:space-around;margin-top:28px;font-size:24px;font-weight:800;color:#6e5238}}
.linha b{{color:#3a2414;font-size:30px}}
.bloco{{margin-top:30px;border-top:2px dashed #e2c690;padding-top:22px}}
.bloco h3{{font-family:Cinzel;font-size:26px;color:#7e1f19;margin-bottom:12px}}
.bloco ul{{list-style:none}}
.bloco li{{display:flex;justify-content:space-between;font-size:24px;padding:8px 0;border-bottom:1px solid #f0e2c2}}
.bloco li b{{color:#b3322a}}.bloco .mais{{color:#6e5238;font-style:italic}}
.vazio{{font-size:22px;color:#6e5238}}
.rod{{text-align:center;margin-top:40px;font-weight:800;font-size:24px;color:#fff8e8;text-shadow:0 2px 4px #0006}}
.data{{text-align:center;font-size:20px;color:#fff8e8;margin-top:6px;text-shadow:0 1px 3px #0006}}
</style></head><body><div class="wrap">
<svg class="lant e" viewBox="0 0 46 110"><line x1="23" y1="0" x2="23" y2="30" stroke="#5d3324" stroke-width="2"/><rect x="15" y="28" width="16" height="6" rx="2" fill="#5d3324"/><ellipse cx="23" cy="56" rx="21" ry="24" fill="#c63d33"/><ellipse cx="23" cy="56" rx="12" ry="16" fill="#ffcf7a" opacity=".85"/><rect x="15" y="78" width="16" height="6" rx="2" fill="#5d3324"/><path d="M18 84 v18 M23 84 v22 M28 84 v18" stroke="#d9a441" stroke-width="2"/></svg>
<svg class="lant d" viewBox="0 0 46 110"><line x1="23" y1="0" x2="23" y2="30" stroke="#5d3324" stroke-width="2"/><rect x="15" y="28" width="16" height="6" rx="2" fill="#5d3324"/><ellipse cx="23" cy="56" rx="21" ry="24" fill="#c63d33"/><ellipse cx="23" cy="56" rx="12" ry="16" fill="#ffcf7a" opacity=".85"/><rect x="15" y="78" width="16" height="6" rx="2" fill="#5d3324"/><path d="M18 84 v18 M23 84 v22 M28 84 v18" stroke="#d9a441" stroke-width="2"/></svg>
<div class="faixa">RESUMO DAS CONFIRMAÇÕES</div>
<div class="av">{html.escape(textos.get("av", "AVATAR"))}</div>
<div class="nm">{html.escape(textos.get("nm", "Theo"))}</div>
<div class="sub">{html.escape(textos.get("infoData", "30/11"))} · {html.escape(hora)} · {html.escape(local)} — {falta}</div>
{capa_html}
<div class="perg">
  <div class="total"><b>{t["total"]}</b><span>PESSOAS CONFIRMADAS</span></div>
  <div class="grupos">
    <div class="g fogo"><b>{t["adultos"]}</b><span>Adultos</span><small>18 anos ou mais</small></div>
    <div class="g terra"><b>{t["adolescentes"]}</b><span>Adolescentes</span><small>10 a 17 anos</small></div>
    <div class="g agua"><b>{t["criancas"]}</b><span>Crianças</span><small>menores de 10</small></div>
  </div>
  <div class="linha"><span>Respostas "vou": <b>{t["respostas_vao"]}</b></span><span>Não vão: <b>{t["respostas_nao"]}</b></span></div>
  {novos_html}
</div>
<div class="rod">{html.escape(nome_festa)} · {html.escape(textos.get("seloNum", "8"))} {html.escape(textos.get("seloTxt", "ANOS").lower())}</div>
<div class="data">Atualizado em {agora.strftime("%d/%m/%Y às %H:%M")}</div>
</div></body></html>"""
    return pagina, t


def monta_email(t, textos):
    """HTML de e-mail (tabelas + estilos inline) com a arte do convite."""
    e = html.escape
    nome = f'{textos.get("av", "AVATAR")} {textos.get("nm", "Theo")}'
    dias = t["dias"]
    falta = "É hoje! 🎉" if dias == 0 else ("Falta 1 dia" if dias == 1 else f"Faltam {dias} dias")
    info = f'{textos.get("infoData", "30/11")} · {textos.get("infoHora", "16h")} · {textos.get("infoLocal", "Sítio Geranium")}'
    def caixa(n, rot, sub, cor):
        return (f'<td width="33%" style="padding:6px"><div style="background:{cor};border-radius:14px;padding:14px 6px;text-align:center;color:#fff">'
                f'<div style="font:900 40px Georgia,serif;line-height:1">{n}</div>'
                f'<div style="font:800 15px Arial,sans-serif;margin-top:4px">{rot}</div>'
                f'<div style="font:12px Arial,sans-serif;opacity:.9">{sub}</div></div></td>')
    if t["novos"]:
        linhas = "".join(
            f'<tr><td style="padding:7px 0;border-bottom:1px solid #f0e2c2;font:15px Arial,sans-serif;color:#3a2414">{e(n["nome"])}</td>'
            f'<td style="padding:7px 0;border-bottom:1px solid #f0e2c2;font:bold 15px Arial,sans-serif;color:#b3322a;text-align:right">'
            f'{"+" + str(n["total"]) if n["vai"] else "não vai"}</td></tr>' for n in t["novos"][:10])
        novos = f'<table width="100%" cellpadding="0" cellspacing="0">{linhas}</table>'
    else:
        novos = '<p style="font:15px Arial,sans-serif;color:#6e5238;margin:0">Nenhuma nova resposta hoje.</p>'
    agora = dt.datetime.now(TZ).strftime("%d/%m/%Y às %H:%M")
    return f"""<div style="background:#f1e3c2;padding:24px 10px">
<table align="center" width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;background:linear-gradient(180deg,#d7ebf5,#f1e3c2 35%,#f0c98a);border-radius:12px">
<tr><td style="padding:26px 22px 8px;text-align:center">
<div style="display:inline-block;background:#b3322a;color:#fff8e8;font:bold 12px Georgia,serif;letter-spacing:3px;padding:7px 18px">RESUMO DAS CONFIRMAÇÕES</div>
<div style="font:900 22px Georgia,serif;letter-spacing:6px;color:#7e1f19;margin-top:14px">{e(textos.get("av", "AVATAR"))}</div>
<div style="font:italic bold 60px Georgia,serif;line-height:1;color:#b3322a;text-shadow:3px 3px 0 #f3d58a">{e(textos.get("nm", "Theo"))}</div>
<div style="font:bold 14px Arial,sans-serif;color:#3a2414;margin-top:8px">{e(info)} — {falta}</div>
</td></tr>
<tr><td style="padding:14px 16px 20px">
<div style="background:#fff8e8;border:2px solid #e2c690;border-top:10px solid #8e2a21;border-bottom:10px solid #8e2a21;border-radius:6px;padding:20px 14px">
<div style="text-align:center"><div style="font:900 76px Georgia,serif;line-height:1;color:#b3322a">{t["total"]}</div>
<div style="font:bold 15px Georgia,serif;letter-spacing:2px;color:#7e1f19">PESSOAS CONFIRMADAS</div></div>
<table width="100%" cellpadding="0" cellspacing="0" style="margin-top:14px"><tr>
{caixa(t["adultos"], "Adultos", "18 anos ou mais", "#e2552b")}
{caixa(t["adolescentes"], "Adolescentes", "10 a 17 anos", "#5f8a3a")}
{caixa(t["criancas"], "Crianças", "menores de 10", "#2f7fc1")}
</tr></table>
<p style="text-align:center;font:bold 15px Arial,sans-serif;color:#6e5238;margin:14px 0 0">Respostas "vou": <b style="color:#3a2414">{t["respostas_vao"]}</b> &nbsp;·&nbsp; Não vão: <b style="color:#3a2414">{t["respostas_nao"]}</b></p>
<div style="border-top:2px dashed #e2c690;margin-top:16px;padding-top:12px">
<div style="font:bold 15px Georgia,serif;color:#7e1f19;margin-bottom:6px">Novas respostas nas últimas 24h</div>{novos}</div>
</div>
<p style="text-align:center;margin:16px 0 0"><a href="https://thiagovinicius7.github.io/festa-theo/painel.html" style="display:inline-block;background:#b3322a;color:#fff8e8;text-decoration:none;font:bold 14px Arial,sans-serif;padding:11px 20px;border-radius:10px">Abrir o painel completo</a></p>
<p style="text-align:center;font:12px Arial,sans-serif;color:#6e5238;margin:12px 0 0">{e(nome)} · atualizado em {agora}</p>
</td></tr></table></div>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--senha")
    ap.add_argument("--saida", default=".")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        respostas, capa, textos = demo()
    else:
        if not a.senha:
            sys.exit("Informe --senha")
        respostas, capa, textos = busca(a.senha)
    pagina, totais = monta_html(respostas, capa, textos)
    os.makedirs(a.saida, exist_ok=True)
    caminho_html = os.path.join(a.saida, "resumo.html")
    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(pagina)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 800}, device_scale_factor=1)
        pg.goto("file://" + os.path.abspath(caminho_html))
        pg.wait_for_timeout(800)
        pg.screenshot(path=os.path.join(a.saida, "resumo.png"), full_page=True)
        b.close()
    with open(os.path.join(a.saida, "email.html"), "w", encoding="utf-8") as f:
        f.write(monta_email(totais, textos))
    with open(os.path.join(a.saida, "resumo.json"), "w", encoding="utf-8") as f:
        json.dump(totais, f, ensure_ascii=False, indent=2)
    print(json.dumps(totais, ensure_ascii=False))


if __name__ == "__main__":
    main()
