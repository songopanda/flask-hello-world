import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Permite que tu web alojada en Tiiny Host lea los datos de Render sin bloqueos
CORS(app)

# Lee la clave de API que pusiste en la sección "Environment Variables" de Render
ODDS_API_KEY = os.environ.get("ODDS_API_KEY", "")

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "CASI PARLAY Data Engine",
        "version": "2026.1"
    })

@app.route('/api/partidos-del-dia', methods=['GET'])
def obtener_partidos():
    if not ODDS_API_KEY:
        return jsonify({"error": "No se ha detectado la ODDS_API_KEY en las variables de Render"}), 400

    # Consulta las cuotas reales de Winamax y Bet365 para la Champions League / Ligas Europeas
    url_odds = f'https://api.the-odds-api.com/v4/sports/soccer_uefa_champs_league/odds/?apiKey={ODDS_API_KEY}&regions=eu&markets=h2h,totals&bookmakers=winamax,bet365'
    
    try:
        response = requests.get(url_odds, timeout=10)
        datos = response.json()
        
        return jsonify({
            "estado": "exito",
            "total_eventos": len(datos),
            "eventos": datos
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render asigna dinámicamente el puerto
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
