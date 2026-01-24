import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_deni_latest_game():
    """
    מושך את המשחק האחרון של דני אבדיה עם כל הנתונים
    """
    url = "https://www.basketball-reference.com/players/a/avdijde01/gamelog/2026"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        print("🏀 מושך נתונים מ-Basketball Reference...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # מצא את הטבלה
        table = soup.find('table', {'id': 'player_game_log_reg'})
        
        if not table:
            print("❌ לא מצאתי את הטבלה")
            return None
        
        print("✅ מצאתי את הטבלה!")
        
        # המר את כל הטבלה ל-DataFrame
        df = pd.read_html(str(table))[0]
        
        # נקה שורות ריקות ושורות של כותרות
        df = df[df['Rk'].notna()]
        df = df[df['Rk'] != 'Rk']
        
        print(f"📊 סה\"כ {len(df)} משחקים בעונה")
        
        # קח את המשחק האחרון (השורה האחרונה)
        latest_game = df.iloc[-1]
        
        # בדוק אם דני שיחק (יש דקות משחק)
        if pd.isna(latest_game['MP']) or latest_game['MP'] == '':
            print("⚠️  דני לא שיחק במשחק האחרון")
            return None
        
        # הדפס את הנתונים החשובים
        print("\n" + "="*70)
        print("📊 המשחק האחרון של דני אבדיה:")
        print("="*70)
        print(f"📅 תאריך: {latest_game.get('Date', 'N/A')}")
        print(f"🏀 יריב: {latest_game.get('Opp', 'N/A')}")
        print(f"🏆 תוצאה: {latest_game.get('Unnamed: 5', 'N/A')} ({latest_game.get('Unnamed: 6', 'N/A')})")
        print(f"⏱️  דקות: {latest_game.get('MP', '0')}")
        print(f"🎯 נקודות: {latest_game.get('PTS', '0')}")
        print(f"📦 ריבאונדים: {latest_game.get('TRB', '0')}")
        print(f"🤝 אסיסטים: {latest_game.get('AST', '0')}")
        print(f"🛡️  גניבות: {latest_game.get('STL', '0')}")
        print(f"🚫 חסימות: {latest_game.get('BLK', '0')}")
        print(f"📈 FG: {latest_game.get('FG', '0')}/{latest_game.get('FGA', '0')}")
        print(f"🎯 3P: {latest_game.get('3P', '0')}/{latest_game.get('3PA', '0')}")
        print(f"🎪 FT: {latest_game.get('FT', '0')}/{latest_game.get('FTA', '0')}")
        print("="*70)
        
        # החזר את כל השורה כ-dictionary
        game_dict = latest_game.to_dict()
        
        print("\n✅ הצלחה! כל הנתונים נמשכו")
        print(f"\n📋 עמודות זמינות: {list(game_dict.keys())}")
        
        return game_dict
        
    except requests.exceptions.RequestException as e:
        print(f"❌ שגיאת רשת: {e}")
        return None
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # הרץ את הפונקציה
    game_data = get_deni_latest_game()
    
    if game_data:
        print("\n" + "="*70)
        print("🎉 כל הנתונים (JSON):")
        print("="*70)
        for key, value in game_data.items():
            print(f"{key}: {value}")