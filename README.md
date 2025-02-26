# BotWatcher

## Установка


1. Скачайте файл main.py и requirements.txt.
2. Установите необходимые зависимости:
   ```bash
   python3.12 (python3.12.7)
   pip install -r requirements.txt
   ```
3. Создайте `.env` файл и добавьте в него необходимые переменные окружения, например:
   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   ```
4. Убедитесь, что у вас есть файл `config.ini`. Если его нет, скрипт создаст его автоматически.

## Использование

Запустите бота командой:
```bash
python main.py
```

## Логирование
Логи сохраняются в папке `logs/` с временной меткой в названии файла.

## Загрузка файлов
Файлы сохраняются в папке `downloads/`.

## Авторы
* **Vinogradov Artyom Valerievich**

