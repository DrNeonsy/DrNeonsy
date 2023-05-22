import requests
import os

# GitHub username
username = "GITHUB_USER_NAME"

# Personal access token (Needs "contents" read-only, paired with "metadata", if a fine grained token is being used)
token = "YOUR_AUTH_TOKEN"

# Headers for authenticated requests
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
}

# Fetch the list of repositories
response = requests.get(f"https://api.github.com/user/repos", headers=headers)
repos = response.json()

# Separate public and private repositories
public_repos = [repo for repo in repos if not repo["private"]]
private_repos = [repo for repo in repos if repo["private"]]

# Ask the user whether they want to clone a public or private repository
print("Please choose the type of repository you want to clone:")
print("0: Public")
print("1: Private")
repo_type_input = input("Enter your choice (Default is public): ")

# Default to public if nothing is entered
repo_type = "private" if repo_type_input == "1" else "public"

# Choose the appropriate list of repositories
chosen_repos = private_repos if repo_type == "private" else public_repos

if response.status_code == 200:
    # Display the repository names with index numbers
    print(f"{repo_type.capitalize()} Repositories:")
    for index, repo in enumerate(chosen_repos, start=1):
        # Print the index and repository name
        print(f"{index}. {repo['name']}")

    # Print an extra newline after the last repository
    print()

    # Prompt for repository selection
    while True:
        try:
            repo_index = int(
                input(
                    f"Enter the number of the {repo_type} repository to clone (or 0 to exit): "
                )
            )
            if repo_index == 0:
                break
            elif 1 <= repo_index <= len(chosen_repos):
                selected_repo = chosen_repos[repo_index - 1]
                break
            else:
                print(
                    f"Invalid number. Please enter a number between 1 and {len(chosen_repos)}."
                )
        except ValueError:
            print("Invalid input. Please enter a number.")

    if "selected_repo" in locals():
        # Clone the selected repository
        clone_url = selected_repo["clone_url"]
        repo_name = selected_repo["name"]
        print(f"Cloning repository '{repo_name}'...")
        result = os.system(f"git clone {clone_url}")
        if result != 0:
            print("Failed to clone the repository.")
        else:
            print("Repository cloned successfully.")
else:
    print(f"Failed to fetch repositories. Error: {response.status_code}")
