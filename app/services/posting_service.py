from app.platforms.twitter import TwitterPlatform
from app.platforms.linkedin import LinkedInPlatform
from app.platforms.facebook import FacebookPlatform
from app.platforms.instagram import InstagramPlatform
from app.platforms.reddit import RedditPlatform
from app.platforms.telegram import TelegramPlatform
from app.platforms.devto import DevToPlatform
from app.platforms.medium import MediumPlatform


PLATFORMS = [
    TwitterPlatform(),
    LinkedInPlatform(),
    FacebookPlatform(),
    InstagramPlatform(),
    RedditPlatform(),
    TelegramPlatform(),
    DevToPlatform(),
    MediumPlatform(),
]


def post_to_all_platforms(message: str) -> list:
    """Post the message to every platform independently. Failures don't stop
    others."""
    results = []
    for platform in PLATFORMS:
        try:
            result = platform.post(message)
        except Exception as exc:
            result = {
                "platform": platform.name,
                "status": "failed",
                "posted_url": None,
                "public_access": False,
                "error": str(exc),
            }
        results.append(result)
    return results
