# Tools-in-data-science
This repo contains the project I completed as part of the IITM BS Degree coursework "Tools in Data Science."

## Project-1: Singapore GitHub data analysis
1. GitHub data for Singapore users with 100+ followers was gathered and processed using GitHub's API and 2 Python scripts~
   1. **`extract_users.py`** - fetches user data(name, company, bio, etc.) and stores it in **`users.csv`**. Python libraries used: `requests`, `csv` and `time`.
   2. **`extract_repo.py`** - retrieves up to 500 recent repositories for each user and saves repository info to **`repositories.csv`**. Python libraries used: `requests`, `csv`, `time`, `requests.adapters.HTTPAdapter` and `urllib3.util.Retry`.

2. The one insight that caught me intriguing through this analysis is the company that the majority of these developers work at, which is `NATIONAL UNIVERSITY OF SINGAPORE`.

3. To make a striking impact, the Singaporean developers could use the `mit` license and develop skills on the most popular languages: `JavaScript` and `Python`. Additionally, collaborating with institutions like `NATIONAL UNIVERSITY OF SINGAPORE` can boost their networking. They should aim to maintain well-documented repositories with projects and wikis that can improve engagement and attract followers.
