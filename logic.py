from random import randint
import requests

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.height = self.get_height()
        self.weight = self.get_weight()
        self.abilities = self.get_abilities()
        

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/{self.pokemon_number}.png'
        else:
            return "Photo is not found"
    
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"
        
# Метод для получения высоты покемона через API
    def get_height(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['height'])
        else:
            return "-"
        
# Метод для получения ширины покемона через API
    def get_weight(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['weight'])
        else:
            return "-"

# Метод для получения способностей покемона через API
    def get_abilities(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            abilities = []
            for ability in data.get('abilities', []):
                ability_name = ability['ability']['name']
                is_hidden = ability['is_hidden']
                abilities.append(f"{ability_name}" + (" (hidden)" if is_hidden else ""))
            return abilities
        return []

    # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покеомона: {self.name}\nВысота: {self.height}\nШирина: {self.weight}\nСпособности: {self.abilities}"

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img



