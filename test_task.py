import time
import random
from queue import Queue


class TrafficLight:
    def __init__(self, id):
        self.id = id
        self.state = 'RED'  # Начальное состояние
        self.queue = Queue()# Очередь
        self.car_count = 0 # начальное количество машин
        self.human_count = 0 # Начальное количесво пешеходов

        self.car_green_time = 3  # Время зеленого света для автомобилей
        self.car_red_time = 5  # Время красного света для автомобилей

        self.human_green_time = 7  # Время зеленого света для пешеходов
        self.human_red_time = 10 # Время красного света для пешеходов

    def update_counts(self, car_count, human_count):#Функция обновления количества машин и пешеходов
        self.car_count = car_count
        self.human_count = human_count

    def send_event(self, traffic_light_id, event):# Отправка события другому светофору        
        traffic_lights[traffic_light_id].queue.put(event)

    def adapt_traffic(self):# Адаптация времени зеленого света в зависимости от машин и пешеходов
        if self.car_count > 10:
            self.car_green_time = 15

        elif self.car_count > 5:
            self.car_green_time = 12
        else:
            self.car_green_time = 10

        if self.human_count > 5:
            self.human_green_time = 10
        else:
            self.human_green_time = 7

    def run(self):
        self.adapt_traffic()
        print(f"Светофор {self.id} текущее состояние: {self.state}, Машин в ожидании: {self.car_count}, Людей в ожидании: {self.human_count}\n"
              f"Время для проезда состоявляет {self.car_green_time}, время для прохода пешеходов состоявлет {self.human_green_time}")

        if self.state == 'RED':
            print(f"Светофор {self.id} красный для машин, зеленый для пешеходов\n")
            self.state = 'GREEN'
            self.send_event((self.id + 1) % len(traffic_lights), {'type': 'STATE_CHANGE', 'new_state': 'RED'})
            self.send_event((self.id + 4) % len(traffic_lights), {'type': 'PEDESTRIAN_STATE_CHANGE', 'new_state': 'RED'})
            time.sleep(self.car_red_time)
            
        else:
            print(f"Светофор {self.id} зеленый для машин, красный для пешеходов\n")
            self.state = 'RED'
            self.send_event((self.id + 1) % len(traffic_lights), {'type': 'STATE_CHANGE', 'new_state': 'GREEN'})
            self.send_event((self.id + 4) % len(traffic_lights), {'type': 'PEDESTRIAN_STATE_CHANGE', 'new_state': 'GREEN'})
            time.sleep(self.car_green_time)

            
            

# Инициализация автомобильных и пешеходных светофоров
traffic_lights = [TrafficLight(i) for i in range(12)]  

# Симуляция работы светофоров с ограничением на количество итераций
for _ in range(10):  # Ограничение на количество итераций
    for light in traffic_lights:        
        light.update_counts(random.randint(0, 20), random.randint(0, 8))
        light.run()
