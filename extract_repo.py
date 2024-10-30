import requests
import csv
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

TOKEN = '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'
HEADERS = {'Authorization': f'Bearer {TOKEN}'}

users_csv = 'users.csv'
repos_csv = 'repositories.csv'
repo_fields = ['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name']

retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

def get_user_repos(login):
    """Fetch up to 500 most recent repositories for a user."""
    user_repos = []
    page = 1
    per_page = 100
    while True:
        repos_url = f'https://api.github.com/users/{login}/repos?per_page={per_page}&page={page}&sort=pushed'
        try:
            response = http.get(repos_url, headers=HEADERS)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories for user {login}: {e}")
            break
        
        repos = response.json()
        if not repos:
            break

        user_repos.extend(repos)
        if len(user_repos) >= 500:
            break

        page += 1
        time.sleep(1)

    return user_repos[:500]

def extract_repo_info(repo, login):
    """Extract required fields from the repository."""
    return {
        'login': login,
        'full_name': repo['full_name'],
        'created_at': repo['created_at'],
        'stargazers_count': repo.get('stargazers_count', 0),
        'watchers_count': repo.get('watchers_count', 0),
        'language': repo.get('language', ''),
        'has_projects': repo.get('has_projects', False),
        'has_wiki': repo.get('has_wiki', False),
        'license_name': repo['license']['key'] if repo.get('license') else ''
    }

with open(users_csv, mode='r', encoding='utf-8-sig') as users_file:
    users_reader = csv.DictReader(users_file)
    
    with open(repos_csv, mode='w', newline='', encoding='utf-8-sig') as repos_file:
        repo_writer = csv.DictWriter(repos_file, fieldnames=repo_fields)
        repo_writer.writeheader()

        for user in users_reader:
            login = user['login']
            print(f"Fetching repositories for user: {login}")

            repos = get_user_repos(login)

            for repo in repos:
                repo_info = extract_repo_info(repo, login)
                repo_writer.writerow(repo_info)

            time.sleep(2)

print(f"Repositories data saved to {repos_csv}")
