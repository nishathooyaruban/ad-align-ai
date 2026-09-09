SCORING_RUBRIC = {
    "message_match": {
        "name": "Message Match",
        "description": (
            "Measures how well the landing page supports "
            "the keyword, ad headline, and ad promises."
        ),
        "criteria": {
            "keyword_alignment": {
                "max_points": 25,
                "guidance": (
                    "Score based on how directly the landing page "
                    "supports the search keyword.\n\n"
                    "22-25: Keyword or very close semantic equivalent "
                    "is clearly and repeatedly supported.\n"
                    "16-21: Keyword intent is mostly supported but "
                    "wording or topic coverage is less direct.\n"
                    "10-15: Partial topical overlap exists, but the "
                    "keyword intent is only partly supported.\n"
                    "0-9: Little or no meaningful keyword support."
                ),
            },

            "headline_alignment": {
                "max_points": 25,
                "guidance": (
                    "Score how well the landing page supports the "
                    "main message in the ad headline.\n\n"
                    "22-25: Headline message is strongly and directly "
                    "supported.\n"
                    "16-21: Most of the headline is supported, with "
                    "some missing or indirect elements.\n"
                    "10-15: Only part of the headline is supported.\n"
                    "0-9: Headline is poorly supported or unrelated."
                ),
            },

            "ad_description_alignment": {
                "max_points": 25,
                "guidance": (
                    "Evaluate each meaningful promise in the ad "
                    "description separately before assigning points.\n\n"
                    "22-25: Almost every important promise is directly "
                    "supported by landing-page evidence. No major "
                    "promise is missing.\n"
                    "16-21: Most promises are supported, but one "
                    "meaningful promise is missing, indirect, or "
                    "only partially supported.\n"
                    "10-15: Some promises are supported, but two or "
                    "more important promises are missing or not "
                    "explicitly supported.\n"
                    "0-9: Very little of the ad description is "
                    "supported by the landing page.\n\n"
                    "Important rule: Do not treat related wording as "
                    "proof of a specific promise. For example, "
                    "'personalized tours' does not automatically prove "
                    "'private tours', and 'get quote' does not prove "
                    "'free quote'."
                ),
            },

            "promise_consistency": {
                "max_points": 25,
                "guidance": (
                    "Score whether the promises made by the ad are "
                    "consistent with what the landing page actually "
                    "presents.\n\n"
                    "22-25: Ad promises are highly consistent with the "
                    "page and no major contradiction or unsupported "
                    "claim exists.\n"
                    "16-21: Mostly consistent, but one or more promises "
                    "lack complete support.\n"
                    "10-15: Several promises are only partly supported "
                    "or create noticeable expectation gaps.\n"
                    "0-9: Major promises are unsupported, misleading, "
                    "or inconsistent with the page."
                ),
            },
        },
    },

    "search_intent_match": {
        "name": "Search Intent Match",
        "description": (
            "Measures whether the landing page satisfies "
            "the likely intent behind the search keyword."
        ),
        "criteria": {
            "topic_relevance": {
                "max_points": 30,
                "guidance": (
                    "Score how directly the landing page topic matches "
                    "the search topic."
                ),
            },

            "intent_satisfaction": {
                "max_points": 30,
                "guidance": (
                    "Score whether the page gives the visitor the "
                    "information or action needed to satisfy the likely "
                    "search intent."
                ),
            },

            "content_focus": {
                "max_points": 20,
                "guidance": (
                    "Score how strongly the page remains focused on "
                    "the relevant search topic."
                ),
            },

            "irrelevant_content_penalty": {
                "max_points": 20,
                "guidance": (
                    "Higher points mean less harmful irrelevant content. "
                    "Reduce points when unrelated content distracts from "
                    "the user's search intent."
                ),
            },
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
            "offer_presence": {
                "max_points": 30,
                "guidance": (
                    "Score whether the advertised product or service "
                    "offer is clearly present on the landing page."
                ),
            },

            "offer_consistency": {
                "max_points": 30,
                "guidance": (
                    "Score how consistently the landing-page offer "
                    "matches the advertised offer."
                ),
            },

            "offer_details": {
                "max_points": 20,
                "guidance": (
                    "Score whether enough useful details are supplied "
                    "to understand the offer."
                ),
            },

            "offer_clarity": {
                "max_points": 20,
                "guidance": (
                    "Score how clearly the visitor can understand "
                    "what is being offered."
                ),
            },
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
            "primary_cta_exists": {
                "max_points": 25,
                "guidance": (
                    "Score whether a clear primary call to action "
                    "exists."
                ),
            },

            "cta_matches_ad_offer": {
                "max_points": 25,
                "guidance": (
                    "Score whether the call to action directly supports "
                    "the action or offer promised in the advertisement."
                ),
            },

            "cta_specificity": {
                "max_points": 20,
                "guidance": (
                    "Score how specific the CTA wording is about what "
                    "the visitor will do or receive."
                ),
            },

            "action_available": {
                "max_points": 15,
                "guidance": (
                    "Score whether the visitor has an actual available "
                    "path to take the intended action."
                ),
            },

            "action_clarity": {
                "max_points": 15,
                "guidance": (
                    "Score how clearly the next step is communicated."
                ),
            },
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
            "business_identity": {
                "max_points": 20,
                "guidance": (
                    "Score whether the business identity is clearly "
                    "present and understandable."
                ),
            },

            "contact_information": {
                "max_points": 15,
                "guidance": (
                    "Score the quality and availability of contact "
                    "information."
                ),
            },

            "customer_evidence": {
                "max_points": 25,
                "guidance": (
                    "Score customer testimonials, reviews, case evidence, "
                    "or similar trust-supporting material."
                ),
            },

            "experience_or_credentials": {
                "max_points": 20,
                "guidance": (
                    "Score evidence of experience, expertise, credentials, "
                    "or qualifications."
                ),
            },

            "verifiable_trust_signals": {
                "max_points": 20,
                "guidance": (
                    "Score independently verifiable trust signals more "
                    "highly than self-reported claims. Do not treat "
                    "unsupported marketing claims as independently "
                    "verified evidence."
                ),
            },
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
            "offer_clarity": {
                "max_points": 20,
                "guidance": (
                    "Score whether the visitor can clearly understand "
                    "the offer."
                ),
            },

            "cta_accessibility": {
                "max_points": 20,
                "guidance": (
                    "Score whether the visitor has an accessible path "
                    "to take action based on supplied evidence."
                ),
            },

            "trust_support": {
                "max_points": 20,
                "guidance": (
                    "Score whether enough trust evidence exists to "
                    "support a visitor's decision."
                ),
            },

            "decision_information": {
                "max_points": 20,
                "guidance": (
                    "Score whether the visitor has enough practical "
                    "information to make a decision."
                ),
            },

            "conversion_friction": {
                "max_points": 20,
                "guidance": (
                    "Higher points mean lower apparent friction. "
                    "Reduce points when missing information, unclear "
                    "forms, unclear next steps, or unsupported promises "
                    "could make conversion harder."
                ),
            },
        },
    },
}


def validate_rubric():
    """
    Verify that every scoring dimension totals 100 points.
    """

    for dimension, rubric in SCORING_RUBRIC.items():

        total = sum(
            criterion["max_points"]
            for criterion in rubric["criteria"].values()
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