from random import randint
import requests

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1, 1000)
        self.hp = randint(1, 500)
        self.power = randint(1, 500)
        self.img = self.get_img()
        self.name = self.get_name()
        self.height = self.get_height()
        self.weight = self.get_weight()
        self.abilities = self.get_abilities()
        self.is_alive = True

        Pokemon.pokemons[pokemon_trainer] = self

    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            return f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/{self.pokemon_number}.png'
        return "Фото не найдено"

    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['forms'][0]['name']
        return "Pikachu"

    def get_height(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['height']
        return "-"

    def get_weight(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['weight']
        return "-"

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

    def attack(self, enemy):
        if enemy.hp <= 0:
            return f"Противник @{enemy.pokemon_trainer} уже повержен."

        damage = self.power
        enemy.hp -= damage
        if enemy.hp <= 0:
            enemy.hp = 0
            enemy.is_alive = False
            self.post_battle_bonus()
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}!"

        return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}, у противника осталось {enemy.hp} здоровья."

    def post_battle_bonus(self):
        pass

    def info(self):
        return (f"Имя твоего покемона: {self.name}\n"
                f"Сила: {self.power}\n"
                f"Здоровье: {self.hp}\n"
                f"Высота: {self.height}\n"
                f"Ширина: {self.weight}\n"
                f"Способности: {self.abilities}")

    def show_img(self):
        return self.img


class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp += 300
        self.super_shield_used = False

    def attack(self, enemy):
        if not self.super_shield_used and isinstance(enemy, Wizard):
            if randint(1, 5) == 1:
                self.super_shield_used = True
                return f"{self.name} применил щит и уклонился от атаки!"

        return super().attack(enemy)

    def post_battle_bonus(self):
        if not self.super_shield_used:
            self.super_shield_used = True
            heal = randint(20, 50)
            self.hp += heal
            print(f"{self.name} получил супер защиту и восстановил здоровье на {heal}. Текущее здоровье: {self.hp}")

    def info(self):
        base_info = super().info()
        shield_status = "использована" if self.super_shield_used else "не использована"
        return f"У тебя Маг (здоровье увеличено на 300) + супер защита ({shield_status})\n{base_info}"


class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.power += 200
        self.super_strike_used = False

    def attack(self, enemy):
        if not self.super_strike_used and not enemy.is_alive:
            self.super_strike_used = True
            extra_power = randint(50, 100)
            self.power += extra_power
            print(f"{self.name} получил супер удар, сила увеличена на {extra_power}. Текущая сила: {self.power}")

        result = super().attack(enemy)

        if self.hp < 0.5 * 800:
            heal = randint(10, 50)
            self.hp += heal
            print(f"{self.name} восстановил здоровье на {heal}. Текущее здоровье: {self.hp}")

        return result

    def post_battle_bonus(self):
        pass

    def info(self):
        base_info = super().info()
        strike_status = "использован" if self.super_strike_used else "не использован"
        return f"У тебя Боец (сила увеличена на 200) + супер удар ({strike_status})\n{base_info}"


if __name__ == "__main__":
    wizard = Wizard("MageMaster")
    fighter = Fighter("StrongFighter")

    print("Информация о маге:")
    print(wizard.info())
    print("\nИнформация о бойце:")
    print(fighter.info())

    print("\nНачинается бой:")

    while wizard.is_alive and fighter.is_alive:
        print(wizard.attack(fighter))
        if not fighter.is_alive:
            break
        print(fighter.attack(wizard))

    print("\nИтоги боя:")
    print(wizard.info())
    print(fighter.info())

