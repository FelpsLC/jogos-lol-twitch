from flask import Flask
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Liga -> slug
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
        
        # Pega a API KEY da variável de ambiente
        api_key = os.getenv("RIOT_API_KEY")
        if not api_key:
            return "⚠️ API Key da Riot não encontrada."

        headers = {
            "x-api-key": api_key
        }

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"⚠️ Erro na API da Riot ({response.status_code})"
        
        data = response.json()

        # Ajuste do fuso horário (UTC-3)
        hoje = (datetime.utcnow() - timedelta(hours=3)).date().isoformat()
        resposta = []

        for event in data.get("data", {}).get("schedule", {}).get("events", []):
            if not event.get("startTime", "").startswith(hoje):
                continue

            liga_slug = event.get("league", {}).get("slug")
            if liga_slug not in LIGAS.values():
                continue

            # Evita erro caso times não estejam disponíveis
            teams = event.get("match", {}).get("teams", [])
            if len(teams) < 2:
                continue

            t1 = teams[0].get("name", "Time1")
            t2 = teams[1].get("name", "Time2")

            try:
                hora = datetime.fromisoformat(event["startTime"].replace("Z", "")) - timedelta(hours=3)
                hora_str = hora.strftime("%H:%M")
            except:
                hora_str = "??:??"

            nome_liga = [k for k, v in LIGAS.items() if v == liga_slug][0]
            resposta.append(f"{nome_liga}: {t1} vs {t2} – {hora_str}")

        if not resposta:
            return "❌ Nenhum jogo de LoL hoje."

        return "🎮 LoL hoje: " + " | ".join(resposta)

    except Exception as e:
        # Retorna erro real para ajudar no debug
        return f"⚠️ Erro ao buscar jogos de LoL: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

