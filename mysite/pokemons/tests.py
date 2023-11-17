from django.test import TestCase
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_page(self):
        response = self.client.get('/pokemons/')
        self.assertEqual(response.status_code, 200)

    def test_pokemon(self):
        response = self.client.get('/pokemons/pikachu')
        self.assertEqual(response.status_code, 200)

    def test_fight(self):
        response = self.client.get('/pokemons/pikachu/fight')
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.post('/pokemons/search', {'search': 'pikachu'})
        self.assertEqual(response.status_code, 200)

    def test_result(self):
        response = self.client.post('/pokemons/pikachu/fight/result', {'send_type': 'db', 'event': 'test event saved!'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/pokemons/pikachu/fight/result', {'send_type': 'mail', 'event': 'test event saved!', 'email': 'dimas.sektor001@mail.ru'})
        self.assertEqual(response.status_code, 200)

    def test_save(self):
        response = self.client.post('/pokemons/pikachu/save', {'server': 'localhost', 'login': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 200)


class SeleniumTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Edge(service=Service('C:\\Temp\\msedgedriver.exe'))

    def test_page(self):
        self.driver.get('http://localhost:8000/pokemons/')
        element = self.driver.find_element(By.TAG_NAME, 'p')
        self.assertTrue(element.text)

    def test_pokemon(self):
        self.driver.get('http://localhost:8000/pokemons/pikachu')
        element = self.driver.find_element(By.TAG_NAME, 'a')
        self.assertEqual(element.text, 'pikachu')

    def test_search(self):
        self.driver.get('http://localhost:8000/pokemons/')
        element = self.driver.find_element(By.ID, 'search')
        element.send_keys('pikachu')
        element.submit()

    def test_fight(self):
        self.driver.get('http://localhost:8000/pokemons/pikachu/fight')
        element = self.driver.find_element(By.ID, 'input')
        element.send_keys('5')
        button = self.driver.find_element(By.XPATH, '//button[text()="Бросить"]')
        button.click()
