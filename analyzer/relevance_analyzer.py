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
    Extract useful words from text while removing
    common stop words and punctuation.
    """

    meaningful_words = []

    for word in text.split():

        cleaned_word = (
            word
            .lower()
            .strip(".,!?;:'\"()")
        )

        if (
            len(cleaned_word) > 3
            and cleaned_word not in STOP_WORDS
        ):
            meaningful_words.append(
                cleaned_word
            )

    return meaningful_words


def build_page_text(page_data):
    """
    Combine relevant landing-page evidence into
    one searchable text block.
    """

    page_text = " ".join(
        [
            page_data.get(
                "title",
                "",
            ),
            page_data.get(
                "meta_description",
                "",
            ),
            " ".join(
                page_data.get(
                    "headings",
                    {},
                ).get(
                    "h1",
                    [],
                )
            ),
            " ".join(
                page_data.get(
                    "headings",
                    {},
                ).get(
                    "h2",
                    [],
                )
            ),
            " ".join(
                page_data.get(
                    "headings",
                    {},
                ).get(
                    "h3",
                    [],
                )
            ),
            " ".join(
                page_data.get(
                    "paragraphs",
                    [],
                )
            ),
            " ".join(
                page_data.get(
                    "links",
                    [],
                )
            ),
            " ".join(
                page_data.get(
                    "buttons",
                    [],
                )
            ),
        ]
    ).lower()

    return page_text


def analyze_asset_match(
    text,
    page_text,
):
    """
    Measure simple deterministic text support for
    one headline or description asset.
    """

    meaningful_words = extract_meaningful_words(
        text
    )

    matched_words = [
        word
        for word in meaningful_words
        if word in page_text
    ]

    if meaningful_words:

        match_ratio = (
            len(matched_words)
            / len(meaningful_words)
        )

    else:

        match_ratio = 0

    match_score = round(
        match_ratio * 100
    )

    return {
        "text": text,
        "meaningful_words": meaningful_words,
        "matched_words": matched_words,
        "matched_word_count": len(
            matched_words
        ),
        "total_meaningful_words": len(
            meaningful_words
        ),
        "match_score": match_score,
    }


def calculate_average_score(
    asset_results,
):
    """
    Calculate the average deterministic score
    across a group of ad assets.
    """

    if not asset_results:
        return 0

    total = sum(
        item["match_score"]
        for item in asset_results
    )

    return round(
        total / len(asset_results)
    )


def analyze_relevance(
    keyword,
    ad_headlines,
    ad_descriptions,
    page_data,
):
    """
    Compare a Google Ads keyword and multiple ad
    headline/description assets against evidence
    extracted from the landing page.
    """

    page_text = build_page_text(
        page_data
    )

    # -------------------------------------------------
    # Keyword match
    # -------------------------------------------------

    keyword_match = (
        keyword.lower()
        in page_text
    )

    keyword_score = (
        100
        if keyword_match
        else 0
    )

    # -------------------------------------------------
    # Headline asset analysis
    # -------------------------------------------------

    headline_results = []

    for headline in ad_headlines:

        cleaned_headline = (
            headline.strip()
        )

        if not cleaned_headline:
            continue

        result = analyze_asset_match(
            text=cleaned_headline,
            page_text=page_text,
        )

        headline_results.append(
            result
        )

    headline_average_score = (
        calculate_average_score(
            headline_results
        )
    )

    # -------------------------------------------------
    # Description asset analysis
    # -------------------------------------------------

    description_results = []

    for description in ad_descriptions:

        cleaned_description = (
            description.strip()
        )

        if not cleaned_description:
            continue

        result = analyze_asset_match(
            text=cleaned_description,
            page_text=page_text,
        )

        description_results.append(
            result
        )

    description_average_score = (
        calculate_average_score(
            description_results
        )
    )

    # -------------------------------------------------
    # Overall deterministic message score
    # -------------------------------------------------

    component_scores = [
        keyword_score,
    ]

    if headline_results:
        component_scores.append(
            headline_average_score
        )

    if description_results:
        component_scores.append(
            description_average_score
        )

    if component_scores:

        overall_message_score = round(
            sum(component_scores)
            / len(component_scores)
        )

    else:

        overall_message_score = 0

    # -------------------------------------------------
    # Weakest assets
    # -------------------------------------------------

    weakest_headline = None

    if headline_results:

        weakest_headline = min(
            headline_results,
            key=lambda item: (
                item["match_score"]
            ),
        )

    weakest_description = None

    if description_results:

        weakest_description = min(
            description_results,
            key=lambda item: (
                item["match_score"]
            ),
        )

    # -------------------------------------------------
    # Result
    # -------------------------------------------------

    return {
        "keyword": keyword,

        "keyword_found_on_page": (
            keyword_match
        ),

        "keyword_match_score": (
            keyword_score
        ),

        "headline_results": (
            headline_results
        ),

        "headline_average_score": (
            headline_average_score
        ),

        "description_results": (
            description_results
        ),

        "description_average_score": (
            description_average_score
        ),

        "message_match_score": (
            overall_message_score
        ),

        "weakest_headline": (
            weakest_headline
        ),

        "weakest_description": (
            weakest_description
        ),
    }