from flask import Flask
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ API LoL online!"

@app.route("/jogoslol")
def jogos_lol():
    url = "https://lolesports.com/api/schedule"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()

        hoje = (datetime.utcnow() - timedelta(hours=3)).date().isoformat()
        jogos = []

        for e in data.get("data", {}).get("schedule", {}).get("events", []):
            if not e.get("startTime", "").startswith(hoje):
                continue

            league = e["league"]["name"]
            teams = e["match"]["teams"]

            if len(teams) < 2:
                continue

            t1 = teams[0]["name"]
            t2 = teams[1]["name"]

            hora = datetime.fromisoformat(e["startTime"].replace("Z", "")) - timedelta(hours=3)
            jogos.append(f"{league}: {t1} vs {t2} ({hora:%H:%M})")

        if not jogos:
            return "❌ Nenhum jogo de LoL hoje"

        return " | ".join(jogos)

    except Exception as e:
        return "❌ Erro ao buscar jogos"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

