import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import numpy as np

def get_deni_latest_game():
    """מושך את המשחק האחרון של דני אבדיה"""
    url = "https://www.basketball-reference.com/players/a/avdijde01/gamelog/2026"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        print("🏀 מושך נתונים מ-Basketball Reference...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': 'player_game_log_reg'})
        
        if not table:
            print("❌ לא מצאתי את הטבלה")
            return None
        
        print("✅ מצאתי את הטבלה!")
        
        df = pd.read_html(str(table))[0]
        df = df[df['Rk'].notna()]
        df = df[df['Rk'] != 'Rk']
        
        print(f"📊 סה\"כ {len(df)} משחקים בעונה")
        
        latest_game_df = df.iloc[[-1]]
        
        mp_value = latest_game_df['MP'].values[0]
        if pd.isna(mp_value) or mp_value == '':
            print("⚠️  דני לא שיחק במשחק האחרון")
            return None
        
        game = latest_game_df.iloc[0]
        print("\n" + "="*70)
        print("📊 המשחק האחרון של דני אבדיה:")
        print("="*70)
        print(f"📅 תאריך: {game['Date']}")
        print(f"🏀 יריב: {game['Opp']}")
        print(f"🎯 נקודות: {game['PTS']}")
        print("="*70)
        
        return latest_game_df
        
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        import traceback
        traceback.print_exc()
        return None

def check_if_last_game_in_history(latest_game_df, history_df):
    """בודק אם המשחק האחרון כבר קיים בהיסטוריה"""
    if latest_game_df is None:
        return False
    
    latest_date = latest_game_df['Date'].values[0]
    
    if latest_date in history_df['Date'].values:
        print("✅ המשחק כבר קיים בהיסטוריה")
        return True
    else:
        print("🆕 משחק חדש נמצא!")
        return False

def clean_and_process_data(df):
    """מעבד ומנקה את הנתונים"""
    df = df.copy()  # עבוד על עותק
    
    df.rename(columns={
        'Unnamed: 5': 'Home/Away',
        'Rk': 'Rank',
        'Gcar': 'Games_Career',
        'Gtm': 'Games_Team',
        'GS': 'Games_Started',
    }, inplace=True)
    
    df.loc[df['Home/Away'] == '@', 'Home/Away'] = 'Away'
    df.loc[df['Home/Away'] != 'Away', 'Home/Away'] = 'Home'
    df['Home/Away_num'] = np.where(df['Home/Away'] == 'Away', 0, 1)
    
    df[['Result_type', 'Score']] = df['Result'].str.split(',', expand=True)
    df[['Team_Score', 'Opponent_Score']] = df['Score'].str.split('-', expand=True)
    
    df['Win_lose_num'] = np.where(df['Result_type'] == 'W', 1, 0)
    df['Games_Started_num'] = np.where(df['Games_Started'] == '*', 1, 0)
    df['Games_Started_str'] = np.where(df['Games_Started'] == '*', 'Yes', 'No')
    
    return df

if __name__ == "__main__":
    # משוך את המשחק האחרון
    latest_game_df = get_deni_latest_game()
    
    if latest_game_df is not None:
        # נתיב לקובץ ההיסטוריה
        obs_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(obs_dir, 'processed_seasons_data.csv')
        
        # טען את ההיסטוריה
        try:
            history = pd.read_csv(csv_path)
            print(f"📂 נטען קובץ היסטוריה עם {len(history)} משחקים")
        except FileNotFoundError:
            print("⚠️  קובץ היסטוריה לא נמצא, יוצר חדש...")
            history = pd.DataFrame()
        
        # בדוק אם המשחק קיים
        is_in_history = check_if_last_game_in_history(latest_game_df, history)
        
        if not is_in_history:
            print("\n🔄 מעבד ומעדכן את ההיסטוריה...")
            latest_game_df = clean_and_process_data(latest_game_df)
            updated_history = pd.concat([history, latest_game_df], ignore_index=True)
            updated_history.to_csv(csv_path, index=False)
            print(f"✅ ההיסטוריה עודכנה! סה\"כ {len(updated_history)} משחקים")
        else:
            print("ℹ️  המשחק כבר קיים, אין צורך בעדכון")
    else:
        print("❌ לא ניתן לעדכן - לא נמצא משחק חדש")