import os
import requests

from dotenv import load_dotenv

load_dotenv()

print(os.getenv("DISCORD_WEBHOOK_URL"))

headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": os.getenv("PERSONAL_ACCESS_TOKEN"),
}

req = requests.get(" https://api.github.com/repos/ayutaz/UnityBuildNotificationToDiscord/actions/artifacts",
                   headers=headers).json()


def get_download_url(content):
    for artifact in content["artifacts"]:
        if artifact["name"] == "Build-StandaloneWindows64":
            run_id = artifact["workflow_run"]["id"]
            url = f"https://github.com/ayutaz/UnityBuildNotificationToDiscord/actions/runs/{run_id}"
            return url
    return None


def message(url):
    content = {
        "username": "ビルドダウンロードページ",
        "content": "ビルドが終了しました。"
                   + f"\nダウンロードページ: {url}"
    }
    return content


requests.post(os.getenv("DISCORD_WEBHOOK_URL"), message(get_download_url(req)))
