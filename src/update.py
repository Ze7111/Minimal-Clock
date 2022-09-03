import requests

# Get the latest version of this program from GitHub
def getLatestVersion():
    # Get the latest release from GitHub
    latestRelease = requests.get('https://api.github.com/repos/ze7111//releases/latest').json()
    # Get the latest version from the latest release
    latestVersion = latestRelease['tag_name']
    # Return the latest version
    return latestVersion

print(getLatestVersion())