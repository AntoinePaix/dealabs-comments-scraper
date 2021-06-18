import csv
from pathlib import Path
from pprint import pprint

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class DealabsCommentsScraper:
    def __init__(self, url, headless=False, verbose=True):
        self.url = url
        self.options = Options()
        self.options.headless = headless
        self.total_comments = 0
        self.new_comments = 0
        self.verbose = verbose
        self.fieldnames = ['url', 'thread_id', 'comment_id', 'author', 'content', 'timestamp']
        self.thread_id = None
        self.filename = None
        self.driver = None

    def __repr__(self):
        return f"<{self.__class__.__name__}(url={self.url}, headless={self.options.headless}, verbose={self.verbose})>"
    
    def _init_driver(self):
        if self.driver is None:
            self.driver = webdriver.Firefox(options=self.options)
            self.driver.get(self.url)
            self._accept_cookies()
            self.thread_id = self._get_thread_id()
    
    def _get_thread_id(self):
        return self.url.split('-')[-1]
    
    def _accept_cookies(self):
        btn_accept_cookies = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[4]/div[1]/div/div[1]/div[2]/button[2]/span"))
        )
        btn_accept_cookies.click()

    def _generate_csv_file(self):
        if self.thread_id is None:
            self.thread_id = self._get_thread_id()
        self.filename = f'{self.thread_id}.csv'
        file = Path(self.filename)
        if file.is_file():
            if self.verbose:
                print(f"Le fichier `{self.filename}` existe déjà. Les nouveaux commentaires seront ajoutés.")
        else:
            with open(self.filename, mode="w") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter=";")
                writer.writeheader()

    def _load_comments_id_from_csvfile(self):
        comments_id = set()
        with open(self.filename, mode="r") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                comments_id.add(row['comment_id'])
        return comments_id

    def generate_comments(self):
        self._init_driver()
        
        while True:

            # On recherche les commentaires et on affiche le texte
            comments_list = WebDriverWait(self.driver, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "commentList")))
            comments = WebDriverWait(self.driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.commentList-item")))

            for comment in comments:
                _id = comment.get_attribute("id")
                author = comment.find_element_by_class_name('userInfo-username').text
                content = comment.find_element_by_class_name('userHtml-content').text
                timestamp = comment.find_element_by_class_name('text--color-greyShade').text

                yield {
                    "url": self.url,
                    "thread_id": self.thread_id,
                    "comment_id": _id,
                    "author": author,
                    "content": content,
                    "timestamp": timestamp,
                }
                
            # On cherche le bouton 'suivant'
            try:
                # Check next button
                next_button = self.driver.find_element_by_css_selector("button[aria-label='Page suivante']")

                if next_button.is_enabled() and next_button.is_displayed():
                    next_button.click()
                else:
                    break
            except NoSuchElementException:
                break
        self.driver.close()

    def fetch_comments(self):
        self._generate_csv_file()
        comments_ids = self._load_comments_id_from_csvfile()

        # On écrit les commentaires dans un fichier CSV.
        with open(self.filename, mode="a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter=";")
            for comment in self.generate_comments():
                if comment['comment_id'] not in comments_ids:
                    writer.writerow(comment)
                    if self.verbose:
                        print(f"Un nouveau commentaire a été ajouté dans `{self.filename}`.")
                        self.new_comments += 1

                if self.verbose:
                    pprint(comment)

                self.total_comments += 1

        if self.verbose:
            print(f"#------ FIN DES COMMENTAIRES ------#")
            print(f"{self.total_comments} COMMENTAIRES TROUVÉS")
            print(f"{self.new_comments} COMMENTAIRES AJOUTÉS")
