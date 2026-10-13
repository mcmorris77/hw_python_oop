class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories


    def get_message(self) -> str:
        """Вернуть строчку с информацией о тренировке"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч; ' 
                f'Потрачено ккал: {self.calories:.3f}.')

M_IN_KM = 1000

class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65 # В метрах (шаг, гребок)

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79 
    def get_spent_calories(self):
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                    + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / M_IN_KM 
                    * self.duration * 60)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_TO_MS = 0.278
    CM_TO_M = 100

    def __init__(self, 
                 action: int, 
                 duration: float, 
                 weight:float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        speed_ms = self.get_mean_speed() * self.KMH_TO_MS
        height_m = self.height / self.CM_TO_M

        calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight 
                     + (speed_ms**2 / height_m) * self.CALORIES_SPEED_HEIGHT_MULTIPLIER 
                     * self.weight) * self.duration * 60)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1
    LEN_STEP = 1.38
    CALORIES_WEIGHT_MULTIPLIER = 2

    def __init__(self, 
                 action: int, 
                 duration: float, 
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None :
        super().__init__(action, duration, weight)
        self.length_pool = length_pool # Длинна бассейна в метрах
        self.count_pool = count_pool # Сколько раз пользователь переплыл бассейн

    def get_distance(self):
        distance = self.length_pool * self.count_pool / M_IN_KM
        return distance


    def get_mean_speed(self) -> float:
        mean_speed = self.get_distance() / self.duration
        return mean_speed
    

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_MULTIPLIER) 
                     * self.CALORIES_WEIGHT_MULTIPLIER 
                     * self.weight * self.duration)
        return calories
        

WORKOUT_TYPES = {
    'RUN': Running,
    'WLK': SportsWalking,
    'SWM': Swimming
}

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчика."""
    return WORKOUT_TYPES[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

