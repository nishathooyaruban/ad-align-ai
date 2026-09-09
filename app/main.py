from crawler.crawler import crawl_page


url = "https://ceylonempiretravels.com/"

result = crawl_page(url)

print("\n=== ADALIGN AI — LANDING PAGE EVIDENCE ===")

print("\nURL:")
print(result["url"])

print("\nTITLE:")
print(result["title"])

print("\nMETA DESCRIPTION:")
print(result["meta_description"])

print("\nHEADINGS:")
print(result["headings"])

print("\nPARAGRAPHS:")
print(result["paragraphs"])

print("\nLINKS:")
print(result["links"])

print("\nBUTTONS:")
print(result["buttons"])

print("\nFORMS:")
print(result["form_count"])

print("\nIMAGES:")
print(result["image_count"])

print("\nIMAGES WITH ALT TEXT:")
print(result["images_with_alt"])