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


def readable_name(name):
    """
    Convert snake_case names into readable names.
    """

    return name.replace(
        "_",
        " ",
    ).title()


def get_strong_match_case():
    """
    Return the controlled strong-match test case.
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
    Crawl the landing page once and build one fixed
    evidence payload.

    Every LLM run receives exactly the same payload.
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


def classify_stability(variation):
    """
    Classify score variation using provisional
    development thresholds.
    """

    if variation <= 5:
        return "GOOD"

    if variation <= 10:
        return "MODERATE"

    return "HIGH VARIATION"


def calculate_statistics(scores):
    """
    Calculate simple consistency statistics.
    """

    minimum_score = min(scores)
    maximum_score = max(scores)

    average_score = mean(
        scores
    )

    variation = (
        maximum_score
        - minimum_score
    )

    return {
        "average": average_score,
        "minimum": minimum_score,
        "maximum": maximum_score,
        "variation": variation,
        "stability": classify_stability(
            variation
        ),
    }


def run_consistency_test():
    """
    Run the same grounded evidence several times.

    Measure both:

    1. Dimension-level consistency
    2. Criterion-level consistency
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

    dimension_scores = {
        dimension: []
        for dimension in DIMENSIONS
    }

    criterion_scores = {
        dimension: {}
        for dimension in DIMENSIONS
    }

    successful_runs = 0

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

        successful_runs += 1

        for dimension in DIMENSIONS:

            dimension_result = result.get(
                dimension,
                {},
            )

            score = dimension_result.get(
                "score",
                0,
            )

            dimension_scores[
                dimension
            ].append(
                score
            )

            print(
                f"{readable_name(dimension)}: "
                f"{score}/100"
            )

            criteria = dimension_result.get(
                "criteria",
                {},
            )

            for (
                criterion_name,
                criterion_result,
            ) in criteria.items():

                points = criterion_result.get(
                    "points_awarded",
                    0,
                )

                max_points = criterion_result.get(
                    "max_points",
                    0,
                )

                if criterion_name not in (
                    criterion_scores[
                        dimension
                    ]
                ):

                    criterion_scores[
                        dimension
                    ][criterion_name] = {
                        "scores": [],
                        "max_points": max_points,
                    }

                criterion_scores[
                    dimension
                ][criterion_name][
                    "scores"
                ].append(
                    points
                )

    print(
        "\n\n"
        "========================================\n"
        "   DIMENSION CONSISTENCY RESULTS\n"
        "========================================"
    )

    for dimension in DIMENSIONS:

        scores = dimension_scores[
            dimension
        ]

        print(
            f"\n{readable_name(dimension)}"
        )

        if not scores:

            print(
                "No successful evaluations."
            )

            continue

        statistics = calculate_statistics(
            scores
        )

        print(
            f"Scores: {scores}"
        )

        print(
            f'Average: '
            f'{statistics["average"]:.2f}'
        )

        print(
            f'Minimum: '
            f'{statistics["minimum"]}'
        )

        print(
            f'Maximum: '
            f'{statistics["maximum"]}'
        )

        print(
            f'Variation: '
            f'{statistics["variation"]} points'
        )

        print(
            f'Stability: '
            f'{statistics["stability"]}'
        )

    print(
        "\n\n"
        "========================================\n"
        "   CRITERION CONSISTENCY RESULTS\n"
        "========================================"
    )

    unstable_criteria = []

    for dimension in DIMENSIONS:

        print(
            f"\n{'=' * 60}"
        )

        print(
            readable_name(
                dimension
            ).upper()
        )

        print(
            f"{'=' * 60}"
        )

        criteria = criterion_scores[
            dimension
        ]

        if not criteria:

            print(
                "No criterion results."
            )

            continue

        for (
            criterion_name,
            criterion_data,
        ) in criteria.items():

            scores = criterion_data[
                "scores"
            ]

            max_points = criterion_data[
                "max_points"
            ]

            statistics = (
                calculate_statistics(
                    scores
                )
            )

            print(
                f"\n"
                f"{readable_name(criterion_name)}"
            )

            print(
                f"Scores: {scores}"
            )

            print(
                f"Maximum possible: "
                f"{max_points}"
            )

            print(
                f"Average: "
                f'{statistics["average"]:.2f}'
            )

            print(
                f"Variation: "
                f'{statistics["variation"]} points'
            )

            print(
                f"Stability: "
                f'{statistics["stability"]}'
            )

            if (
                statistics["variation"]
                > 5
            ):

                unstable_criteria.append(
                    {
                        "dimension": dimension,
                        "criterion": (
                            criterion_name
                        ),
                        "scores": scores,
                        "variation": (
                            statistics[
                                "variation"
                            ]
                        ),
                        "stability": (
                            statistics[
                                "stability"
                            ]
                        ),
                    }
                )

    print(
        "\n\n"
        "========================================\n"
        "   CONSISTENCY DIAGNOSTIC SUMMARY\n"
        "========================================"
    )

    print(
        f"\nSuccessful runs: "
        f"{successful_runs}/"
        f"{NUMBER_OF_RUNS}"
    )

    if not unstable_criteria:

        print(
            "\nNo criterion exceeded "
            "5 points of variation."
        )

    else:

        print(
            "\nCriteria requiring review:"
        )

        for item in unstable_criteria:

            print(
                "\n"
                f"- "
                f'{readable_name(item["dimension"])}'
                f" → "
                f'{readable_name(item["criterion"])}'
            )

            print(
                f'  Scores: {item["scores"]}'
            )

            print(
                f'  Variation: '
                f'{item["variation"]} points'
            )

            print(
                f'  Stability: '
                f'{item["stability"]}'
            )


if __name__ == "__main__":

    run_consistency_test()