from crawler.crawler import crawl_page
from analyzer.relevance_analyzer import analyze_relevance


url = "https://ceylonempiretravels.com/"

keyword = "Sri Lanka tour packages"

ad_headline = "Best Sri Lanka Tour Packages"

ad_description = (
    "Custom private tours with experienced local guides. "
    "Get a free quote today."
)

page_data = crawl_page(url)

analysis = analyze_relevance(
    keyword=keyword,
    ad_headline=ad_headline,
    ad_description=ad_description,
    page_data=page_data,
)

print("\n=== ADALIGN AI — RELEVANCE ANALYSIS ===")

print("\nKEYWORD:")
print(analysis["keyword"])

print("\nKEYWORD FOUND ON PAGE:")
print(analysis["keyword_found_on_page"])

print("\nHEADLINE WORDS:")
print(analysis["headline_words"])

print("\nMATCHED HEADLINE WORDS:")
print(analysis["matched_headline_words"])

print("\nHEADLINE MATCH COUNT:")
print(analysis["headline_match_count"])

print("\nMESSAGE MATCH SCORE:")
print(f'{analysis["message_match_score"]}/100')

print("\nAD DESCRIPTION MATCH SCORE:")
print(f'{analysis["description_match_score"]}/100')

print("\nMATCHED DESCRIPTION WORDS:")
print(analysis["matched_description_words"])