import requests
import os

TOKEN = os.environ.get('GITHUB_TOKEN')
USERNAME = "MikaPS"
headers = {
    "Authorization": f"token {TOKEN}"
}
# Fetch repositories
repos_url = f"https://api.github.com/users/{USERNAME}/repos"
repos_response = requests.get(repos_url, headers=headers)
repos_data = repos_response.json()

languages_count = {}

for repo in repos_data:
    repo_name = repo["name"]
    languages_url = repo["languages_url"]
    
    # Fetch languages for each repo
    languages_response = requests.get(languages_url, headers=headers)
    languages_data = languages_response.json()
    
    for lang, bytes_count in languages_data.items():
        if lang not in languages_count:
            languages_count[lang] = 0
        languages_count[lang] += bytes_count
total_bytes = sum(languages_count.values())

# Calculate percentages
percentages = {lang: round((count / total_bytes) * 100, 2) for lang, count in languages_count.items()}
# Display top 5 languages by percentage
sorted_languages = sorted(percentages.items(), key=lambda x: x[1], reverse=True)[:5]
# print(sorted_languages)
# Display results
# for lang, percentage in sorted_languages:
#     print(f"{lang}: {percentage:.2f}%")

def get_language_data():
    return sorted_languages
