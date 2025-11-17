
import os
from collections import defaultdict
import requests
import pandas as pd

pat = (os.getenv("GITHUB_TOKEN"))
headers = {"Authorization": f"token {pat}"}
request = requests.get("https://api.github.com/rate_limit", headers=headers)
print(request.json())

languages = {"Python", "Java", "Go", "JavaScript", "TypeScript", "Julia", "PHP", "Rust", "C++", "C#"}
lang_count = defaultdict(int)
watchers_count = defaultdict(int)
stargazers_count = defaultdict(int)
forks_count = defaultdict(int)
dates_count = defaultdict(str)

#iterate through each page of results
for p in range(1, 11):
    query = 'created:2025-10-01..2025-10-31' # change date as required
    url = f'https://api.github.com/search/repositories?q={query}&per_page=100&page={p}'
    response = requests.get(url)
    data = response.json()

    #Iterate through Json fields to gather data
    for field in data['items']:
        lang = field.get('language')
        if lang in languages:
            lang_count[lang] += 1
            num_watchers = field.get('watchers_count')
            num_stargazers = field.get('stargazers_count')
            num_forks = field.get('forks_count')

            watchers_count[lang] += num_watchers
            stargazers_count[lang] += num_stargazers
            forks_count[lang] += num_forks

rows = []
for lang in languages:
    data1 = [lang_count[lang], watchers_count[lang], forks_count[lang]]
    rows.append([query[8:], lang] + data1)

df = pd.DataFrame(rows, columns = ['Month', 'Language', 'Total Created', 'Watchers', 'Forks'])

file = "languages.csv"
if not os.path.exists('languages.csv'):
    df.to_csv('languages.csv', mode = 'w', index=False, header=True)
else:
    df.to_csv('languages.csv', mode = 'a', index=False, header=False)