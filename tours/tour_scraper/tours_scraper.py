from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common import service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from time import sleep, time
from bs4 import BeautifulSoup as bs
import pandas as pd
from pathlib import Path
import os
import csv
from tours_settings import CITIES, BASE_URL, DRIVER_PATH, COOKIE_BTN
from concurrent.futures import ThreadPoolExecutor


class ToursScraper:

    # chrome_options.add_argument('--window-size=1420,1080')
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')

    def __init__(self):
        self.driver_path = DRIVER_PATH
        self.url = BASE_URL
        #self.service = Service(self.driver_path)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("enable-features=NetworkServiceInProcess")
        chrome_options.add_argument("disable-features=NetworkService")
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}

        #self.service = Service(self.driver_path)
        #chromeOptions = Options()
        #chromeOptions.headless = True
        # self.driver = webdriver.Chrome(
        #     service=self.service, options=chrome_options)
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_urls(self):
        """
            The function takes a list of cities and returns a list of urls of each city.


            Returns:
                city_names (List): List of strings of popular city names.


        """

        self.driver.get(self.url)
        sleep(2)
        try:
            cookie_btn = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    ('xpath', COOKIE_BTN))
            )

            cookie_btn.click()
        except NoSuchElementException:
            print('cookie button not found!')
        except TimeoutException:
            print('cookie button time out')

        self.city_urls = []
        i = 0
        while i < len(CITIES):

            for self.city in CITIES:
                search_input = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located(
                        ('xpath', '//*[@id="root"]/div/div[2]/div/div/div[1]/form/div[1]'))
                )

                search_input.click()
                sleep(1)
                try:
                    search_input_focus = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable(
                            ('xpath', '//input[@placeholder="Search for a city"]'))
                    )
                    sleep(3)
                    search_input_focus.send_keys(self.city)
                    sleep(3)
                    search_input_focus.send_keys(Keys.ARROW_DOWN)
                    sleep(2)
                    city_ele = self.driver.find_element(
                        'xpath', '//ul[@role="tablist"]/li[1]')
                    city_ele.click()
                except TimeoutException:
                    pass
                except NoSuchElementException:
                    pass

                sleep(3)
                search_btn = self.driver.find_element(
                    'xpath', '//button[@type="submit"]')
                search_btn.click()
                sleep(5)
                try:
                    WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(
                        ('xpath', '(//a[@class="c2OEc-big-cta"])[2]')))
                    # sleep(5)
                    search_tours = self.driver.find_element(
                        'xpath', '(//a[@class="c2OEc-big-cta"])[2]')

                    actions = ActionChains(self.driver)
                    actions.move_to_element(search_tours)
                    actions.perform()
                    search_tours.click()
                    city_url = self.driver.current_url
                    self.city_urls.append(city_url)

                except:
                    city_url = self.driver.current_url
                    self.city_urls.append(city_url)
                sleep(5)
                i += 1

    def get_data(self, url):
        """
        The function takes urls of cities and extracts information about tours found in each city
        """

        self.driver.get(url)
        sleep(3)

        # scroll page down
        scroll_pause_time = 3
        i = 0
        number_of_scrolls = 2

        # Get scroll height
        previous_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        while i < number_of_scrolls:
            print(f'scrolled {i} time(s)')
            # Scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
            sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
            current_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            if current_height == previous_height:
                # If heights are the same it will exit the function
                break

            previous_height = current_height
            i += 1

        sleep(2)

    # parse page source using beautifulsoup

        soup = bs(self.driver.page_source, "lxml")

        tours = soup.find_all('div', class_="c0p_q")

        self.titles = []
        self.ratings = []
        self.number_of_ratings = []
        self.prices = []
        self.durations = []
        self.star_ratings = []
        self.providers = []

        for tour in tours:
            try:
                title = tour.find('div', class_="c4Hod-title").text
            except:
                title = 'no data provided'

            try:
                rating = tour.find('span', class_="nV2T-rating").text
            except:
                rating = 'no data provided'

            try:
                num_of_ratings = tour.find(
                    'span', class_="nV2T-rating-count-plain").text.lstrip('(').rstrip(')')
            except:
                num_of_ratings = 'no data provided'

            try:
                price = tour.find('span', class_="c0p_q-price").text
            except:
                price = 'no data provided'

            try:
                duration = tour.find('div', class_="sNnk-title").text
            except:
                duration = 'No data provided'
            try:
                provider = tour.find(
                    'span', class_='c0p_q-provider').text
            except:
                provider = 'No data provided'
            try:
                stars = len(tour.find(
                    'div', class_="O3Yc O3Yc-sp-compact"))

            except:
                stars = 'No data provided'

            self.titles.append(title)
            self.ratings.append(rating)
            self.number_of_ratings.append(num_of_ratings)
            self.prices.append(price)
            self.durations.append(duration)
            self.star_ratings.append(stars)
            self.providers.append(provider)

            city = url.split('/')[-1].split(',')[0]

        # save data to dataframe and csv
        df = pd.DataFrame({'Titles': self.titles,
                           'Ratings': self.ratings,
                           'Number_Of_Ratings': self.number_of_ratings,
                           'Prices': self.prices,
                           'Durations': self.durations,
                           'Star_Ratings': self.star_ratings,
                           'Tour_Provider': self.providers

                           })
        # data_file_path = os.path.join(dir, 'tours_data')
        # df.to_csv(f'{data_file_path}/{city}.csv',
        #           encoding='utf-8', index=False)


if __name__ == '__main__':
    scraper = ToursScraper()
    scraper.get_urls()
    start_time = time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(scraper.get_data, scraper.city_urls)

    print(time()-start_time)
    scraper.driver.close()

    # scraper.driver.quit()
    # path = Path(
    #     'C:/Users/admin/Desktop/cheapflights-webscraping-team/src/tours/')
    # data_dir = Path.cwd()/'..'
    # print(f'cwd : {data_dir}')
    # from pathlib import Path

    # dir = Path(__file__).parents[1]
    # print(dir)
    # data_file_path = os.path.join(dir, 'tours_data')

    # print(data_file_path)
