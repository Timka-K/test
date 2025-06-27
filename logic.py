from random import randint
import requests

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1,1000)
        self.hp = randint(1,500)
        self.power = randint(1,500)
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
            return "Фото не найдено"
    
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
    
# Метод атаки покемона 
    def attack(self, enemy):
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "

    # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покеомона: {self.name}\nСила:{self.power}\nЗдоровье:{self.hp}\nВысота: {self.height}\nШирина: {self.weight}\nСпособности: {self.abilities}"

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img


class Wizard(Pokemon):
    #Увеличение здоровья
    def __init__(self, name, power, hp, height, weight, abilities, img, pokemon_trainer, pokemon_number):
        self.hp += 300

# Метод атаки мага
    def attack(self, enemy):
        # Проверка врага
        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance == 1:
                return f"{self.name} применил щит в сражении и уклонился от атаки!"
        return super().attack(enemy)
    
    def info(self):
        info_pok = super().info
        return f'{info_pok}\nУ тебя Маг(здоровье увеличино на 300)\nТеперь здоровье: {self.hp}'
    

class Fighter(Pokemon):
    #Увеличение силы
    def __init__(self, name, power, hp, height, weight, abilities, img, pokemon_trainer, pokemon_number):
        self.power += 200

#Метод атаки бойца
    def attack(self, enemy):
        super_boost = randint(5, 15) 
        self.power += super_boost
        result = super().attack(enemy)
        self.power -= super_boost  # Восстанавливаем силу
        return result + f"\nБоец применил супер-атаку силой: {super_boost}."
    
    def info(self):
        info_pok = super().info()
        return  f'{info_pok}\nУ тебя Боец(сила увеличина на 200)\nТеперь сила: {self.power}'
    

