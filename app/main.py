import json

from crawler.crawler import crawl_page
from analyzer.relevance_analyzer import analyze_relevance
from analyzer.llm_evaluator import (
    build_evaluation_payload,
    evaluate_with_llm,
)


# -------------------------------------------------
# 1. Test Google Ad
# -------------------------------------------------

url = "https://ceylonempiretravels.com/"

keyword = "Sri Lanka tour packages"

ad_headline = "Best Sri Lanka Tour Packages"

ad_description = (
    "Custom private tours with experienced local guides. "
    "Get a free quote today."
)


# -------------------------------------------------
# 2. Crawl Landing Page
# -------------------------------------------------

print("\nCrawling landing page...")

page_data = crawl_page(url)


# -------------------------------------------------
# 3. Deterministic Analysis
# -------------------------------------------------

analysis = analyze_relevance(
    keyword=keyword,
    ad_headline=ad_headline,
    ad_description=ad_description,
    page_data=page_data,
)

print("\n=== ADALIGN AI — DETERMINISTIC ANALYSIS ===")

print("\nKEYWORD:")
print(analysis["keyword"])

print("\nKEYWORD FOUND ON PAGE:")
print(analysis["keyword_found_on_page"])

print("\nMESSAGE MATCH SCORE:")
print(f'{analysis["message_match_score"]}/100')

print("\nAD DESCRIPTION MATCH SCORE:")
print(f'{analysis["description_match_score"]}/100')


# -------------------------------------------------
# 4. Build Grounded Evidence
# -------------------------------------------------

evaluation_payload = build_evaluation_payload(
    keyword=keyword,
    ad_headline=ad_headline,
    ad_description=ad_description,
    page_data=page_data,
    deterministic_analysis=analysis,
)


# -------------------------------------------------
# 5. Call LLM
# -------------------------------------------------

print("\nCalling OpenAI evaluator...")

try:
    llm_result = evaluate_with_llm(
        evaluation_payload
    )

except Exception as error:
    print("\n=== LLM EVALUATION ERROR ===")
    print(error)
    raise SystemExit(1)


# -------------------------------------------------
# 6. Display Rubric-Based Results
# -------------------------------------------------

print("\n=== ADALIGN AI — RUBRIC-BASED EVALUATION ===")


for dimension_key, dimension_result in llm_result.items():

    dimension_name = dimension_result.get(
        "name",
        dimension_key.replace("_", " ").title(),
    )

    dimension_score = dimension_result.get(
        "score",
        0,
    )

    print(
        f"\n{'=' * 60}"
    )

    print(
        f"{dimension_name.upper()} — "
        f"{dimension_score}/100"
    )

    print(
        f"{'=' * 60}"
    )

    criteria = dimension_result.get(
        "criteria",
        {},
    )

    for criterion_key, criterion_result in criteria.items():

        criterion_name = criterion_key.replace(
            "_",
            " ",
        ).title()

        points_awarded = criterion_result.get(
            "points_awarded",
            0,
        )

        max_points = criterion_result.get(
            "max_points",
            0,
        )

        reason = criterion_result.get(
            "reason",
            "",
        )

        evidence = criterion_result.get(
            "evidence",
            [],
        )

        print(
            f"\n{criterion_name}: "
            f"{points_awarded}/{max_points}"
        )

        print(
            f"Reason: {reason}"
        )

        print("Evidence:")

        if evidence:

            for item in evidence:
                print(
                    f"  - {item}"
                )

        else:
            print(
                "  - No supporting evidence provided."
            )

    print("\nOVERALL EXPLANATION:")

    print(
        dimension_result.get(
            "explanation",
            "",
        )
    )

    print("\nRECOMMENDATION:")

    print(
        dimension_result.get(
            "recommendation",
            "",
        )
    )


# -------------------------------------------------
# 7. Score Summary
# -------------------------------------------------

print(
    "\n\n=== ADALIGN AI — SCORE SUMMARY ==="
)

for dimension_key, dimension_result in llm_result.items():

    dimension_name = dimension_result.get(
        "name",
        dimension_key.replace("_", " ").title(),
    )

    score = dimension_result.get(
        "score",
        0,
    )

    print(
        f"{dimension_name}: {score}/100"
    )


# -------------------------------------------------
# 8. Raw Structured JSON
# -------------------------------------------------

print(
    "\n=== RAW STRUCTURED RESULT ==="
)

print(
    json.dumps(
        llm_result,
        indent=2,
        ensure_ascii=False,
    )
)