
import asyncio
import json
from TikTokLive import TikTokLiveClient

ACCOUNTS = {
    "synergy.rce": "owner",
    "skid.mark007": "admin"
}

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
        result = await check_account(username, role)
        results.append(result)

    print(json.dumps({
        "streamers": results
    }, indent=2))

if __name__ == "__main__":
    asyncio.run(main())

