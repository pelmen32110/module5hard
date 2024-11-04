import hashlib
import time


class User:
    #Атрибуты: nickname(имя пользователя, строка), password(в хэшированном виде, число), age(возраст, число)

    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = self._hash_password(password)
        self.age = age

    def _hash_password(self, password):
        return int(hashlib.sha256(password.encode()).hexdigest(), 16)

    def __str__(self):
        return  self.nickname

class Video:
    #Атрибуты: title(заголовок, строка), duration(продолжительность, секунды),
    # time_now(секунда остановки (изначально 0)), adult_mode(ограничение по возрасту, bool (False по умолчанию))

    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode

class UrTube:
    def __init__(self):
        self.users = [] #список пользователей
        self.current_user = None #текущий пользователь
        self.videos = [] #список видео

    def log_in(self, nickname, password):
        hashed_password = int(hashlib.sha256(password.encode()).hexdigest(), 16)
        for user in self.users:
            if user.nickname == nickname and user.password == hashed_password:
                self.current_user = user
                print(f"Пользователь {user.nickname} успешно вошел.")
                return
        print("Неверные данные для входа.")

    def register(self, nickname, password, age):
        for user in self.users:
            if user.nickname == nickname:
                print(f"Пользователь с ником {nickname} уже существует")
                return
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user
        print(f"Пользователь {nickname} успешно зарегистрирован и вошел.")

    def log_out(self):
        if self.current_user:
            print(f"Пользователь {self.current_user.nickname} вышел.")
            self.current_user = None
        else:
            print("Вы не вошли в систему")

    def __add__(self, *videos):
        for video in videos:
            if not any(v.title == video.title for v in self.videos):
                self.videos.append(video)
                print(f"Видео  '{video.title}' добавлено")
            else:
                print(f"Видео {video.title} уже есть")

    def get_videos(self, search):
        search=search.lower()
        for video in self.videos:
            if search in video.title.lower():
                print(f'{video.title}')

    def watch_video(self, title):
        if not self.current_user:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

            # Find the video
        video = next((v for v in self.videos if v.title == title), None)
        if not video:
            print("Видео не найдено.")
            return

        # Check age restriction
        if video.adult_mode and self.current_user.age < 18:
            print("Вам нет 18 лет, пожалуйста покиньте страницу")
            return

        # Play the video
        print(f"Начало воспроизведения '{title}'")
        for second in range(video.time_now, video.duration+1):
            print(f"Секунда {second}")
            video.time_now += 1
            time.sleep(1)  # Simulate real-time watching

        print("Конец видео")
        video.time_now = 0  # Reset after watching


ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.__add__(v1,v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт  !!!!! Но тут же регистрация другого пользователя !!!!!
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')