from flask import Flask
import requests
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ API LoL online!"

@app.route("/jogoslol")
def jogos_lol():
    url = "https://api.pandascore.co/lol/matches/upcoming"

    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return "❌ Erro ao buscar jogos"

        data = r.json()
        hoje = datetime.utcnow().date().isoformat()
        jogos = []

        for jogo in data:
            if not jogo.get("begin_at"):
                continue

            if not jogo["begin_at"].startswith(hoje):
                continue

            times = jogo.get("opponents", [])
            if len(times) < 2:
                continue

            t1 = times[0]["opponent"]["name"]
            t2 = times[1]["opponent"]["name"]

            hora = jogo["begin_at"][11:16]
            liga = jogo["league"]["name"]

            jogos.append(f"{liga}: {t1} vs {t2} ({hora})")

        if not jogos:
            return "❌ Nenhum jogo de LoL hoje"

        return " | ".join(jogos)

    except Exception:
        return "❌ Erro inesperado"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.r
