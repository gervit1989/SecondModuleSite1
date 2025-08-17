#Данные JSON
import json
#Работа с файлами
import os
# логирование
import logging
#Библиотека изображений
from PIL import Image
# Конфигурация
from configuration import *
from environment_holder import get_env_variable

# Основная программа запуска
def run():
    logging.info('Старт работы программы')
    pass

# запуск
if __name__ == '__main__':
    try:
        # Получаем пути для настройки
        uploads, logs = get_paths()

        #Готовим директории
        os.makedirs(os.path.dirname(logs), exist_ok=True)
        os.makedirs(uploads, exist_ok=True)

        # Настраиваем логирование
        logging.basicConfig(
            filename=logs,
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s: %(message)s'
        )

        # Идем на запуск
        run()
    # пропускаем перезапуск - не ошибка
    except KeyboardInterrupt:
        print('Прерывание выполнения программы')
    finally:
        logging.info('Сеанс завершен')
