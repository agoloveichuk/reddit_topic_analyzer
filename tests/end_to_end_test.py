from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from msedge.selenium_tools import Edge

class MyApplicationEndToEndTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Налашутвання Selenium WebDriver для Edge
        cls.selenium = Edge()

    @classmethod
    def tearDownClass(cls):
        # Закриття Selenium WebDriver
        cls.selenium.quit()
        super().tearDownClass()

    def test_end_to_end_flow(self):
        # Відкриття додатку в браузері 
        self.selenium.get(self.live_server_url)

        # Знаходження пошукового елемента та введення topic
        search_input = self.selenium.find_element_by_name("topic")
        search_input.send_keys("python")
        search_input.send_keys(Keys.ENTER)

        # Верифікаця сторінки результату 
        self.assertIn("Search Results", self.selenium.title)

        # Перевірка елементу заголовку 
        header = self.selenium.find_element_by_tag_name("h1")
        self.assertEqual(header.text, 'Search Results for "python"')

        # Перевірка списку дописів 
        posts_list = self.selenium.find_element_by_tag_name("ul")
        posts = posts_list.find_elements_by_tag_name("li")
        self.assertGreater(len(posts), 0)

        # Перевірка списку найчастіших власних назв 
        entities_list = self.selenium.find_elements_by_xpath("//div/h2[contains(text(), 'List of top Entities')]/following-sibling::ul")
        entities = entities_list[0].find_elements_by_tag_name("li")
        self.assertGreater(len(entities), 0)

