TEST_CASES = [
    {
        "id": "strong_match",
        "name": "Strong Match — Sri Lanka Tours",
        "url": "https://ceylonempiretravels.com/",
        "keyword": "Sri Lanka tour packages",
        "ad_headline": "Best Sri Lanka Tour Packages",
        "ad_description": (
            "Custom private tours with experienced local guides. "
            "Get a free quote today."
        ),
        "expected": {
            "message_match": "high",
            "search_intent_match": "high",
            "offer_relevance": "high",
        },
    },

    {
        "id": "complete_mismatch",
        "name": "Complete Mismatch — Car Insurance",
        "url": "https://ceylonempiretravels.com/",
        "keyword": "car insurance Sri Lanka",
        "ad_headline": "Affordable Car Insurance Sri Lanka",
        "ad_description": (
            "Protect your vehicle with comprehensive insurance. "
            "Get your insurance quote today."
        ),
        "expected": {
            "message_match": "low",
            "search_intent_match": "low",
            "offer_relevance": "low",
        },
    },

    {
        "id": "partial_match",
        "name": "Partial Match — Luxury Honeymoon Tours",
        "url": "https://ceylonempiretravels.com/",
        "keyword": "luxury Sri Lanka tours",
        "ad_headline": "Luxury Sri Lanka Honeymoon Packages",
        "ad_description": (
            "Stay in five-star resorts with private chauffeur service, "
            "luxury villas, spa experiences, and exclusive honeymoon packages."
        ),
        "expected": {
            "message_match": "medium",
            "search_intent_match": "medium",
            "offer_relevance": "medium",
        },
    },
]


def get_test_cases():
    """
    Return all controlled AdAlign AI evaluation cases.
    """

    return TEST_CASES