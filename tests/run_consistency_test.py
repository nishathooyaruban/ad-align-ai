from statistics import mean

from crawler.crawler import crawl_page
from analyzer.relevance_analyzer import analyze_relevance
from analyzer.llm_evaluator import (
    build_evaluation_payload,
    evaluate_with_llm,
)
from tests.test_cases import get_test_cases


NUMBER_OF_RUNS = 3

DIMENSIONS = [
    "message_match",
    "search_intent_match",
    "offer_relevance",
    "cta_strength",
    "trust_credibility",
    "conversion_readiness",
]


def get_strong_match_case():
    """
    Get the strong-match controlled test case.
    """

    test_cases = get_test_cases()

    for test_case in test_cases:
        if test_case["id"] == "strong_match":
            return test_case

    raise ValueError(
        "Strong-match test case was not found."
    )


def prepare_evidence(test_case):
    """
    Crawl the page once and build the evidence payload.

    We intentionally reuse exactly the same payload
    for every LLM run so that only the LLM evaluation
    is being tested for consistency.
    """

    print("\nCrawling landing page once...")

    page_data = crawl_page(
        test_case["url"]
    )

    deterministic_analysis = analyze_relevance(
        keyword=test_case["keyword"],
        ad_headline=test_case["ad_headline"],
        ad_description=test_case[
            "ad_description"
        ],
        page_data=page_data,
    )

    payload = build_evaluation_payload(
        keyword=test_case["keyword"],
        ad_headline=test_case["ad_headline"],
        ad_description=test_case[
            "ad_description"
        ],
        page_data=page_data,
        deterministic_analysis=(
            deterministic_analysis
        ),
    )

    return payload


def run_consistency_test():
    """
    Evaluate the exact same evidence several times
    and measure score variation.
    """

    test_case = get_strong_match_case()

    print(
        "\n"
        "========================================\n"
        "   ADALIGN AI — CONSISTENCY TEST\n"
        "========================================"
    )

    print(
        f'\nTest case: {test_case["name"]}'
    )

    print(
        f"Number of runs: {NUMBER_OF_RUNS}"
    )

    payload = prepare_evidence(
        test_case
    )

    scores = {
        dimension: []
        for dimension in DIMENSIONS
    }

    for run_number in range(
        1,
        NUMBER_OF_RUNS + 1,
    ):

        print(
            f"\n--- RUN "
            f"{run_number}/{NUMBER_OF_RUNS} ---"
        )

        try:
            result = evaluate_with_llm(
                payload
            )

        except Exception as error:
            print(
                f"Run {run_number} failed:"
            )
            print(error)
            continue

        for dimension in DIMENSIONS:

            score = result.get(
                dimension,
                {},
            ).get(
                "score",
                0,
            )

            scores[dimension].append(
                score
            )

            readable_name = (
                dimension
                .replace("_", " ")
                .title()
            )

            print(
                f"{readable_name}: "
                f"{score}/100"
            )

    print(
        "\n\n"
        "========================================\n"
        "   CONSISTENCY RESULTS\n"
        "========================================"
    )

    for dimension in DIMENSIONS:

        dimension_scores = scores[
            dimension
        ]

        readable_name = (
            dimension
            .replace("_", " ")
            .title()
        )

        print(
            f"\n{readable_name}"
        )

        if not dimension_scores:
            print(
                "No successful evaluations."
            )
            continue

        minimum_score = min(
            dimension_scores
        )

        maximum_score = max(
            dimension_scores
        )

        average_score = mean(
            dimension_scores
        )

        variation = (
            maximum_score
            - minimum_score
        )

        print(
            f"Scores: {dimension_scores}"
        )

        print(
            f"Average: "
            f"{average_score:.2f}"
        )

        print(
            f"Minimum: "
            f"{minimum_score}"
        )

        print(
            f"Maximum: "
            f"{maximum_score}"
        )

        print(
            f"Variation: "
            f"{variation} points"
        )

        if variation <= 5:
            stability = "GOOD"

        elif variation <= 10:
            stability = "MODERATE"

        else:
            stability = "HIGH VARIATION"

        print(
            f"Stability: {stability}"
        )


if __name__ == "__main__":
    run_consistency_test()