#Работа с файлами
import os
# логирование
import logging
# Конфигурация
from configuration import *
from environment_holder import get_env_variable
from http.server import BaseHTTPRequestHandler, HTTPServer
from server import ImageServer

# Основная программа запуска
def run():
    logging.info('Старт работы программы')
    host = get_env_variable('HOST')
    port_arg = get_env_variable('PORT')
    port_num = 0
    try:
        port_num = int(port_arg)
        logging.info(f'host: {host}\nport: {port_num}\n')
        server_address = (host, port_num)
        httpd = HTTPServer(server_address, ImageServer)
        httpd.serve_forever()
    except ValueError:
        logging.info('Port is not int\nNot runned')

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
            format='[%(asctime)s] %(levelname)s: %(message)s',
            mode='w'
        )

        # Идем на запуск
        run()
    # пропускаем перезапуск - не ошибка
    except KeyboardInterrupt:
        print('Прерывание выполнения программы')
    finally:
        logging.info('Сеанс завершен')
