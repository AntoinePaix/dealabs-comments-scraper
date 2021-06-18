# from dealabs_scraper import DealabsCommentsScraper

# scraper = DealabsCommentsScraper(
#     "https://www.dealabs.com/bons-plans/dome-moustiquaire-insect-protect-140x200x150cm-2167450",
#     headless=True,
#     verbose=True
#     )

# print(scraper)
# scraper.fetch_comments()

from dealabs_scraper import DealabsCommentsScraper

scraper = DealabsCommentsScraper(
    "https://www.dealabs.com/bons-plans/dome-moustiquaire-insect-protect-140x200x150cm-2167450",
    headless=True,
    verbose=True
    )

print(scraper)

for comment in scraper.generate_comments():
    print(f"{comment['author']} a écrit `{comment['content']}`")
    print('-' * 50)