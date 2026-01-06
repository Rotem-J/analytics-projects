from flask import Flask, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

# Player ID של דני אבדיה
DENI_PLAYER_ID = "1630166"

def get_latest_game():
    """
    מושך את המשחק האחרון של דני אבדיה מ-NBA.com
    """
    url = "https://stats.nba.com/stats/playergamelog"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': 'https://www.nba.com/',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true'
    }
    
    params = {
        'PlayerID': DENI_PLAYER_ID,
        'Season': '2025-26',
        'SeasonType': 'Regular Season'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        games = data['resultSets'][0]['rowSet']
        
        if not games:
            return {
                'success': False,
                'error': 'No games found'
            }
        
        # המשחק האחרון הוא הראשון ברשימה
        latest_game = games[0]
        
        # בניית אובייקט עם הסטטיסטיקות
        game_stats = {
            'success': True,
            'player': 'Deni Avdija',
            'game_id': latest_game[1],
            'game_date': latest_game[2],
            'matchup': latest_game[4],
            'result': 'W' if latest_game[5] == 'W' else 'L',
            'minutes': latest_game[6],
            'points': latest_game[24],
            'rebounds': latest_game[18],
            'assists': latest_game[19],
            'steals': latest_game[20],
            'blocks': latest_game[21],
            'fg_pct': latest_game[9],
            'fg3_pct': latest_game[12],
            'ft_pct': latest_game[15],
            'plus_minus': latest_game[25]
        }
        
        return game_stats
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/')
def home():
    """
    דף הבית - מראה שה-API פעיל
    """
    return jsonify({
        'status': 'active',
        'message': 'Deni Avdija Stats API',
        'endpoints': {
            '/latest': 'Get latest game stats',
            '/health': 'Health check'
        }
    })

@app.route('/latest', methods=['GET'])
def latest_game():
    """
    מחזיר את המשחק האחרון של דני
    """
    result = get_latest_game()
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health():
    """
    בדיקת תקינות
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Render ידרוש את זה
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)