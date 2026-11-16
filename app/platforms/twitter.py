import httpx
from app.config import settings
from app.platforms.base import BasePlatform


class TwitterPlatform(BasePlatform):
    name = "Twitter (X)"

    def post(self, message: str) -> dict:
        if not settings.twitter_bearer_token:
            return self._result("failed", error="TWITTER_BEARER_TOKEN not configured")
        try:
            with httpx.Client(timeout=20) as client:
                resp = client.post(
                    "https://api.twitter.com/2/tweets",
                    headers={"Authorization": f"Bearer {settings.twitter_bearer_token}",
                             "Content-Type": "application/json"},
                    json={"text": message},
                )
            if resp.status_code in (200, 201):
                data = resp.json()
                tweet_id = data.get("data", {}).get("id")
                return self._result("success", posted_url=f"https://twitter.com/i/web/status/{tweet_id}" if tweet_id else None, public_access=True)
            return self._result("failed", error=f"Twitter API error {resp.status_code}: {resp.text[:200]}")
        except Exception as exc:
            return self._result("failed", error=str(exc))
