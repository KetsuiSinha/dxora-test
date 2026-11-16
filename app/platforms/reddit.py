import httpx
from app.config import settings
from app.platforms.base import BasePlatform


class RedditPlatform(BasePlatform):
    name = "Reddit"

    def post(self, message: str) -> dict:
        if not all([settings.reddit_client_id, settings.reddit_client_secret,
                    settings.reddit_username, settings.reddit_password]):
            return self._result("failed", error="Reddit credentials not fully configured")
        try:
            with httpx.Client(timeout=20) as client:
                auth = client.post(
                    "https://www.reddit.com/api/v1/access_token",
                    data={"grant_type": "password", "username": settings.reddit_username,
                          "password": settings.reddit_password},
                    auth=(settings.reddit_client_id, settings.reddit_client_secret),
                    headers={"User-Agent": settings.reddit_user_agent},
                )
                if auth.status_code != 200:
                    return self._result("failed", error=f"Reddit auth failed ({auth.status_code})")
                token = auth.json().get("access_token")
                resp = client.post(
                    "https://oauth.reddit.com/api/submit",
                    headers={"Authorization": f"Bearer {token}", "User-Agent": settings.reddit_user_agent},
                    data={"kind": "self", "sr": "all", "title": message[:299], "text": message, "resubmit": "true"},
                )
            if resp.status_code in (200, 201, 302):
                return self._result("success", posted_url="https://reddit.com", public_access=True)
            return self._result("failed", error=f"Reddit API error {resp.status_code}: {resp.text[:200]}")
        except Exception as exc:
            return self._result("failed", error=str(exc))
