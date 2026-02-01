from flask import Flask
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

LIGAS = {
    "LCK": "lck",
    "LPL": "lpl",
    "LEC": "lec",
    "CBLOL": "cblol",
    "LCS": "lcs"
}

@app.route("/jogoslol")
def jogos_lol():
    try:
        url = "https://esports-api.lolesports.com/persisted/gw/getSchedule?hl=pt-BR"
        headers = {
            "x-api-key": os.getenv("RIOT_API_KEY")
        }

        data = requests.get(url, headers=headers).json()

        hoje = (datetime.utcnow() - timedelta(hours=3)).date().isoformat()
        resposta = []

        for event in data["data"]["schedule"]["events"]:
            if not event["startTime"].startswith(hoje):
                continue

            liga_slug = event["league"]["slug"]
            if liga_slug not in LIGAS.values():
                continue

            t1 = event["match"]["teams"][0]["name"]
            t2 = event["match"]["teams"][1]["name"]

            hora = datetime.fromisoformat(
                event["startTime"].replace("Z", "")
            ) - timedelta(hours=3)

            nome_liga = [k for k, v in LIGAS.items() if v == liga_slug][0]
            resposta.append(
                f"{nome_liga}: {t1} vs {t2} – {hora.strftime('%H:%M')}"
            )

        if not resposta:
            return "❌ Nenhum jogo de LoL hoje."

        return "🎮 LoL hoje: " + " | ".join(resposta)

    except:
        return "⚠️ Erro ao buscar jogos de LoL."

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
