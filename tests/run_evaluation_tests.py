from crawler.crawler import crawl_page
from analyzer.relevance_analyzer import analyze_relevance
from analyzer.llm_evaluator import (
    build_evaluation_payload,
    evaluate_with_llm,
)
from tests.test_cases import get_test_cases


# -------------------------------------------------
# Score classification
# -------------------------------------------------

def classify_score(score):
    """
    Convert a numerical score into a simple
    Low / Medium / High classification.
    """

    if score >= 70:
        return "high"

    if score >= 40:
        return "medium"

    return "low"


# -------------------------------------------------
# Compare actual result with expected result
# -------------------------------------------------

def check_expectation(
    dimension,
    actual_score,
    expected_level,
):
    """
    Check whether the actual score falls into
    the expected score category.
    """

    actual_level = classify_score(
        actual_score
    )

    passed = (
        actual_level == expected_level
    )

    return {
        "dimension": dimension,
        "score": actual_score,
        "actual_level": actual_level,
        "expected_level": expected_level,
        "passed": passed,
    }


# -------------------------------------------------
# Run one test case
# -------------------------------------------------

def run_test_case(test_case):
    """
    Run one controlled AdAlign AI evaluation.
    """

    print(
        f"\n{'=' * 70}"
    )

    print(
        f'TEST: {test_case["name"]}'
    )

    print(
        f"{'=' * 70}"
    )

    print(
        f'Keyword: {test_case["keyword"]}'
    )

    print(
        f'Headline: {test_case["ad_headline"]}'
    )

    print(
        f'URL: {test_case["url"]}'
    )

    print("\nCrawling landing page...")

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

    print(
        "Building grounded evidence..."
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

    print(
        "Calling OpenAI evaluator..."
    )

    llm_result = evaluate_with_llm(
        payload
    )

    test_results = []

    print(
        "\n--- EXPECTATION CHECK ---"
    )

    for dimension, expected_level in (
        test_case["expected"].items()
    ):

        dimension_result = (
            llm_result.get(
                dimension,
                {},
            )
        )

        actual_score = (
            dimension_result.get(
                "score",
                0,
            )
        )

        result = check_expectation(
            dimension=dimension,
            actual_score=actual_score,
            expected_level=expected_level,
        )

        test_results.append(
            result
        )

        status = (
            "PASS"
            if result["passed"]
            else "FAIL"
        )

        readable_dimension = (
            dimension
            .replace("_", " ")
            .title()
        )

        print(
            f"\n{readable_dimension}"
        )

        print(
            f"Score: "
            f'{result["score"]}/100'
        )

        print(
            f"Expected: "
            f'{result["expected_level"].upper()}'
        )

        print(
            f"Actual: "
            f'{result["actual_level"].upper()}'
        )

        print(
            f"Result: {status}"
        )

    return {
        "id": test_case["id"],
        "name": test_case["name"],
        "results": test_results,
        "llm_result": llm_result,
    }


# -------------------------------------------------
# Run all controlled tests
# -------------------------------------------------

def run_all_tests():

    test_cases = get_test_cases()

    all_results = []

    print(
        "\n"
        "========================================\n"
        "   ADALIGN AI — EVALUATION TEST SUITE\n"
        "========================================"
    )

    for test_case in test_cases:

        try:

            result = run_test_case(
                test_case
            )

            all_results.append(
                result
            )

        except Exception as error:

            print(
                "\nTEST ERROR:"
            )

            print(
                error
            )

            all_results.append(
                {
                    "id": test_case["id"],
                    "name": test_case["name"],
                    "results": [],
                    "error": str(error),
                }
            )

    # ---------------------------------------------
    # Final summary
    # ---------------------------------------------

    print(
        "\n\n"
        "========================================\n"
        "   ADALIGN AI — TEST SUMMARY\n"
        "========================================"
    )

    total_checks = 0
    passed_checks = 0

    for test_result in all_results:

        print(
            f'\n{test_result["name"]}'
        )

        if "error" in test_result:

            print(
                f'ERROR: {test_result["error"]}'
            )

            continue

        for result in test_result[
            "results"
        ]:

            total_checks += 1

            if result["passed"]:
                passed_checks += 1

            status = (
                "PASS"
                if result["passed"]
                else "FAIL"
            )

            readable_dimension = (
                result["dimension"]
                .replace("_", " ")
                .title()
            )

            print(
                f"  {readable_dimension}: "
                f'{result["score"]}/100 '
                f"→ {status}"
            )

    failed_checks = (
        total_checks - passed_checks
    )

    print(
        "\n----------------------------------------"
    )

    print(
        f"Checks passed: "
        f"{passed_checks}/{total_checks}"
    )

    print(
        f"Checks failed: "
        f"{failed_checks}/{total_checks}"
    )

    print(
        "----------------------------------------"
    )

    return all_results


# -------------------------------------------------
# Entry point
# -------------------------------------------------

if __name__ == "__main__":

    run_all_tests()