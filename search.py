import requests

API_KEY = "3613869e86msh9fba730f58c5652p1dc262jsn0b7d179dbee0"
BASE_URL = "https://free-api-live-football-data.p.rapidapi.com"


def api_request(endpoint, params=None):
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com",
    }

    try:
        response = requests.get(
            f"{BASE_URL}/{endpoint}", headers=headers, params=params
        )
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def extract_suggestions(data, limit=5):
    return data.get("response", {}).get("suggestions", [])[:limit]


def search_teams(query, limit=5):
    data = api_request("football-teams-search", {"search": query})
    return extract_suggestions(data, limit)


def search_players(query, limit=5):
    data = api_request("football-players-search", {"search": query})
    return extract_suggestions(data, limit)


def search_leagues(query, limit=5):
    data = api_request("football-leagues-search", {"search": query})
    return extract_suggestions(data, limit)


def search_matches(query, limit=5):
    data = api_request("football-matches-search", {"search": query})
    return extract_suggestions(data, limit)


def search_all(query, limit=5):
    return {
        "Teams": search_teams(query, limit),
        "Players": search_players(query, limit),
        "Leagues": search_leagues(query, limit),
        "Matches": search_matches(query, limit),
    }


def print_results(title, results):
    print("\n==== " + title + " ====")
    if not results:
        print("No results found.")
        return

    for item in results:
        name = item.get("name", "Unknown")
        league = item.get("leagueName", "")
        score = item.get("score", "")

        if league:
            print(f"- {name}  ({league})")
        else:
            print(f"- {name}")


def main_menu():
    while True:
        print("\n==============================")
        print(" FOOTBALL SEARCH MENU")
        print("==============================")
        print("1. Search Teams")
        print("2. Search Players")
        print("3. Search Leagues")
        print("4. Search Matches")
        print("5. Search Everything (All)")
        print("6. Exit")
        print("==============================")

        choice = input("Enter your choice: ")

        if choice == "6":
            print("Goodbye!")
            break

        if choice not in {"1", "2", "3", "4", "5"}:
            print("Invalid choice. Try again.")
            continue

        query = input("Enter search text: ")

        if choice == "1":
            results = search_teams(query)
            print_results("Teams", results)

        elif choice == "2":
            results = search_players(query)
            print_results("Players", results)

        elif choice == "3":
            results = search_leagues(query)
            print_results("Leagues", results)

        elif choice == "4":
            results = search_matches(query)
            print_results("Matches", results)

        elif choice == "5":
            results = search_all(query)
            for category, items in results.items():
                print_results(category, items)


main_menu()
