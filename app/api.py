from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from crawler.crawler import crawl_page
from analyzer.relevance_analyzer import analyze_relevance
from analyzer.llm_evaluator import (
    build_evaluation_payload,
    evaluate_with_llm,
)


app = FastAPI(
    title="AdAlign AI API",
    description=(
        "API for evaluating alignment between Google Ads assets "
        "and landing-page content."
    ),
    version="1.0.0",
)


BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "templates" / "index.html"


class AnalyzeRequest(BaseModel):
    """
    Request model for AdAlign AI analysis.
    """

    url: str = Field(
        ...,
        description="Landing page URL",
    )

    keyword: str = Field(
        ...,
        description="Target Google Ads keyword",
    )

    headlines: List[str] = Field(
        ...,
        description="Google Ads headline assets",
    )

    descriptions: List[str] = Field(
        ...,
        description="Google Ads description assets",
    )


@app.get("/")
def root():
    """
    Serve the AdAlign AI web interface.
    """

    if not INDEX_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail="Web interface file was not found.",
        )

    return FileResponse(
        INDEX_FILE
    )


@app.get("/health")
def health_check():
    """
    Health endpoint used to confirm that
    the backend service is available.
    """

    return {
        "status": "healthy"
    }


@app.post("/analyze")
def analyze_ads(request: AnalyzeRequest):
    """
    Run the full AdAlign AI evaluation pipeline.
    """

    url = request.url.strip()
    keyword = request.keyword.strip()

    headlines = [
        headline.strip()
        for headline in request.headlines
        if headline.strip()
    ]

    descriptions = [
        description.strip()
        for description in request.descriptions
        if description.strip()
    ]

    if not url:
        raise HTTPException(
            status_code=400,
            detail="Landing page URL is required.",
        )

    if not keyword:
        raise HTTPException(
            status_code=400,
            detail="Target keyword is required.",
        )

    if not headlines:
        raise HTTPException(
            status_code=400,
            detail=(
                "At least one Google Ads headline "
                "is required."
            ),
        )

    if not descriptions:
        raise HTTPException(
            status_code=400,
            detail=(
                "At least one Google Ads description "
                "is required."
            ),
        )

    try:
        page_data = crawl_page(
            url
        )

        deterministic_analysis = analyze_relevance(
            keyword=keyword,
            ad_headlines=headlines,
            ad_descriptions=descriptions,
            page_data=page_data,
        )

        payload = build_evaluation_payload(
            keyword=keyword,
            ad_headlines=headlines,
            ad_descriptions=descriptions,
            page_data=page_data,
            deterministic_analysis=(
                deterministic_analysis
            ),
        )

        llm_evaluation = evaluate_with_llm(
            payload
        )

        return {
            "status": "success",
            "input": {
                "url": url,
                "keyword": keyword,
                "headlines": headlines,
                "descriptions": descriptions,
            },
            "landing_page": {
                "title": page_data.get(
                    "title",
                    "",
                ),
                "meta_description": page_data.get(
                    "meta_description",
                    "",
                ),
            },
            "deterministic_analysis": (
                deterministic_analysis
            ),
            "evaluation": (
                llm_evaluation
            ),
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error