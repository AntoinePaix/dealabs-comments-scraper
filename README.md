# dealabs-comments-scraper

Un scraper très simple qui permet de récupérer les commentaires sous un article publié sur dealabs.com

## Installation


```bash
mkdir dealabs-scraper
cd dealabs-scraper

python3 -m venv env
source env/bin/activate

git clone https://github.com/AntoinePaix/dealabs-comments-scraper
pip install -r requirements.txt
```

## Utilisation

Vous pouvez modifier le fichier `main.py`.


```python
# Pour enregistrer les nouveaux commentaires dans un fichier csv,
# utilisez la méthode .fetch_comments()

from dealabs_scraper import DealabsCommentsScraper

scraper = DealabsCommentsScraper(
    "https://www.dealabs.com/bons-plans/dome-moustiquaire-insect-protect-140x200x150cm-2167450",
    headless=True,
    verbose=True
    )

print(scraper)
scraper.fetch_comments()
```

```python
# Pour générer uniquement les nouveaux commentaires

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
```