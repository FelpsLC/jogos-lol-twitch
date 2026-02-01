from flask import Flask
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ API LoL online!"

@app.route("/teste")
def teste():
    if os.getenv("RIOT_API_KEY"):
        return "✅ API Key encontrada"
    return "❌ API Key NÃO encontrada"

@app.route("/jogoslol")
def jogos_lol():
    url = "https://esports-api.lolesports.com/persisted/gw/getSchedule?hl=pt-BR"

    api_key = os.getenv("RIOT_API_KEY")
    if not api_key:
        return "❌ API Key não encontrada"

    headers = {
        "x-api-key": api_key,
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Origin": "https://lolesports.com"
    }

    r = requests.get(url, headers=headers, timeout=10)

    if r.status_code != 200:
        return f"❌ Erro Riot {r.status_code}"

    data = r.json()

    hoje = (datetime.utcnow() - timedelta(hours=3)).date().isoformat()
    jogos = []

    for e in data["data"]["schedule"]["events"]:
        if not e["startTime"].startswith(hoje):
            continue

        liga = e["league"]["slug"]
        if liga not in ["lck", "lpl", "lec", "lcs", "cblol"]:
            continue

        t = e["match"]["teams"]
        if len(t) < 2:
            continue

        hora = datetime.fromisoformat(e["startTime"].replace("Z", "")) - timedelta(hours=3)
        jogos.append(f"{liga.upper()}: {t[0]['name']} vs {t[1]['name']} ({hora:%H:%M})")

    if not jogos:
        return "❌ Nenhum jogo hoje"

    return " | ".join(jogos)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
