import httpx
from app.config import settings
from app.platforms.base import BasePlatform


class DevToPlatform(BasePlatform):
    name = "Dev.to"

    def post(self, message: str) -> dict:
        if not settings.devto_api_key:
            return self._result("failed", error="DEVTO_API_KEY not configured")
        try:
            with httpx.Client(timeout=20) as client:
                resp = client.post(
                    "https://dev.to/api/articles",
                    headers={"api-key": settings.devto_api_key, "Content-Type": "application/json"},
                    json={"article": {"title": message[:200], "published": True, "body_markdown": message}},
                )
            if resp.status_code in (200, 201):
                data = resp.json()
                return self._result("success", posted_url=data.get("url"), public_access=True)
            return self._result("failed", error=f"Dev.to API error {resp.status_code}: {resp.text[:200]}")
        except Exception as exc:
            return self._result("failed", error=str(exc))
