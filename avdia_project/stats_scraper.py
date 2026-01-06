"""
NBA Stats Scraper for Deni Avdija
Retrieves all game statistics from career start through current season
"""

import requests
import pandas as pd
import time

# Deni Avdija's player ID
PLAYER_ID = "1630166"

# Seasons to retrieve (start of career through current)
SEASONS = ["2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]

# NBA Stats API endpoint for player game logs
API_URL = "https://stats.nba.com/stats/playergamelog"

# Headers to avoid being blocked by NBA.com API
HEADERS = {
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9,he;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.nba.com/',
    'Origin': 'https://www.nba.com',
    'Connection': 'keep-alive',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site'
}


def fetch_game_logs(player_id, season, max_retries=3):
    """
    Fetch game logs for a specific player and season from NBA Stats API

    Args:
        player_id (str): NBA player ID
        season (str): Season in format 'YYYY-YY' (e.g., '2020-21')
        max_retries (int): Maximum number of retry attempts

    Returns:
        dict: JSON response from API or None if request fails
    """
    params = {
        'PlayerID': player_id,
        'Season': season,
        'SeasonType': 'Regular Season',
        'LeagueID': '00'
    }

    for attempt in range(max_retries):
        try:
            # Add delay before retry attempts
            if attempt > 0:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"\n  Retrying (attempt {attempt + 1}/{max_retries}) in {wait_time}s...", end=" ")
                time.sleep(wait_time)

            response = requests.get(API_URL, headers=HEADERS, params=params, timeout=45)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                print(f"\n  Timeout occurred, retrying...", end="")
            else:
                print(f"\n  Max retries reached due to timeout")
                return None
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"\n  Error: {e}, retrying...", end="")
            else:
                print(f"\n  Error fetching data: {e}")
                return None

    return None


def parse_game_logs(json_data, season):
    """
    Parse JSON response and extract relevant statistics

    Args:
        json_data (dict): JSON response from NBA API
        season (str): Season string to add to each row

    Returns:
        list: List of dictionaries containing game statistics
    """
    if not json_data or 'resultSets' not in json_data:
        return []

    result_set = json_data['resultSets'][0]
    headers = result_set['headers']
    rows = result_set['rowSet']

    games = []
    for row in rows:
        # Create a dictionary mapping headers to values
        game_dict = dict(zip(headers, row))

        # Calculate shooting percentages (handle division by zero)
        fga = game_dict.get('FGA', 0)
        fg_pct = round(game_dict.get('FG_PCT', 0) * 100, 1) if fga > 0 else 0.0

        fg3a = game_dict.get('FG3A', 0)
        fg3_pct = round(game_dict.get('FG3_PCT', 0) * 100, 1) if fg3a > 0 else 0.0

        fta = game_dict.get('FTA', 0)
        ft_pct = round(game_dict.get('FT_PCT', 0) * 100, 1) if fta > 0 else 0.0

        # Extract relevant information
        game_data = {
            'Game Date': game_dict.get('GAME_DATE', ''),
            'Season': season,
            'Matchup': game_dict.get('MATCHUP', ''),
            'Result': game_dict.get('WL', ''),
            'Minutes Played': game_dict.get('MIN', 0),
            'Points': game_dict.get('PTS', 0),
            'Rebounds': game_dict.get('REB', 0),
            'Assists': game_dict.get('AST', 0),
            'Steals': game_dict.get('STL', 0),
            'Blocks': game_dict.get('BLK', 0),
            'FG%': fg_pct,
            '3P%': fg3_pct,
            'FT%': ft_pct
        }

        games.append(game_data)

    return games


def main():
    """
    Main function to retrieve all career stats and save to CSV
    """
    print(f"Starting data retrieval for Deni Avdija (Player ID: {PLAYER_ID})")
    print(f"Retrieving seasons: {', '.join(SEASONS)}\n")

    all_games = []

    # Fetch data for each season
    for season in SEASONS:
        print(f"Processing season: {season}...", end=" ")

        # Fetch game logs
        json_data = fetch_game_logs(PLAYER_ID, season)

        if json_data:
            # Parse the data
            games = parse_game_logs(json_data, season)
            all_games.extend(games)
            print(f"✓ Retrieved {len(games)} games")
        else:
            print(f"✗ Failed to retrieve data")

        # Be respectful to the API - add a delay between requests
        time.sleep(2)

    # Convert to DataFrame
    if all_games:
        df = pd.DataFrame(all_games)

        # Sort by date (oldest to newest)
        df['Game Date'] = pd.to_datetime(df['Game Date'])
        df = df.sort_values('Game Date')

        # Format date back to string for CSV
        df['Game Date'] = df['Game Date'].dt.strftime('%Y-%m-%d')

        # Save to CSV
        output_file = 'deni_avdija_career_stats.csv'
        df.to_csv(output_file, index=False)

        print(f"\n{'='*60}")
        print(f"Success! Retrieved {len(all_games)} total games")
        print(f"Data saved to: {output_file}")
        print(f"{'='*60}")

        # Print summary statistics
        print("\nCareer Summary:")
        print(f"  Total Games: {len(df)}")
        print(f"  Wins: {len(df[df['Result'] == 'W'])}")
        print(f"  Losses: {len(df[df['Result'] == 'L'])}")
        print(f"  Average Points: {df['Points'].mean():.1f}")
        print(f"  Average Rebounds: {df['Rebounds'].mean():.1f}")
        print(f"  Average Assists: {df['Assists'].mean():.1f}")
    else:
        print("\n✗ No data retrieved. Please check your connection and try again.")


if __name__ == "__main__":
    main()
