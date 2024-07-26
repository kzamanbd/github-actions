import os
from skpy import Skype
import requests

# Retrieve environment variables
skype_username = os.environ.get("SKYPE_USERNAME")
skype_password = os.environ.get("SKYPE_PASSWORD")
author_name = os.environ.get("AUTHOR_NAME")
branch_name = os.environ.get("BRANCH_NAME")
last_commit = os.environ.get("LAST_COMMIT")
release_notes = os.environ.get("RELEASE_NOTES")
build_result = os.environ.get("BUILD_RESULT")
github_run_id = os.environ.get('GITHUB_RUN_ID')
github_actor = os.environ.get('GITHUB_ACTOR')
token = os.environ.get('GITHUB_TOKEN')

url = "https://devweb.jerpbd.com"
origin = "Development Environment"
if branch_name == "release/production":
    url = "https://njpl.jerpbd.com"
    origin = "Production Environment"

if build_result == "cancelled":
    try:
        response = requests.get(f"https://api.github.com/users/{github_actor}")
        data = response.json()
        author_name = data.get("name", author_name)
        print(author_name)

    except Exception as e:
        print("Failed to fetch author name from GitHub API")

if not release_notes:
    release_notes = f"No release notes provided."
    # get last commit message from github api if not provided
    gh_username = 'mononsoft'
    repo_owner = 'mononsoft'
    repo_name = 'jerp-frontend'

    try:
        # GitHub API URL for the repository's commits on a specific branch
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits?sha={branch_name}'

        # Make a request to the GitHub API
        response = requests.get(url, auth=(gh_username, token))

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            commits = response.json()
            if commits:
                # Get the last commit message
                last_commit = commits[0]['commit']['message']
                print(f'Last commit message on branch "{branch_name}": {last_commit}')
            else:
                print(f'No commits found on branch "{branch_name}".')
        else:
            print(f'Failed to fetch commits. Status code: {response.status_code}')
    except Exception as e:
        print("Failed to fetch author name from GitHub API")

note = "📝 **N.B.:** This message is automatically generated by the CI/CD pipeline. 🚀"
# Create the message to be sent
message = f"""🎉 **New Release Deployed!**

-------------------

📝 **Release Notes:**
{release_notes} 
Last Commit: {last_commit}

👤 **Released By:** {author_name}

🌿 **Branch Name:** {branch_name}

🧑‍💻 **Origin:** {origin}

-------------------

{note}

Best regards
Frontend Team"""

error_message = f"""🚨 **Deployment Alert!**

-------------------

❌ **Build Failed**

👤 **Triggered By:** {author_name}

🌿 **Branch Name:** {branch_name}

🧑‍💻 **Origin:** {origin}

📄 **Error Details:**
https://github.com/mononsoft/jerp-frontend/actions/runs/{github_run_id}

-------------------

Please address the issue as soon as possible.

{note}
Thank you! 🙏"""

cancelled_message = f"""🛑 **Deployment Cancelled**

-------------------

❌ **Build Cancelled**

👤 **Triggered By:** {author_name}

🌿 **Branch Name:** {branch_name}

🧑‍💻 **Origin:** {origin}

📄 **Job Details:**
https://github.com/mononsoft/jerp-frontend/actions/runs/{github_run_id}

-------------------

The deployment process was cancelled.

{note}
Thank you! 🙏"""

if build_result == "failure":
    message = error_message
elif build_result == "cancelled":
    message = cancelled_message

try:
    # Initialize the Skype instance
    skype = Skype(skype_username, skype_password)
    # Define the Skype recipient and group IDs
    group_id = "19:1e55bc9219844d01a3b27253a2f78652@thread.skype"
    # Send the message to the group
    chat = skype.chats.chat(group_id)
    chat.sendMsg(message)
    print(message)

except Exception as e:
    print(f"Failed to send message: {e}")