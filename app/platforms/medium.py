import httpx
from app.config import settings
from app.platforms.base import BasePlatform


class MediumPlatform(BasePlatform):
    name = "Medium"

    def post(self, message: str) -> dict:
        if not settings.medium_access_token:
            return self._result("failed", error="MEDIUM_ACCESS_TOKEN not configured")
        try:
            with httpx.Client(timeout=20) as client:
                me = client.get(
                    "https://api.medium.com/v1/me",
                    headers={"Authorization": f"Bearer {settings.medium_access_token}"},
                )
                if me.status_code != 200:
                    return self._result("failed", error=f"Medium auth failed ({me.status_code})")
                user_id = me.json().get("data", {}).get("id")
                resp = client.post(
                    f"https://api.medium.com/v1/users/{user_id}/posts",
                    headers={"Authorization": f"Bearer {settings.medium_access_token}",
                             "Content-Type": "application/json"},
                    json={"title": message[:200], "contentFormat": "markdown",
                          "content": message, "publishStatus": "public"},
                )
            if resp.status_code in (200, 201):
                data = resp.json().get("data", {})
                return self._result("success", posted_url=data.get("url"), public_access=True)
            return self._result("failed", error=f"Medium API error {resp.status_code}: {resp.text[:200]}")
        except Exception as exc:
            return self._result("failed", error=str(exc))
