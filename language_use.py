import requests
import os
import matplotlib.pyplot as plt

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
    if not isinstance(repo, dict):
        continue
    else:
        languages_url = repo["languages_url"]
    # Fetch languages for each repo
    languages_response = requests.get(languages_url, headers=headers)
    languages_data = languages_response.json()
    
    for lang, bytes_count in languages_data.items():
        if lang == "HTML" or "Makefile" in lang or "CSS" in lang:
            continue
        if lang not in languages_count:
            languages_count[lang] = 0
        languages_count[lang] += 1
total_bytes = sum(languages_count.values())
# Calculate percentages
percentages = {lang: round((count / total_bytes) * 100, 2) for lang, count in languages_count.items()}
# Display top 5 languages by percentage
sorted_languages = sorted(percentages.items(), key=lambda x: x[1], reverse=True)[:5]
labels = [label[0]+"\n("+str(languages_count[label[0]])+")" for label in sorted_languages] 
percentages = [percentage[1] for percentage in sorted_languages] 

plt.figure(figsize=(6, 6))
bars = plt.bar(range(len(labels)), percentages, color=['orange', 'red', 'purple', 'blue', 'green'])

# Add labels on the bars
for i, bar in enumerate(bars):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 3, f"{percentages[i]}%", ha='center', color='white', fontsize=12)

# Set x-axis ticks and labels
plt.xticks(range(len(labels)), labels) 

plt.title('Language Distribution')
plt.ylabel('Percentage (%)')
plt.xlabel('Languages (# of repos)')

# Save the figure
plt.tight_layout()
plt.savefig('chart-image.png')
