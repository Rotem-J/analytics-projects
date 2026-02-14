import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np

def get_deni_latest_game():
    """
    מושך את המשחק האחרון של דני אבדיה עם כל הנתונים
    מחזיר DataFrame עם שורה אחת
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
        
        # קח את המשחק האחרון (השורה האחרונה) כ-DataFrame
        latest_game_df = df.iloc[[-1]]  # שים לב ל-[[-1]] כדי לשמור על DataFrame
        
        # בדוק אם דני שיחק (יש דקות משחק)
        mp_value = latest_game_df['MP'].values[0]
        if pd.isna(mp_value) or mp_value == '':
            print("⚠️  דני לא שיחק במשחק האחרון")
            return None
        
        # הדפס את הנתונים החשובים
        game = latest_game_df.iloc[0]
        print("\n" + "="*70)
        print("📊 המשחק האחרון של דני אבדיה:")
        print("="*70)
        print(f"📅 תאריך: {game.get('Date', 'N/A')}")
        print(f"🏀 יריב: {game.get('Opp', 'N/A')}")
        print(f"⏱️  דקות: {game.get('MP', '0')}")
        print(f"🎯 נקודות: {game.get('PTS', '0')}")
        print(f"📦 ריבאונדים: {game.get('TRB', '0')}")
        print(f"🤝 אסיסטים: {game.get('AST', '0')}")
        print("="*70)
        
        print("\n✅ הצלחה! הנתונים נמשכו כ-DataFrame")
        print(f"\n📋 עמודות: {list(latest_game_df.columns)}")
        print(f"\n📊 DataFrame shape: {latest_game_df.shape}")
        
        return latest_game_df
        
    except requests.exceptions.RequestException as e:
        print(f"❌ שגיאת רשת: {e}")
        return None
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()
        return None
    
def chack_if_last_game_in_history(latest_game_df, history_df):
    if latest_game_df is None:
        print("⚠️  אין נתונים למשחק האחרון, לא ניתן לבדוק בהיסטוריה")
        return False
    
    latest_date = latest_game_df['Date'].values[0]
    
    if latest_date in history_df['Date'].values:
        print("✅ המשחק האחרון כבר קיים בהיסטוריה")

    else:
        print("⚠️  המשחק האחרון לא נמצא בהיסטוריה, ייתכן שזה משחק חדש")
        return False

def clean_and_process_data(last_game_df):
    last_game_df.rename(columns={
        'Unnamed: 5': 'Home/Away',
        'GS': 'Games Started',
        'Rk': 'Rank',
        'Gcar': 'Games_Career',
        'Gtm': 'Games_Team',
        'GS': 'Games_Started',
    }, inplace=True)
    last_game_df.loc[last_game_df['Home/Away'] == '@', 'Home/Away'] = 'Away'
    last_game_df.loc[last_game_df['Home/Away'] != 'Away', 'Home/Away'] = 'Home'
    last_game_df['Home/Away_num'] = np.where(last_game_df['Home/Away'] == 'Away', 0, 1)
    last_game_df[['Result_type', 'Score']] = last_game_df['Result'].str.split(',', expand=True)
    last_game_df[['Team_Score', 'Opponent_Score']] = last_game_df['Score'].str.split('-', expand=True)
    last_game_df['Win_lose_num'] = np.where(last_game_df['Result_type'] == 'W', 1, 0)
    last_game_df['Games_Started_num'] = np.where(last_game_df['Games_Started'] == '*', 1, 0)
    last_game_df['Games_Started_str'] = np.where(last_game_df['Games_Started'] == '*', 'Yes', 'No')
    return last_game_df

if __name__ == "__main__":
    # הרץ את הפונקציה
    latest_game_df = get_deni_latest_game()
    
    if latest_game_df is not None:
        print("\n" + "="*70)
        print("🎉 ה-DataFrame המלא:")
        print("="*70)
        print(latest_game_df)
        

obs_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(obs_dir, 'processed_seasons_data.csv')
history = pd.read_csv(csv_path)
is_latest_game_in_history = chack_if_last_game_in_history(latest_game_df, history)
if not is_latest_game_in_history:
    latest_game_df = clean_and_process_data(latest_game_df)
    updated_history = pd.concat([history, latest_game_df], ignore_index=True)
    updated_history.to_csv(csv_path, index=False)