import telebot 
from random import randint
from config import token
from logic import Pokemon, Wizard, Fighter

# Инициализация бота с токеном
bot = telebot.TeleBot(token) 

# Словарь для хранения покемонов, ключами являются имена пользователей
Pokemon.pokemons = {}

@bot.message_handler(commands=['go'])
def go(message):
    # Проверяем, создал ли пользователь уже покемона
    if message.from_user.username not in Pokemon.pokemons:
        # С вероятностью 20% создаем покемона с супер силой (маг)
        if randint(1, 5) == 1:
            pokemon = Wizard(message.from_user.username)
        else:
            # В противном случае создаем обычного покемона (боец)
            pokemon = Fighter(message.from_user.username)

        # Отправляем изображение и информацию о покемоне
        bot.send_photo(message.chat.id, pokemon.show_img())
        bot.send_message(message.chat.id, pokemon.info())
    else:
        # Если покемон уже создан, уведомляем пользователя
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(func=lambda message: message.reply_to_message is not None and message.text.startswith('/attack'))
def attack(message):
    # Получаем имена атакующего и защитника
    attacker_username = message.from_user.username
    defender_username = message.reply_to_message.from_user.username

    # Проверяем, существуют ли покемоны у обоих игроков
    if attacker_username in Pokemon.pokemons and defender_username in Pokemon.pokemons:
        attacker_pokemon = Pokemon.pokemons[attacker_username]
        defender_pokemon = Pokemon.pokemons[defender_username]

        # Выполняем атаку и получаем результат
        result = attacker_pokemon.attack(defender_pokemon)
        bot.send_message(message.chat.id, result)

        # Проверяем, жив ли защитник после атаки
        if not defender_pokemon.is_alive:
            bot.send_message(message.chat.id, f"{defender_username}, твой покемон повержен!")
    else:
        # Если у одного из игроков нет покемонов, уведомляем об этом
        bot.send_message(message.chat.id, "Убедитесь, что оба игрока создали покемонов.")

@bot.message_handler(commands=['restore'])
def restore_power(message):
    # Получаем имя пользователя
    username = message.from_user.username
    # Проверяем, существует ли покемон у пользователя
    if username in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[username]
        # Восстанавливаем здоровье покемона на случайное значение от 10 до 50
        heal_amount = randint(10, 50)
        pokemon.hp += heal_amount
        bot.send_message(message.chat.id, f"{pokemon.name} восстановил здоровье на {heal_amount}. Текущее здоровье: {pokemon.hp}.")
    else:
        # Если покемон не создан, уведомляем пользователя
        bot.send_message(message.chat.id, "Сначала создайте покемона с помощью команды /go.")

# Запускаем бота
bot.infinity_polling(none_stop=True)