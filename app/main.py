from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.schemas import PostingRequest, PostingResponse, ErrorResponse
from app.services.posting_service import post_to_all_platforms


app = FastAPI(
    title="Dxora Test - Automated Multi-Platform Posting System",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "service": "Dxora Automated Multi-Platform Posting System",
        "endpoints": {
            "posting": "POST /posting",
        },
        "docs": "/docs",
    }


@app.post("/posting", response_model=PostingResponse)
def posting(request: PostingRequest):
    """Post a message to multiple third-party platforms independently."""
    results = post_to_all_platforms(request.message)
    return {"success": True, "results": results}
