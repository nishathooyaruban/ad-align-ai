import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from analyzer.scoring_rubric import get_scoring_rubric


load_dotenv()


SYSTEM_PROMPT = """
You are the evaluation engine for AdAlign AI.

AdAlign AI evaluates alignment between:

1. A Google Ads keyword
2. Google Ads copy
3. The actual landing page

You MUST evaluate using only the supplied landing-page
evidence and scoring rubric.

GROUNDING RULES:

- Do not invent page content.
- Do not assume evidence exists when it is not supplied.
- Do not use outside knowledge about the company.
- Treat business claims as claims, not independently
  verified facts.
- If evidence is insufficient, explicitly say so.
- Do not choose an overall score independently.
- Score each rubric criterion separately.
- Never award more than the criterion's maximum points.
- The dimension score MUST equal the sum of its
  criterion scores.

Conversion Readiness measures whether the supplied
landing-page evidence supports a visitor taking the
desired action.

It is NOT a prediction of actual conversion rate.

Return valid JSON only.
"""


def build_evaluation_payload(
    keyword,
    ad_headline,
    ad_description,
    page_data,
    deterministic_analysis,
):
    """
    Build the grounded evidence package supplied
    to the LLM.
    """

    payload = {
        "advertisement": {
            "keyword": keyword,
            "headline": ad_headline,
            "description": ad_description,
        },

        "landing_page": {
            "url": page_data.get("url", ""),
            "title": page_data.get("title", ""),
            "meta_description": page_data.get(
                "meta_description",
                "",
            ),
            "headings": page_data.get(
                "headings",
                {},
            ),
            "paragraphs": page_data.get(
                "paragraphs",
                [],
            ),
            "links": page_data.get(
                "links",
                [],
            ),
            "buttons": page_data.get(
                "buttons",
                [],
            ),
            "form_count": page_data.get(
                "form_count",
                0,
            ),
            "image_count": page_data.get(
                "image_count",
                0,
            ),
            "images_with_alt": page_data.get(
                "images_with_alt",
                [],
            ),
        },

        "deterministic_evidence": {
            "keyword_found_on_page":
                deterministic_analysis.get(
                    "keyword_found_on_page",
                    False,
                ),

            "matched_headline_words":
                deterministic_analysis.get(
                    "matched_headline_words",
                    [],
                ),

            "message_match_score":
                deterministic_analysis.get(
                    "message_match_score",
                    0,
                ),

            "matched_description_words":
                deterministic_analysis.get(
                    "matched_description_words",
                    [],
                ),

            "description_match_score":
                deterministic_analysis.get(
                    "description_match_score",
                    0,
                ),
        },
    }

    return payload


def build_user_prompt(payload):
    """
    Build the grounded evaluation prompt including
    the AdAlign AI scoring rubric.
    """

    rubric = get_scoring_rubric()

    evidence_json = json.dumps(
        payload,
        indent=2,
        ensure_ascii=False,
    )

    rubric_json = json.dumps(
        rubric,
        indent=2,
        ensure_ascii=False,
    )

    return f"""
Evaluate this Google Ad and landing page.

Use ONLY the supplied evidence and scoring rubric.

SCORING RUBRIC:

{rubric_json}

LANDING PAGE EVIDENCE:

{evidence_json}

For every criterion:

1. Give "points_awarded".
2. Give "max_points".
3. Explain why those points were awarded.
4. Provide evidence from the supplied data.

The overall score for each dimension must equal the
sum of its criterion points.

Return JSON using this structure:

{{
    "message_match": {{
        "criteria": {{
            "keyword_alignment": {{
                "points_awarded": 0,
                "max_points": 25,
                "reason": "",
                "evidence": []
            }},
            "headline_alignment": {{
                "points_awarded": 0,
                "max_points": 25,
                "reason": "",
                "evidence": []
            }},
            "ad_description_alignment": {{
                "points_awarded": 0,
                "max_points": 25,
                "reason": "",
                "evidence": []
            }},
            "promise_consistency": {{
                "points_awarded": 0,
                "max_points": 25,
                "reason": "",
                "evidence": []
            }}
        }},
        "score": 0,
        "explanation": "",
        "recommendation": ""
    }},

    "search_intent_match": {{
        "criteria": {{}},
        "score": 0,
        "explanation": "",
        "recommendation": ""
    }},

    "offer_relevance": {{
        "criteria": {{}},
        "score": 0,
        "explanation": "",
        "recommendation": ""
    }},

    "cta_strength": {{
        "criteria": {{}},
        "score": 0,
        "explanation": "",
        "recommendation": ""
    }},

    "trust_credibility": {{
        "criteria": {{}},
        "score": 0,
        "explanation": "",
        "recommendation": ""
    }},

    "conversion_readiness": {{
        "criteria": {{}},
        "score": 0,
        "explanation": "",
        "recommendation": ""
    }}
}}
"""


def validate_llm_evaluation(evaluation):
    """
    Validate the LLM output against the scoring rubric
    and calculate final scores ourselves.

    The LLM does NOT get final authority over the
    dimension score.
    """

    rubric = get_scoring_rubric()

    validated_result = {}

    for dimension, dimension_rubric in rubric.items():

        if dimension not in evaluation:
            raise ValueError(
                f"LLM response is missing dimension: "
                f"{dimension}"
            )

        llm_dimension = evaluation[dimension]

        llm_criteria = llm_dimension.get(
            "criteria",
            {},
        )

        validated_criteria = {}

        calculated_score = 0

        for criterion, max_points in (
            dimension_rubric["criteria"].items()
        ):

            if criterion not in llm_criteria:
                raise ValueError(
                    f"Missing criterion "
                    f"'{criterion}' in "
                    f"'{dimension}'."
                )

            criterion_result = llm_criteria[
                criterion
            ]

            points = criterion_result.get(
                "points_awarded",
                0,
            )

            try:
                points = float(points)
            except (TypeError, ValueError):
                raise ValueError(
                    f"Invalid score for "
                    f"{dimension}.{criterion}"
                )

            # Prevent scores below zero
            points = max(
                0,
                points,
            )

            # Prevent scores above rubric maximum
            points = min(
                points,
                max_points,
            )

            # Convert whole-number floats to integers
            if points.is_integer():
                points = int(points)

            calculated_score += points

            validated_criteria[criterion] = {
                "points_awarded": points,
                "max_points": max_points,
                "reason": criterion_result.get(
                    "reason",
                    "",
                ),
                "evidence": criterion_result.get(
                    "evidence",
                    [],
                ),
            }

        if isinstance(calculated_score, float):
            calculated_score = round(
                calculated_score,
                2,
            )

        validated_result[dimension] = {
            "name": dimension_rubric["name"],
            "criteria": validated_criteria,

            # IMPORTANT:
            # This score is calculated by Python,
            # not trusted directly from the LLM.
            "score": calculated_score,

            "explanation": llm_dimension.get(
                "explanation",
                "",
            ),

            "recommendation": llm_dimension.get(
                "recommendation",
                "",
            ),
        }

    return validated_result


def evaluate_with_llm(payload):
    """
    Send grounded evidence and scoring rubric to
    GPT-5.6 Luna.

    Validate the response and calculate final scores
    deterministically in Python.
    """

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY was not found. "
            "Check your .env file."
        )

    client = OpenAI(
        api_key=api_key
    )

    user_prompt = build_user_prompt(
        payload
    )

    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions=SYSTEM_PROMPT,
        input=user_prompt,
    )

    raw_text = response.output_text

    if not raw_text:
        raise ValueError(
            "The LLM returned an empty response."
        )

    try:
        evaluation = json.loads(
            raw_text
        )

    except json.JSONDecodeError as error:
        raise ValueError(
            "The LLM response was not valid JSON.\n"
            f"Raw response:\n{raw_text}"
        ) from error

    validated_evaluation = (
        validate_llm_evaluation(
            evaluation
        )
    )

    return validated_evaluation