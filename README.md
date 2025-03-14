# Telegram Bot

## Установка

1. Клонируйте репозиторий или скачайте файлы.
2. Установите необходимые зависимости:
   ```bash
   python3.12 (python3.12.7)
   pip install -r requirements.txt
   ```
3. Получите API ID и API HASH:
   - Перейдите на сайт [my.telegram.org](https://my.telegram.org/)
   - Авторизуйтесь с помощью номера телефона
   - Перейдите в раздел "API development tools"
   - Создайте новое приложение и получите `API_ID` и `API_HASH`

4. Создайте `.env` файл и добавьте в него необходимые переменные окружения:
   ```env
   API_ID = your_api_id
   API_HASH = your_api_hash
   BOT_TOKEN = your_bot_token
   ALLOWED_IDS = id1,id2,id3...
   ```

В ALLOWED_IDS нужно указать id аккаунтов, которые смогут управлять ботом.
(id аккаунта можно узнать в боте @getidsbot)

## Использование

Запустите бота командой:
```bash
python3 main.py
```
- Командой ```/help``` и ```/start``` в боте можно узнать список всех команд.

- Команда ```/link``` позволяет указать группы/аккаунты, куда будут приходить полученные сообщения. Можно указать вызвать команду с параметром ```/link csb4hs4p```, тем самым сообщения будут приходить только пользователю @csb4hs4p. Если вызвать команду без параметров ```/link```, то бот предложит отправить файл links.txt, в который можно указать несколь username-ов и id приватных групп (каждое значение с новой строчки)

- Команда ```/getid``` позволяет узнать id приватной группы. В качестве параметра нужно указать название этой группы ```/getid example```. После чего этот id можно передавать в команду ```/link```. Чтобы получить id, нужно добавить бота в приватную группу, id которой вы хотите получить, и написать любое сообщение в эту группу.
-  Команды ```/triggers```, ```/channels``` аналогично команде ```/links``` позволяет загружать файлы triggers.txt и channels.txt, в которых содержатся триггер слова/фразы и названия каналов/групп/чатов которые нужно мониторить (!!! названия, а не никнеймы !!!)


## Логирование
Логи сохраняются в папке `logs/` с временной меткой в названии файла.

## Загрузка файлов
Загруженные файлы сохраняются в папке `downloads/`.


