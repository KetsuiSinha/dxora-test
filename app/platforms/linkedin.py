import httpx
from app.config import settings
from app.platforms.base import BasePlatform


class LinkedInPlatform(BasePlatform):
    name = "LinkedIn"

    def post(self, message: str) -> dict:
        if not settings.linkedin_access_token:
            return self._result("failed", error="LINKEDIN_ACCESS_TOKEN not configured")
        try:
            with httpx.Client(timeout=20) as client:
                me = client.get(
                    "https://api.linkedin.com/v2/me",
                    headers={"Authorization": f"Bearer {settings.linkedin_access_token}"},
                )
                if me.status_code != 200:
                    return self._result("failed", error=f"LinkedIn auth failed ({me.status_code})")
                person_id = me.json().get("id")
                urn = f"urn:li:person:{person_id}"
                payload = {
                    "author": urn,
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {"text": message},
                            "shareMediaCategory": "NONE",
                        }
                    },
                    "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"},
                }
                resp = client.post(
                    "https://api.linkedin.com/v2/ugcPosts",
                    headers={"Authorization": f"Bearer {settings.linkedin_access_token}",
                             "Content-Type": "application/json"},
                    json=payload,
                )
            if resp.status_code in (200, 201):
                return self._result("success", posted_url="https://www.linkedin.com/feed/", public_access=True)
            return self._result("failed", error=f"LinkedIn API error {resp.status_code}: {resp.text[:200]}")
        except Exception as exc:
            return self._result("failed", error=str(exc))
