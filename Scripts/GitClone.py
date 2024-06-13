import requests
import os
import re
import msvcrt
import time

# Personal access token (Needs "contents" read-only, paired with "metadata", if a fine grained token is being used)
token = "YOUR_AUTH_TOKEN"


# Headers for authenticated requests
headers = {
    "Authorization": f"token {token}",
    "Accept": "application.vnd.github.v3+json",
}

# Fetch the list of repositories
response = requests.get(f"https://api.github.com/user/repos", headers=headers)
if response.status_code == 401:
    os.system("cls" if os.name == "nt" else "clear")
    print("Error: Invalid authentication token or insufficient permissions.")
    print("Press any key to exit...")
    msvcrt.getch()
    exit()
all_repos = response.json()

while True:
    # Prompt for repository search
    search_query = ""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Search for repo (Escape to exit): {search_query}")
        key = msvcrt.getch()
        if key == b"\x1b":  # Escape key
            exit()
        elif key == b"\r":  # Enter key
            break
        elif key == b"\x08":  # Backspace key
            search_query = search_query[:-1]
        else:
            search_query += key.decode()
    search_query = search_query.strip()

    if not search_query:
        matched_repos = all_repos
    else:
        # Perform lazy fuzzy search
        search_words = search_query.lower().split()
        matched_repos = [
            repo
            for repo in all_repos
            if all(word in repo["name"].lower() for word in search_words)
        ]

    # Sort matched repositories alphabetically
    matched_repos.sort(key=lambda repo: repo["name"].lower())

    if matched_repos:
        selected_index = 0
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            for index, repo in enumerate(matched_repos):
                if index == selected_index:
                    print(f"> {repo['name']}")
                else:
                    print(f"  {repo['name']}")
            print(
                "\nPress Enter to clone the selected repository, Escape to go back to search"
            )

            key = ord(msvcrt.getch())
            if key == 27:  # Escape key
                os.system("cls" if os.name == "nt" else "clear")
                break
            elif key == 13:  # Enter key
                selected_repo = matched_repos[selected_index]

                # Clone the selected repository
                clone_url = selected_repo["clone_url"]
                repo_name = selected_repo["name"]
                print(f"Cloning repository '{repo_name}'...")
                result = os.system(f"git clone {clone_url}")
                if result != 0:
                    print("Failed to clone the repository.")
                else:
                    print("Repository cloned successfully.")
                    exit()  # Exit the script after cloning
            elif key == 80:  # Down arrow
                selected_index = (selected_index + 1) % len(matched_repos)
            elif key == 72:  # Up arrow
                selected_index = (selected_index - 1) % len(matched_repos)

        if key == 27:  # Escape key
            continue

    else:
        os.system("cls" if os.name == "nt" else "clear")
        print("No repo found, please try again\n")
        search_query = ""
        time.sleep(1.8)
