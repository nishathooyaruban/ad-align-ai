SCORING_RUBRIC = {
    "message_match": {
        "name": "Message Match",
        "description": (
            "Measures how well the landing page supports "
            "the keyword, ad headline, and ad promises."
        ),
        "criteria": {
            "keyword_alignment": 25,
            "headline_alignment": 25,
            "ad_description_alignment": 25,
            "promise_consistency": 25,
        },
    },

    "search_intent_match": {
        "name": "Search Intent Match",
        "description": (
            "Measures whether the landing page satisfies "
            "the likely intent behind the search keyword."
        ),
        "criteria": {
            "topic_relevance": 30,
            "intent_satisfaction": 30,
            "content_focus": 20,
            "irrelevant_content_penalty": 20,
        },
    },

    "offer_relevance": {
        "name": "Offer Relevance",
        "description": (
            "Measures whether the product or service "
            "offered on the landing page matches what "
            "the advertisement promises."
        ),
        "criteria": {
            "offer_presence": 30,
            "offer_consistency": 30,
            "offer_details": 20,
            "offer_clarity": 20,
        },
    },

    "cta_strength": {
        "name": "CTA Strength",
        "description": (
            "Measures how clearly and effectively the "
            "landing page encourages the visitor to "
            "take the intended action."
        ),
        "criteria": {
            "primary_cta_exists": 25,
            "cta_matches_ad_offer": 25,
            "cta_specificity": 20,
            "action_available": 15,
            "action_clarity": 15,
        },
    },

    "trust_credibility": {
        "name": "Trust & Credibility",
        "description": (
            "Measures the amount and quality of evidence "
            "that helps a visitor trust the business "
            "and its claims."
        ),
        "criteria": {
            "business_identity": 20,
            "contact_information": 15,
            "customer_evidence": 25,
            "experience_or_credentials": 20,
            "verifiable_trust_signals": 20,
        },
    },

    "conversion_readiness": {
        "name": "Conversion Readiness",
        "description": (
            "Measures whether the available landing-page "
            "evidence indicates that a visitor has enough "
            "clarity and opportunity to take the desired "
            "action. It does not predict conversion rate."
        ),
        "criteria": {
            "offer_clarity": 20,
            "cta_accessibility": 20,
            "trust_support": 20,
            "decision_information": 20,
            "conversion_friction": 20,
        },
    },
}


def validate_rubric():
    """
    Verify that every scoring dimension totals 100 points.
    """

    for dimension, rubric in SCORING_RUBRIC.items():

        total = sum(
            rubric["criteria"].values()
        )

        if total != 100:
            raise ValueError(
                f"{dimension} rubric totals "
                f"{total}, expected 100."
            )

    return True


def get_scoring_rubric():
    """
    Return the complete AdAlign AI scoring rubric.
    """

    validate_rubric()

    return SCORING_RUBRIC