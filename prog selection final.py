from github import Github
import csv

# === Configuration ===
GITHUB_TOKEN = "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"
MAX_RESULTS = 50
MIN_COMMITS = 500
CSV_FILE = "unity_csharp_games_commits_filtered.csv"

# === Recherche ciblée sur Unity/C# ===
SEARCH_QUERY = "unity game language:C#"

# === Initialisation GitHub ===
g = Github(GITHUB_TOKEN)

def is_game_project(repo):
    """Filtre pour exclure les assets, plugins, templates, etc."""
    EXCLUDE_KEYWORDS = [
        "plugin", "tool", "editor", "sdk", "demo", "template", "asset", "shader", "test", "framework", "sample"
    ]
    desc = (repo.description or "").lower()
    name = repo.name.lower()
    full_text = name + " " + desc
    return not any(keyword in full_text for keyword in EXCLUDE_KEYWORDS)

def fetch_filtered_games():
    print("🔍 Recherche de jeux Unity en C# avec >500 commits...")
    results = []
    for repo in g.search_repositories(query=SEARCH_QUERY, sort="stars", order="desc"):
        if len(results) >= MAX_RESULTS:
            break
        if repo.language != "C#":
            continue
        if not is_game_project(repo):
            continue
        try:
            commit_count = repo.get_commits().totalCount
            if commit_count < MIN_COMMITS:
                continue
        except Exception as e:
            print(f"⚠️ Erreur lecture commits pour {repo.full_name} : {e}")
            continue
        results.append({
            "name": repo.full_name,
            "url": repo.html_url,
            "stars": repo.stargazers_count,
            "commits": commit_count,
            "language": repo.language,
            "description": repo.description or ""
        })
        print(f"✅ {repo.full_name} | {commit_count} commits")
    return results

def save_to_csv(repos, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "url", "stars", "commits", "language", "description"])
        writer.writeheader()
        for repo in repos:
            writer.writerow(repo)

if __name__ == "__main__":
    games = fetch_filtered_games()
    save_to_csv(games, CSV_FILE)
    print(f"\n✅ Résultats enregistrés dans : {CSV_FILE}")
