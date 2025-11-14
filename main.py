import requests
import streamlit as st

st.set_page_config(page_title="GameCastAI – Football", page_icon="⚽")
st.title("⚽ GameCastAI – Football Predictions (Top 5 Leagues)")


# --------------------------------------------------
# API CONFIGURATION
# --------------------------------------------------
API_KEY = "8895fc67cb31a6d94674c943088653a9"
BASE_URL = "https://v3.football.api-sports.io/"

headers = {"x-apisports-key": API_KEY}

url = f"{BASE_URL}/teams"
params = {"league": 39, "season": 2023}

print("Calling API...")
res = requests.get(url, headers=headers, params=params)

print("Status Code:", res.status_code)
print("Raw Output:", res.text[:500])


# --------------------------------------------------
# TOP 5 LEAGUES
# --------------------------------------------------
TOP_LEAGUES = {
    "Premier League (England)": 39,
    "La Liga (Spain)": 140,
    "Serie A (Italy)": 135,
    "Bundesliga (Germany)": 78,
    "Ligue 1 (France)": 61,
}


# --------------------------------------------------
# FETCH TEAMS BY LEAGUE
# --------------------------------------------------
@st.cache_data
def get_teams(league_id, season=2023):
    url = f"{BASE_URL}/teams"
    params = {"league": league_id, "season": season}

    r = requests.get(url, headers=headers, params=params)

    # If request failed
    if r.status_code != 200:
        st.error(f"API Error {r.status_code}")
        st.write(r.text)
        return {}

    # Try reading JSON
    try:
        data = r.json()
    except:
        st.error("JSON decode error")
        st.write(r.text)
        return {}

    # If API returned empty response
    if "response" not in data or not isinstance(data["response"], list):
        st.error("Unexpected API format")
        st.write(data)
        return {}

    teams = {}

    for item in data["response"]:
        team_name = item["team"]["name"]
        team_id = item["team"]["id"]
        teams[team_name] = team_id

    return teams


# --------------------------------------------------
# FETCH TEAM STATS
# --------------------------------------------------
def fetch_team_stats(team_id, league_id, season):
    url = f"{BASE_URL}/teams/statistics"
    params = {"team": team_id, "league": league_id, "season": season}
    res = requests.get(url, headers=headers, params=params).json()
    return res.get("response", None)


# --------------------------------------------------
# FETCH TOP SCORERS (LEAGUE)
# --------------------------------------------------
def fetch_top_scorers(league_id, season):
    url = f"{BASE_URL}/players/topscorers"
    params = {"league": league_id, "season": season}
    res = requests.get(url, headers=headers, params=params).json()
    return res.get("response", [])


# --------------------------------------------------
# LEAGUE SELECTION UI
# --------------------------------------------------
st.subheader("🏆 Select League")
league_name = st.selectbox("Choose a League", list(TOP_LEAGUES.keys()))
league_id = TOP_LEAGUES[league_name]

season = 2023

# Load teams
teams_dict = get_teams(league_id, season)

if not teams_dict:
    st.error("Error fetching teams.")
    st.stop()

team_names = list(teams_dict.keys())


# --------------------------------------------------
# TEAM SELECTION
# --------------------------------------------------
st.subheader("⚔️ Select Teams to Compare")

team1_name = st.selectbox("Team 1", team_names)
team2_name = st.selectbox("Team 2", team_names)

team1_id = teams_dict[team1_name]
team2_id = teams_dict[team2_name]


# --------------------------------------------------
# ANALYZE MATCH
# --------------------------------------------------
if st.button("🔍 Analyze Match"):
    with st.spinner("Fetching statistics..."):
        team1 = fetch_team_stats(team1_id, league_id, season)
        team2 = fetch_team_stats(team2_id, league_id, season)

        if not team1 or not team2:
            st.error("❌ Could not fetch team data.")
            st.stop()

        # --------------------------------------------------
        # EXTRACT TEAM STATS
        # --------------------------------------------------
        def extract_stats(stats):
            goals_avg = float(stats["goals"]["for"]["average"]["total"]) or 1.0
            wins = stats["fixtures"]["wins"]["total"]
            form = len(stats["form"])
            return goals_avg, wins, form

        t1_goals, t1_wins, t1_form = extract_stats(team1)
        t2_goals, t2_wins, t2_form = extract_stats(team2)

        # --------------------------------------------------
        # PREDICTIONS
        # --------------------------------------------------

        # Expected Goals (xG)
        t1_xg = round((t1_goals * 0.7) + (t1_wins * 0.03) + (t1_form * 0.01), 2)
        t2_xg = round((t2_goals * 0.7) + (t2_wins * 0.03) + (t2_form * 0.01), 2)

        # Final Score Prediction
        t1_score = max(0, round(t1_xg))
        t2_score = max(0, round(t2_xg))

        # Winner Prediction
        if t1_score > t2_score:
            winner = f"🏆 **{team1_name} Wins**"
        elif t2_score > t1_score:
            winner = f"🏆 **{team2_name} Wins**"
        else:
            winner = "🤝 **Draw**"

        # --------------------------------------------------
        # FETCH TOP 5 SCORERS
        # --------------------------------------------------
        topscorers = fetch_top_scorers(league_id, season)

        top_list = []
        for p in topscorers[:5]:
            player = p["player"]["name"]
            goals = p["statistics"][0]["goals"]["total"]
            tname = p["statistics"][0]["team"]["name"]
            top_list.append(f"{player} ({tname}) – {goals} goals")

        # --------------------------------------------------
        # DISPLAY RESULTS
        # --------------------------------------------------
        st.success("✅ Match Analysis Ready")

        st.subheader("📊 Predicted Final Score")
        st.write(f"**{team1_name} {t1_score} – {t2_score} {team2_name}**")

        st.subheader("🏆 Match Winner")
        st.write(winner)

        st.subheader("🎯 Expected Goals (xG)")
        st.write(f"{team1_name}: **{t1_xg}**")
        st.write(f"{team2_name}: **{t2_xg}**")

        st.subheader("🔥 League Top Scorers")
        for item in top_list:
            st.write("- " + item)


# import requests

# API_KEY = "8895fc67cb31a6d94674c943088653a9"
# BASE_URL = "https://v3.football.api-sports.io"

# headers = {"x-apisports-key": API_KEY}

# for league in [39, 140, 135, 78, 61]:
#     url = f"{BASE_URL}/teams"
#     params = {"league": league, "season": 2023}
#     r = requests.get(url, headers=headers, params=params).json()

#     print("League:", league, "Teams:", len(r["response"]))


# import requests

# API_KEY = "8895fc67cb31a6d94674c943088653a9"

# url = "https://v3.football.api-sports.io/teams"
# headers = {"x-apisports-key": API_KEY}

# params = {"league": 39, "season": 2023}

# r = requests.get(url, headers=headers, params=params)

# print("Status:", r.status_code)
# print(r.text)
