import sys
from pathlib import Path

import streamlit as st


# -------------------------------------------------
# Project path setup
# -------------------------------------------------

PROJECT_ROOT = Path(
    __file__
).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


# -------------------------------------------------
# AdAlign AI imports
# -------------------------------------------------

from crawler.crawler import crawl_page
from analyzer.relevance_analyzer import analyze_relevance
from analyzer.llm_evaluator import (
    build_evaluation_payload,
    evaluate_with_llm,
)


# -------------------------------------------------
# Page configuration
# -------------------------------------------------

st.set_page_config(
    page_title="AdAlign AI",
    page_icon="🎯",
    layout="wide",
)


# -------------------------------------------------
# Helper functions
# -------------------------------------------------

def classify_score(score):
    """
    Convert numerical score into a simple label.
    """

    if score >= 70:
        return "Strong"

    if score >= 40:
        return "Moderate"

    return "Weak"


def parse_assets(text):
    """
    Convert one-asset-per-line text into
    a clean list of ad assets.
    """

    assets = []

    for line in text.splitlines():

        cleaned_line = line.strip()

        if cleaned_line:
            assets.append(
                cleaned_line
            )

    return assets


def display_asset_results(
    title,
    asset_results,
):
    """
    Display deterministic asset-level
    landing-page match results.
    """

    st.subheader(
        title
    )

    if not asset_results:

        st.info(
            "No assets were supplied."
        )

        return

    for index, asset in enumerate(
        asset_results,
        start=1,
    ):

        score = asset.get(
            "match_score",
            0,
        )

        text = asset.get(
            "text",
            "",
        )

        matched_words = asset.get(
            "matched_words",
            [],
        )

        meaningful_words = asset.get(
            "meaningful_words",
            [],
        )

        st.markdown(
            f"**Asset {index}: {text}**"
        )

        st.progress(
            min(
                float(score) / 100,
                1.0,
            )
        )

        st.write(
            f"Deterministic match: "
            f"**{score}/100**"
        )

        st.write(
            "Matched words:",
            matched_words,
        )

        unmatched_words = [
            word
            for word in meaningful_words
            if word not in matched_words
        ]

        if unmatched_words:

            st.write(
                "Unmatched words:",
                unmatched_words,
            )

        st.divider()


def display_dimension(
    result,
    dimension_key,
):
    """
    Display detailed LLM results for one
    scoring dimension.
    """

    dimension = result[
        dimension_key
    ]

    score = dimension[
        "score"
    ]

    st.subheader(
        f'{dimension["name"]} — {score}/100'
    )

    st.progress(
        min(
            float(score) / 100,
            1.0,
        )
    )

    st.caption(
        f"Assessment: {classify_score(score)}"
    )

    explanation = dimension.get(
        "explanation",
        "",
    )

    if explanation:
        st.write(
            explanation
        )

    st.markdown(
        "#### Criterion Breakdown"
    )

    for (
        criterion_name,
        criterion_result,
    ) in dimension[
        "criteria"
    ].items():

        readable_name = (
            criterion_name
            .replace("_", " ")
            .title()
        )

        points = criterion_result[
            "points_awarded"
        ]

        max_points = criterion_result[
            "max_points"
        ]

        with st.expander(
            f"{readable_name}: "
            f"{points}/{max_points}"
        ):

            st.markdown(
                "**Reason**"
            )

            st.write(
                criterion_result.get(
                    "reason",
                    "",
                )
            )

            evidence = (
                criterion_result.get(
                    "evidence",
                    [],
                )
            )

            st.markdown(
                "**Evidence**"
            )

            if evidence:

                for item in evidence:
                    st.write(
                        f"• {item}"
                    )

            else:

                st.write(
                    "No supporting evidence supplied."
                )

    recommendation = dimension.get(
        "recommendation",
        "",
    )

    if recommendation:

        st.markdown(
            "#### Recommendation"
        )

        st.info(
            recommendation
        )


# -------------------------------------------------
# Header
# -------------------------------------------------

st.title(
    "🎯 AdAlign AI"
)

st.subheader(
    "AI-Powered Google Ads & "
    "Landing Page Relevance Analyzer"
)

st.write(
    "Evaluate how well multiple Google Ads "
    "headline and description assets align "
    "with a landing page."
)

st.divider()


# -------------------------------------------------
# Input section
# -------------------------------------------------

st.header(
    "Campaign Input"
)

url = st.text_input(
    "Landing Page URL",
    placeholder=(
        "https://example.com/"
    ),
)

keyword = st.text_input(
    "Target Keyword",
    placeholder=(
        "Sri Lanka tour packages"
    ),
)

st.markdown(
    "### Google Ads Headlines"
)

st.caption(
    "Enter one headline per line."
)

headline_text = st.text_area(
    "Headline Assets",
    placeholder=(
        "Best Sri Lanka Tour Packages\n"
        "Private Sri Lanka Tours\n"
        "Experienced Local Tour Guides"
    ),
    height=150,
)

st.markdown(
    "### Google Ads Descriptions"
)

st.caption(
    "Enter one description per line."
)

description_text = st.text_area(
    "Description Assets",
    placeholder=(
        "Custom private tours with experienced "
        "local guides. Get a free quote today.\n"
        "Explore flexible Sri Lanka tour packages "
        "with local travel experts."
    ),
    height=180,
)


# -------------------------------------------------
# Analyze button
# -------------------------------------------------

analyze_button = st.button(
    "Analyze Landing Page",
    type="primary",
    use_container_width=True,
)


# -------------------------------------------------
# Analysis
# -------------------------------------------------

if analyze_button:

    ad_headlines = parse_assets(
        headline_text
    )

    ad_descriptions = parse_assets(
        description_text
    )

    if not url.strip():

        st.error(
            "Please enter a landing page URL."
        )

        st.stop()

    if not keyword.strip():

        st.error(
            "Please enter a target keyword."
        )

        st.stop()

    if not ad_headlines:

        st.error(
            "Please enter at least one "
            "Google Ads headline."
        )

        st.stop()

    if not ad_descriptions:

        st.error(
            "Please enter at least one "
            "Google Ads description."
        )

        st.stop()

    try:

        with st.status(
            "Analyzing landing page...",
            expanded=True,
        ) as status:

            st.write(
                "Crawling landing page..."
            )

            page_data = crawl_page(
                url.strip()
            )

            st.write(
                "Running deterministic "
                "asset-level checks..."
            )

            deterministic_analysis = (
                analyze_relevance(
                    keyword=keyword.strip(),
                    ad_headlines=(
                        ad_headlines
                    ),
                    ad_descriptions=(
                        ad_descriptions
                    ),
                    page_data=page_data,
                )
            )

            st.write(
                "Building grounded evidence..."
            )

            payload = (
                build_evaluation_payload(
                    keyword=keyword.strip(),
                    ad_headlines=(
                        ad_headlines
                    ),
                    ad_descriptions=(
                        ad_descriptions
                    ),
                    page_data=page_data,
                    deterministic_analysis=(
                        deterministic_analysis
                    ),
                )
            )

            st.write(
                "Running AI evaluation..."
            )

            result = evaluate_with_llm(
                payload
            )

            status.update(
                label="Analysis complete",
                state="complete",
                expanded=False,
            )

        # -----------------------------------------
        # Campaign summary
        # -----------------------------------------

        st.divider()

        st.header(
            "Campaign Summary"
        )

        summary_columns = st.columns(
            4
        )

        with summary_columns[0]:

            st.metric(
                "Headlines",
                len(
                    ad_headlines
                ),
            )

        with summary_columns[1]:

            st.metric(
                "Descriptions",
                len(
                    ad_descriptions
                ),
            )

        with summary_columns[2]:

            st.metric(
                "Headline Avg Match",
                (
                    f'{deterministic_analysis.get(
                        "headline_average_score",
                        0,
                    )}/100'
                ),
            )

        with summary_columns[3]:

            st.metric(
                "Description Avg Match",
                (
                    f'{deterministic_analysis.get(
                        "description_average_score",
                        0,
                    )}/100'
                ),
            )

        # -----------------------------------------
        # Main AI scorecard
        # -----------------------------------------

        st.divider()

        st.header(
            "AdAlign AI Scorecard"
        )

        dimensions = [
            (
                "message_match",
                "Message Match",
            ),
            (
                "search_intent_match",
                "Search Intent",
            ),
            (
                "offer_relevance",
                "Offer Relevance",
            ),
            (
                "cta_strength",
                "CTA Strength",
            ),
            (
                "trust_credibility",
                "Trust & Credibility",
            ),
            (
                "conversion_readiness",
                "Conversion Readiness",
            ),
        ]

        first_row = st.columns(
            3
        )

        second_row = st.columns(
            3
        )

        all_columns = (
            first_row
            + second_row
        )

        for (
            column,
            dimension,
        ) in zip(
            all_columns,
            dimensions,
        ):

            dimension_key = (
                dimension[0]
            )

            label = (
                dimension[1]
            )

            score = result[
                dimension_key
            ][
                "score"
            ]

            with column:

                st.metric(
                    label=label,
                    value=f"{score}/100",
                )

                st.progress(
                    min(
                        float(score) / 100,
                        1.0,
                    )
                )

                st.caption(
                    classify_score(
                        score
                    )
                )

        # -----------------------------------------
        # Asset-level analysis
        # -----------------------------------------

        st.divider()

        st.header(
            "Ad Asset Alignment"
        )

        st.write(
            "These scores come from the "
            "deterministic text-matching layer. "
            "The AI evaluator then considers "
            "semantic meaning and the full page "
            "evidence."
        )

        headline_tab, description_tab = (
            st.tabs(
                [
                    "Headline Assets",
                    "Description Assets",
                ]
            )
        )

        with headline_tab:

            display_asset_results(
                title=(
                    "Headline → Landing Page Match"
                ),
                asset_results=(
                    deterministic_analysis.get(
                        "headline_results",
                        [],
                    )
                ),
            )

        with description_tab:

            display_asset_results(
                title=(
                    "Description → Landing Page Match"
                ),
                asset_results=(
                    deterministic_analysis.get(
                        "description_results",
                        [],
                    )
                ),
            )

        # -----------------------------------------
        # Weakest assets
        # -----------------------------------------

        st.divider()

        st.header(
            "Potential Alignment Issues"
        )

        weakest_headline = (
            deterministic_analysis.get(
                "weakest_headline"
            )
        )

        weakest_description = (
            deterministic_analysis.get(
                "weakest_description"
            )
        )

        issue_columns = st.columns(
            2
        )

        with issue_columns[0]:

            st.markdown(
                "#### Weakest Headline"
            )

            if weakest_headline:

                st.write(
                    weakest_headline.get(
                        "text",
                        "",
                    )
                )

                st.metric(
                    "Match Score",
                    (
                        f'{weakest_headline.get(
                            "match_score",
                            0,
                        )}/100'
                    ),
                )

            else:

                st.write(
                    "No headline data."
                )

        with issue_columns[1]:

            st.markdown(
                "#### Weakest Description"
            )

            if weakest_description:

                st.write(
                    weakest_description.get(
                        "text",
                        "",
                    )
                )

                st.metric(
                    "Match Score",
                    (
                        f'{weakest_description.get(
                            "match_score",
                            0,
                        )}/100'
                    ),
                )

            else:

                st.write(
                    "No description data."
                )

        # -----------------------------------------
        # Detailed AI evaluation
        # -----------------------------------------

        st.divider()

        st.header(
            "Detailed AI Evaluation"
        )

        for (
            dimension_key,
            _,
        ) in dimensions:

            display_dimension(
                result=result,
                dimension_key=dimension_key,
            )

            st.divider()

    except Exception as error:

        st.error(
            "The analysis could not be completed."
        )

        st.exception(
            error
        )


# -------------------------------------------------
# Footer
# -------------------------------------------------

st.caption(
    "AdAlign AI — Evidence-grounded analysis "
    "for Google Ads and landing-page alignment. "
    "Scores are assessments, not predictions "
    "of actual conversion rate."
)