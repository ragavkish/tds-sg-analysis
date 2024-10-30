#1) top 5 users in Singapore with the highest number of followers
import csv
top_users = []
with open('users.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    sorted_users = sorted(reader, key=lambda x: int(x['followers']), reverse=True)
    top_users = [user['login'] for user in sorted_users[:5]]
print(', '.join(top_users))

#2) 5 earliest registered GitHub users
from datetime import datetime
top_earliest_users = []
with open('users.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    sorted_users = sorted(reader, key=lambda x: datetime.strptime(x['created_at'], '%Y-%m-%dT%H:%M:%SZ'))
    top_earliest_users = [user['login'] for user in sorted_users[:5]]
print(', '.join(top_earliest_users))

#3) 3 most popular license among these users
from collections import Counter
license_counts = Counter()
with open('repositories.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        license_name = row['license_name']
        if license_name:
            license_counts[license_name] += 1
top_licenses = [license for license, _ in license_counts.most_common(3)]
print(', '.join(top_licenses))

#4) company that majority of these developers work at
from collections import Counter
def clean_company_name(company):
    if company:
        company = company.strip()
        if company.startswith('@'):
            company = company[1:]
        company = company.upper()
    return company
company_counts = Counter()
with open('users.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        company = clean_company_name(row['company'])
        if company:
            company_counts[company] += 1
most_common_company = company_counts.most_common(1)[0][0] if company_counts else None
print(most_common_company)

#5) most popular programming language
from collections import Counter
language_counts = Counter()
with open('repositories.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        language = row['language']
        if language:
            language_counts[language] += 1
most_popular_language = language_counts.most_common(1)[0][0] if language_counts else None
print(most_popular_language)

#6) second most popular programming language after 2020
from collections import Counter
from datetime import datetime
recent_users = set()
with open('users.csv', mode='r', encoding='utf-8-sig') as users_file:
    users_reader = csv.DictReader(users_file)
    for user in users_reader:
        if datetime.strptime(user['created_at'], '%Y-%m-%dT%H:%M:%SZ') > datetime(2020, 1, 1):
            recent_users.add(user['login'])
language_counts = Counter()
with open('repositories.csv', mode='r', encoding='utf-8-sig') as repos_file:
    repos_reader = csv.DictReader(repos_file)
    for repo in repos_reader:
        if repo['login'] in recent_users:
            language = repo['language']
            if language:
                language_counts[language] += 1
second_most_popular_language = language_counts.most_common(2)[1][0] if len(language_counts) > 1 else None
print(second_most_popular_language)

#7) language with the highest average number of stars per repository
from collections import defaultdict
language_stats = defaultdict(lambda: {'total_stars': 0, 'count': 0})
with open('repositories.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        language = row['language']
        stars = int(row['stargazers_count'])
        if language:
            language_stats[language]['total_stars'] += stars
            language_stats[language]['count'] += 1
highest_avg_language = None
highest_avg_stars = 0
for language, stats in language_stats.items():
    if stats['count'] > 0:
        avg_stars = stats['total_stars'] / stats['count']
        if avg_stars > highest_avg_stars:
            highest_avg_stars = avg_stars
            highest_avg_language = language
print(highest_avg_language)

#8)top 5 in terms of leader_strength = followers / (1 + following)
users_strength = []
with open('users.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        followers = int(row['followers'])
        following = int(row['following'])
        leader_strength = followers / (1 + following)
        users_strength.append((row['login'], leader_strength))
top_5_users = sorted(users_strength, key=lambda x: x[1], reverse=True)[:5]
top_5_logins = [user[0] for user in top_5_users]
print(', '.join(top_5_logins))

#9)correlation between the number of followers and the number of public repositories
import csv
from scipy.stats import pearsonr
followers = []
public_repos = []
with open('users.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        followers.append(int(row['followers']))
        public_repos.append(int(row['public_repos']))
correlation, _ = pearsonr(followers, public_repos)
print(f"{correlation:.3f}")

#10)regression slope of followers on repos
from scipy.stats import linregress
followers = []
public_repos = []
with open('users.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        followers.append(int(row['followers']))
        public_repos.append(int(row['public_repos']))
slope, _, _, _, _ = linregress(public_repos, followers)
print(f"{slope:.3f}")

#11)correlation b/w projects and wiki-enabled
import csv
from scipy.stats import pearsonr
has_projects = []
has_wiki = []
with open('repositories.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        has_projects.append(1 if row['has_projects'].lower() == 'true' else 0)
        has_wiki.append(1 if row['has_wiki'].lower() == 'true' else 0)
correlation, _ = pearsonr(has_projects, has_wiki)
print(f"{correlation:.3f}")

#12)do hireable users follow more people?
hireable_following = []
non_hireable_following = []
with open('users.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        following = int(row['following'])
        if row['hireable'].lower() == 'true':
            hireable_following.append(following)
        else:
            non_hireable_following.append(following)
average_following_hireable = sum(hireable_following) / len(hireable_following) if hireable_following else 0
average_following_non_hireable = sum(non_hireable_following) / len(non_hireable_following) if non_hireable_following else 0
difference = average_following_hireable - average_following_non_hireable
print(f"{difference:.3f}")

#13)regression slope of followers on bio wordcount
from scipy.stats import linregress
bio_word_counts = []
followers = []
with open('users.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row['bio'].strip():
            bio_word_count = len(row['bio'].split())
            bio_word_counts.append(bio_word_count)
            followers.append(int(row['followers']))
slope, _, _, _, _ = linregress(bio_word_counts, followers)
print(f"{slope:.3f}")

#14) the top 5 users with most repositories created on weekends
from datetime import datetime
from collections import Counter
weekend_repos = Counter()
with open('repositories.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        created_at = datetime.strptime(row['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        if created_at.weekday() >= 5:
            weekend_repos[row['login']] += 1
top_5_users = [user for user, _ in weekend_repos.most_common(5)]
print(', '.join(top_5_users))

#15) difference in users sharing email when hireable
hireable_with_email = 0
hireable_total = 0
non_hireable_with_email = 0
non_hireable_total = 0
with open('users.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        has_email = bool(row['email'].strip())
        if row['hireable'].lower() == 'true':
            hireable_total += 1
            hireable_with_email += has_email
        else:
            non_hireable_total += 1
            non_hireable_with_email += has_email
fraction_hireable_with_email = hireable_with_email / hireable_total if hireable_total else 0
fraction_non_hireable_with_email = non_hireable_with_email / non_hireable_total if non_hireable_total else 0
difference = fraction_hireable_with_email - fraction_non_hireable_with_email
print(f"{difference:.3f}")

#16) most common surname
from collections import Counter
surnames = Counter()
with open('users.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row['name'].strip()
        if name:
            surname = name.split()[-1] 
            surnames[surname] += 1
max_count = max(surnames.values())
most_common_surnames = sorted([surname for surname, count in surnames.items() if count == max_count])
print(', '.join(most_common_surnames))