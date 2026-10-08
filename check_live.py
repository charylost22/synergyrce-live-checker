
import asyncio
import json
import os
import urllib.request
from TikTokLive import TikTokLiveClient

ACCOUNTS = {
    "synergy.rce": "owner",
    "skid.mark007": "admin"
}

WORKER_URL = (
    "https://synergyrce-live-status.charroe21.workers.dev/update"
)

async def check_account(username, role):
    client = TikTokLiveClient(unique_id=f"@{username}")

    try:
        live = await client.is_live()
        status = "live" if live else "offline"
    except Exception as error:
        print(f"Error checking {username}: {error}")
        status = "unknown"

    return {
        "username": username,
        "role": role,
        "status": status
    }

async def main():
    results = []

    for username, role in ACCOUNTS.items():
        results.append(await check_account(username, role))

    payload = {"streamers": results}
    print(json.dumps(payload, indent=2))

    token = os.environ.get("CLOUDFLARE_LIVE_TOKEN")
    if not token:
        raise RuntimeError("Missing CLOUDFLARE_LIVE_TOKEN")

    request = urllib.request.Request(
        WORKER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        print("Cloudflare update:", response.status)
        print(response.read().decode())

if __name__ == "__main__":
    asyncio.run(main())
