import base64
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config as cfg
from log import getLogger


def crawl(query):
    with PaperSpider() as crawler:
        result = crawler.search(query)
    return result


class PaperSpider:
    def __init__(self, url=cfg.URL_B64, driver_path=cfg.CHROME_DRIVER_PATH):
        self.url = base64.b64decode(url).decode()
        self.driver_path = driver_path

        self.driver = None
        self.wait = None
        self.log = getLogger('PaperSpider')

    def _start(self):
        service = Service(executable_path=self.driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(self.url)
        self.wait = WebDriverWait(self.driver, 20)

        self.log.info(">>> Start crawler")

    def search(self, query):
        # fill query in search bar
        self.driver.find_element(
            By.CSS_SELECTOR, '.landing_search_bar #searchbar-input'
        ).send_keys(query)
        # click search button
        self.driver.find_element(
            By.CSS_SELECTOR, '.landing_search_bar div div button'
        ).click()
        self.log.info(f">>> Search {query}")
        # wait for the results and click the first result to build graph
        article_el = self.wait.until(
            lambda x: x.find_elements(By.CSS_SELECTOR, 'article')
        )
        self.log.info(">>> Select the first result to build graph")
        time.sleep(1)
        article_el[0].click()
        self.log.info(">>> Build graph")

        # Buttons are unclickable without waiting two seconds.
        time.sleep(2)
        btns = self.driver.find_elements(
            By.CSS_SELECTOR, '.main-view-navbar button .outlined-slot'
        )
        self.log.info(">>> Find prior papers")
        prior_papers = self._find_related_papers(btns[0])
        time.sleep(1)
        self.log.info(">>> Find derivative papers")
        derivative_papers = self._find_related_papers(btns[1])

        time.sleep(1)
        self.log.info(">>> Find the origin paper")
        self.driver.find_element(
            By.CSS_SELECTOR,
            '.minilist-column .flexcolumn .items-list .list-group-item-mod.main',
        ).click()
        origin_paper = self._extract_abstract_box()

        return {
            'origin_paper': origin_paper,
            'prior_papers': prior_papers,
            'derivative_papers': derivative_papers,
        }

    def _find_related_papers(self, btn):
        """Find **prior** or **derivative** papers."""
        # Click button and get the table containing the related papers
        btn.click()
        table_el = self.wait.until(
            lambda x: x.find_element(By.CSS_SELECTOR, '.sortable-table-table')
        )
        paper_els = table_el.find_elements(By.CSS_SELECTOR, 'tr')[1:]

        papers = []
        for paper_el in paper_els:
            paper_el.click()
            # Show the abstract box
            metadata = self._extract_abstract_box()
            papers.append(metadata)
        return papers

    def _extract_abstract_box(self):
        """Extract metadata from abstract box."""
        metadata = {}
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.abstractbox-column'))
        )
        # expand authors
        try:
            el = self.driver.find_element(
                By.CSS_SELECTOR, '.abstractbox-column .metadata .plus-authors'
            )
            el.click()
        except Exception:
            pass
        finally:
            abstract_el = self.driver.find_element(
                By.CSS_SELECTOR, '.abstractbox-column .abtract-scrollbox'
            )
        self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, '.abstractbox-column .abtract-scrollbox .flexrow')
            )
        )

        metadata['title'] = abstract_el.find_element(
            By.CSS_SELECTOR, '.title_link'
        ).get_attribute('innerHTML')
        metadata['authors'] = abstract_el.find_element(
            By.CSS_SELECTOR, '.metadata div div'
        ).get_attribute('innerHTML')
        metadata['link'] = abstract_el.find_element(
            By.CSS_SELECTOR, '.title_link'
        ).get_attribute('href')
        metadata['publication'] = abstract_el.find_element(
            By.CSS_SELECTOR, '.publication'
        ).get_attribute('innerHTML')
        metadata['year'] = int(metadata['publication'].strip()[:4])

        citations = abstract_el.find_elements(By.CSS_SELECTOR, '.flexrow .metadata')[
            1
        ].get_attribute('innerHTML')
        metadata['citations'] = int(citations.strip().split()[0])

        metadata['abstract'] = abstract_el.find_element(
            By.CSS_SELECTOR, '.abstract-text'
        ).get_attribute('innerHTML')

        self.log.info(f">>> Extract the meta data for: {metadata['title']}")

        return metadata

    def _close(self):
        self.driver.quit()

    def __enter__(self):
        time.sleep(1)
        self._start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()
