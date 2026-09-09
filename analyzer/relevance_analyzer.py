# Common words that do not provide useful relevance evidence
STOP_WORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "this",
    "that",
    "your",
    "you",
    "our",
    "are",
    "was",
    "were",
    "have",
    "has",
    "get",
    "today",
}


def extract_meaningful_words(text):
    """
    Extract useful words from ad text while removing
    common stop words and punctuation.
    """

    meaningful_words = []

    for word in text.split():
        cleaned_word = word.lower().strip(".,!?;:'\"()")

        if (
            len(cleaned_word) > 3
            and cleaned_word not in STOP_WORDS
        ):
            meaningful_words.append(cleaned_word)

    return meaningful_words


def analyze_relevance(
    keyword,
    ad_headline,
    ad_description,
    page_data,
):
    """
    Compare a Google Ads keyword and ad copy against
    evidence extracted from the landing page.
    """

    # -------------------------------------------------
    # 1. Build searchable landing-page text
    # -------------------------------------------------

    page_text = " ".join(
        [
            page_data.get("title", ""),
            page_data.get("meta_description", ""),
            " ".join(
                page_data.get("headings", {}).get("h1", [])
            ),
            " ".join(
                page_data.get("headings", {}).get("h2", [])
            ),
            " ".join(
                page_data.get("headings", {}).get("h3", [])
            ),
            " ".join(page_data.get("paragraphs", [])),
            " ".join(page_data.get("links", [])),
            " ".join(page_data.get("buttons", [])),
        ]
    ).lower()

    # -------------------------------------------------
    # 2. Keyword Match
    # -------------------------------------------------

    keyword_match = keyword.lower() in page_text

    # -------------------------------------------------
    # 3. Ad Headline Match
    # -------------------------------------------------

    headline_words = extract_meaningful_words(
        ad_headline
    )

    matched_headline_words = [
        word
        for word in headline_words
        if word in page_text
    ]

    if headline_words:
        headline_match_ratio = (
            len(matched_headline_words)
            / len(headline_words)
        )
    else:
        headline_match_ratio = 0

    # -------------------------------------------------
    # 4. Message Match Score
    # -------------------------------------------------

    keyword_score = 40 if keyword_match else 0

    headline_score = round(
        headline_match_ratio * 60
    )

    message_match_score = (
        keyword_score + headline_score
    )

    # -------------------------------------------------
    # 5. Ad Description Match
    # -------------------------------------------------

    description_words = extract_meaningful_words(
        ad_description
    )

    matched_description_words = [
        word
        for word in description_words
        if word in page_text
    ]

    if description_words:
        description_match_ratio = (
            len(matched_description_words)
            / len(description_words)
        )
    else:
        description_match_ratio = 0

    description_match_score = round(
        description_match_ratio * 100
    )

    # -------------------------------------------------
    # 6. Return structured evidence
    # -------------------------------------------------

    return {
        "keyword": keyword,

        "keyword_found_on_page": keyword_match,

        "headline_words": headline_words,

        "matched_headline_words":
            matched_headline_words,

        "headline_match_count":
            len(matched_headline_words),

        "message_match_score":
            message_match_score,

        "description_words":
            description_words,

        "matched_description_words":
            matched_description_words,

        "description_match_score":
            description_match_score,
    }