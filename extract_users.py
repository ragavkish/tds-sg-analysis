import requests
import csv
import time

TOKEN = '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'
HEADERS = {'Authorization': f'Bearer {TOKEN}'}

location = 'Singapore'
min_followers = 100
per_page = 30
page = 1

csv_file = 'users.csv'
fields = ['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at']

def clean_company_name(company):
    if company:
        company = company.strip()
        if company.startswith('@'):
            company = company[1:]
        company = company.upper()
    return company

def safe_encode(value):
    if value:
        return value.encode('utf-8', 'replace').decode('utf-8')
    return ''

def get_user_details(login):
    user_url = f'https://api.github.com/users/{login}'
    for attempt in range(3):
        response = requests.get(user_url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        time.sleep(1)
    return None

def search_users(page):
    users_url = f'https://api.github.com/search/users?q=location:{location}+followers:>{min_followers}&per_page={per_page}&page={page}'
    response = requests.get(users_url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('items', [])
    return []

with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()

    while True:
        users = search_users(page)
        if not users:
            break

        for user in users:
            user_details = get_user_details(user['login'])
            if user_details:
                writer.writerow({
                    'login': user_details['login'],
                    'name': safe_encode(user_details.get('name', '')),
                    'company': clean_company_name(safe_encode(user_details.get('company', ''))),
                    'location': safe_encode(user_details.get('location', '')),
                    'email': safe_encode(user_details.get('email', '')),
                    'hireable': user_details.get('hireable', ''),
                    'bio': safe_encode(user_details.get('bio', '')),
                    'public_repos': user_details.get('public_repos', 0),
                    'followers': user_details.get('followers', 0),
                    'following': user_details.get('following', 0),
                    'created_at': user_details.get('created_at', '')
                })

        time.sleep(2)
        page += 1

print(f"Data saved to {csv_file}")
