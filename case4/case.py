

import random
import json
import os


class GameStats:
    # Класс для управления статистикой игр
    # Инициализируем начальные значения для объекта
    def __init__(self):
        # Название файла
        self.stats_file = 'game_stats.json'
        # Сколько раз играли
        self.games_played = 0
        # Сколько раз выиграли
        self.games_won = 0
        # Число попыток по умолчанию
        self.total_attempts = 0
        # Определяем лучшый результат
        self.best_score = float('inf')
        # Загружаем статистику
        self.load_stats()

    # Загружает статистику из файла
    def load_stats(self):
        try:
            # Проверяем, что файл со статистикой существует
            if os.path.exists(self.stats_file):
                # Безопасно открываем файл
                # Не нужно делать file.open и file.close(), что бы не произошла утечка по пямяти
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.games_played = data.get('games_played', 0)
                    self.games_won = data.get('games_won', 0)
                    self.total_attempts = data.get('total_attempts', 0)
                    self.best_score = data.get('best_score', float('inf'))
        except Exception as e:
            print("Не удалось загрузить статистику: {}".format(e))

    def save_stats(self):
        # Сохраняет статистику в файл
        try:
            data = {
                'games_played': self.games_played,
                'games_won': self.games_won,
                'total_attempts': self.total_attempts,
                'best_score': self.best_score
            }
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Не удалось сохранить статистику: {}".format(e))
            raise SystemExit

    def update_stats(self, won, attempts):
        # Обновляет статистику после игры
        # делаем +1 к игре и +1 к попыткам ( учитывая старый результат total_attempts )
        self.games_played += 1
        self.total_attempts += attempts

        # Если выиграли
        if won:
            # + 1 к победе
            self.games_won += 1
            # Если результат меньше, записывается лучший результат ( best_score )
            if attempts < self.best_score:
                self.best_score = attempts

        self.save_stats()

    def display_stats(self):
        # Отображает текущую статистику
        # Защита от ZeroDivisionError: Использование тернарного оператора (if ... else ...) предотвращает падение программы, если игр еще не было (games_played = 0)
        win_rate = (self.games_won / self.games_played * 100) if self.games_played > 0 else 0
        avg_attempts = (self.total_attempts / self.games_played) if self.games_played > 0 else 0

        # Выплёвываем результат
        print("\n" + "=" * 50)
        print("📊 СТАТИСТИКА ИГР")
        print("=" * 50)
        print("🏆 Сыграно игр: {}".format(self.games_played))
        print("🎯 Побед: {} ({:.1f}%)".format(self.games_won, win_rate))
        print("📊 Среднее число попыток: {:.1f}".format(avg_attempts))

        if self.best_score != float('inf'):
            print("⭐ Лучший результат: {} попыток".format(self.best_score))
        print("=" * 50 + "\n")


class NumberGuessingGame:
    # Основной класс игры 'Угадай число'
    # Цвета для вывода в консоль
    COLORS = {
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'blue': '\033[94m',
        'reset': '\033[0m'
    }

    # Инициализируем начальные значения для объекта
    def __init__(self, min_num=1, max_num=100, max_attempts=10):
        # Инициализация игры
        # Args:
        #     min_num (int) -> Минимальное число диапазона
        #     max_num (int) -> Максимальное число диапазона
        #     max_attempts (int )-> Максимальное количество попыток

        self.min_number = min_num
        self.max_number = max_num
        self.max_attempts = max_attempts
        self.secret_number = None
        self.attempts = 0
        self.stats = GameStats()

    def print_colored(self, text, color='reset'):
        # Выводим текст с цветом
        print(f"{self.COLORS.get(color, self.COLORS['reset'])}{text}{self.COLORS['reset']}")

    def generate_number(self):
        # Генерируем случайное число в заданном диапазоне
        self.secret_number = random.randint(self.min_number, self.max_number)

    def display_welcome(self):
        # Отображает приветственное сообщение и правила
        print("\n" + "=" * 50)
        self.print_colored("=== ИГРА \"УГАДАЙ ЧИСЛО\" ===", 'green')
        print("=" * 50)

        print("Добро пожаловать в игру!\n")
        print("Я загадал число от {} до {}.".format(self.min_number, self.max_number))
        print("У вас есть {} попыток, чтобы угадать его.".format(self.max_attempts))
        print("Правила игры:")
        print("• Вводите числа в указанном диапазоне")
        print("• После каждой попытки я буду подсказывать")
        print("• Сможете ли вы угадать число?")
        print("=" * 50 + "\n")

    def get_hint(self, guess):
        # Сценарий предоставляет подсказку на основе предыдущей догадки
        #
        # Args:
        #     guess (int): Предполагаемое число
        #
        # Returns:
        #     str: Текст подсказки
        #
        difference = abs(self.secret_number - guess)

        if difference <= 5:
            return "🔥 Горячо! Совсем рядом!"
        elif difference <= 10:
            return "🌡️ Тепло! Уже близко"
        elif difference <= 20:
            return "💧 Прохладно"
        else:
            return "❄️ Холодно! Далеко"

    def validate_input(self, user_input):
        # Проверяет корректность введенного пользователем числа
        #
        # Args:
        #    user_input (str): Введенная пользователем строка
        #
        # Returns:
        #    tuple: (bool, int/str) - (успех, значение или сообщение об ошибке)

        try:
            number = int(user_input)

            # Проверяем заданный диаппазон min_number и max_number
            if number < self.min_number:
                return False, "Число должно быть не меньше {}".format(self.min_number)
            if number > self.max_number:
                return False, "Число должно быть не больше {}".format(self.max_number)
            return True, number

        except ValueError:
            return False, "Пожалуйста, введите целое число"
        except Exception as e:
            return False, "Ошибка ввода: {}".format(e)

    def play_round(self):
        # Проводит один раунд игры
        self.generate_number()
        self.attempts = 0
        guesses_history = []

        print("\n🔮 Новая игра! Попробуйте угадать число...")

        while self.attempts < self.max_attempts:
            self.attempts += 1
            remaining = self.max_attempts - self.attempts

            print("\n" + "=" * 40)
            print("Попытка {} из {}".format(self.attempts, self.max_attempts))

            # В цикле ожидаем предложение по вводу числа
            while True:
                user_input = input("Введите ваше предположение: ").strip()

                # Проверка на специальные команды, если введём exit то выйдем
                if user_input.lower() == 'exit':
                    print("Игра прервана пользователем.")
                    return False

                is_valid, result = self.validate_input(user_input)

                if is_valid:
                    guess = result
                    break
                else:
                    self.print_colored("❌ Ошибка: {}".format(result), 'red')

            # Добавляем в историю
            guesses_history.append(guess)

            # Проверка числа
            if guess == self.secret_number:
                self.print_colored("\n🎉 Поздравляю! Вы угадали число {}!".format(self.secret_number), 'green')
                self.print_colored("Количество попыток: {}".format(self.attempts), 'yellow')

                # Показываем историю догадок
                print("\nВаши догадки: {}".format(', '.join(map(str, guesses_history))))

                return True

            # Подсказка болше или меньше
            if guess < self.secret_number:
                self.print_colored("Больше! Попробуйте число повыше.", 'blue')
            else:
                self.print_colored("Меньше! Попробуйте число пониже.", 'blue')

            # Даём подсказку о близости (после 3-й попытки)
            if self.attempts >= 3:
                hint = self.get_hint(guess)
                print("Подсказка: {}".format(hint))

            # Показываем оставшeecя количество попыток
            if remaining > 0:
                print("Осталось попыток: {}".format(remaining))

            # Отображаем историю догадок
            if len(guesses_history) > 1:
                print("Ваши предыдущие догадки: {}".format(', '.join(map(str, guesses_history[:-1]))))

        # Отображаем если игрок проиграл
        self.print_colored("\n😢 К сожалению, вы не угадали число {}.".format(self.secret_number), 'red')
        print("Попытки закончились!")
        return False

    def play(self):
        # Основной игровой цикл
        while True:
            # Отображаем статистику перед игрой
            if self.stats.games_played > 0:
                self.stats.display_stats()
            else:
                self.display_welcome()

            # Играем раунд
            won = self.play_round()

            # Обновляем статистику
            self.stats.update_stats(won, self.attempts if won else self.max_attempts)

            # Спрашиваем о повторной игре, если нет, тогда отображаем статистику
            print("\n" + "=" * 40)
            while True:
                play_again = input("Хотите сыграть еще раз? (да/нет): ").strip().lower()

                if play_again in ['да', 'yes', 'y', 'д']:
                    break
                elif play_again in ['нет', 'no', 'n', 'н']:
                    self.print_colored("\nСпасибо за игру! До свидания!", 'green')

                    # Отображаем финальную статистику
                    print("\n" + "=" * 50)
                    self.print_colored("ИТОГОВАЯ СТАТИСТИКА СЕССИИ", 'yellow')
                    self.stats.display_stats()

                    return
                else:
                    # Если ввели неправильно ввели ДА или НЕТ.
                    self.print_colored("Пожалуйста, введите 'да' или 'нет'", 'red')


def main():
    # Основной фунционал, где можем поменять экземпляр для игры и запустить прилагу
    try:
        # Создаем экземпляр игры с настройками по умолчанию
        game = NumberGuessingGame(min_num=1, max_num=100, max_attempts=10)

        # Запускаем игру
        game.play()

    # Проверяем, что программа прервалась пользователем
    except EOFError:
        print("\nПрограмма прервана пользователем (Ctrl+D)\nДо свидания!")
        raise SystemExit
    # Проверяем, что программа прервалась пользователем
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем (Ctrl+C)\nДо свидания!")
        raise SystemExit
    except Exception as e:
        print("\nПроизошла непредвиденная ошибка: {}\nПожалуйста, перезапустите программу.".format(e))
        raise SystemExit

if __name__ == "__main__":
    main()