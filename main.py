from pyrogram import Client, filters, compose
from dotenv import load_dotenv
from datetime import datetime
import asyncio, configparser, requests, os, logging, time
import re

current_date = datetime.now().date()
time_data = datetime.fromtimestamp(int(time.time()))
current_directory = os.path.dirname(os.path.abspath(__file__))

if 'logs' not in os.listdir(current_directory):
    os.mkdir(f'{current_directory}/logs')
if 'downloads' not in os.listdir(current_directory):
    os.mkdir(f'{current_directory}/downloads')
if 'config.ini' not in os.listdir(current_directory):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'updated': '0', 'links': '', 'channels': ''}
    with open(f'{current_directory}/config.ini', 'w') as configfile:
        config.write(configfile)
logging.basicConfig(level=logging.INFO, filename=f"{current_directory}/logs/logs_{time_data}.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")


load_dotenv()
API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ALLOWED_IDS = list(map(int, os.getenv("ALLOWED_IDS", "").split(',')))

if not all([API_ID, API_HASH, BOT_TOKEN, ALLOWED_IDS]):
    logging.critical("Отсутствуют обязательные переменные окружения")
    exit(1)

async def main():
    app = Client("my_accountq", api_id=API_ID, api_hash=API_HASH)
    bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    apps = [app, bot]

    @app.on_message()
    async def log(client, message):
        config = configparser.ConfigParser()
        config.read(f"{current_directory}/config.ini")
        chats_for_sending = config['DEFAULT']['links']
        chats_for_sending = [i.strip() for i in chats_for_sending.split(',') if i.strip()]

        monitored_channels = config['DEFAULT']['channels']
        
        try:
            with open(f"{current_directory}/downloads/triggers.txt", "r") as f:
                triggers = f.read().splitlines()
        except:
            logging.critical("Отсутствует файл с триггерами")
            triggers = ['ponylab']
        
        if message.chat.title in [i.strip() for i in monitored_channels.split(',') if i.strip()]:
            message_text = message.text
            chat_message = message_text.lower()
            for trigger in triggers:
                if re.search(fr'{trigger}', chat_message) :
                    if message.outgoing == True and message.reply_to_message_id != None:
                        msg = f"Получено сообщение t.me/c/{str(message.chat.id)[4:]}/{message.id}\n{message.text}"
                        logging.info(f"Получено сообщение t.me/c/{str(message.chat.id)[4:]}/{message.id} {message.text.replace('\n', ' ')}")

                        for chat_id in chats_for_sending:
                            try:
                                chat_id = int(chat_id)
                                await bot.send_message(chat_id=chat_id, text=msg)
                            except:
                                await bot.send_message(chat_id=chat_id, text=msg)
                    elif message.outgoing == True and  message.reply_to_message_id == None:
                        if message.from_user is None:
                            if message.chat.username is None:
                                msg = f"Получено сообщение t.me/c/{str(message.chat.id)[4:]}/{message.id}:\n{message.text}"
                                logging.info(f"Получено сообщение t.me/c/{str(message.chat.id)[4:]}/{message.id}: {message.text.replace('\n', ' ')}")
                            else:
                                msg = f"Получено сообщение t.me/{message.chat.username}/{message.id}:\n{message.text}"
                                logging.info(f"Получено сообщение t.me/{message.chat.username}/{message.id}: {message.text.replace('\n', ' ')}")
                        else:
                            if message.chat.username is None:
                                msg = f"Получено сообщение от пользователя @{message.from_user.username} (id: {message.from_user.id}) в приватном чате {message.chat.title}:\n{message.text}"
                                logging.info(f"Получено сообщение от пользователя @{message.from_user.username} (id: {message.from_user.id}) в приватном чате {message.chat.title}: {message.text.replace('\n', ' ')}")
                            else:
                                msg = f"Получено сообщение от пользователя @{message.from_user.username} (id: {message.from_user.id}) t.me/{message.chat.username}/{message.id}:\n{message.text}"
                                logging.info(f"Получено сообщение от пользователя @{message.from_user.username} (id: {message.from_user.id}) t.me/{message.chat.username}/{message.id}: {message.text.replace('\n', ' ')}")

                        for chat_id in chats_for_sending:
                            try:
                                chat_id = int(chat_id)
                                await bot.send_message(chat_id=chat_id, text=msg)
                            except:
                                await bot.send_message(chat_id=chat_id, text=msg)
                    
                    return
                    
    
    @bot.on_message(filters.command(["start", "help"]))
    async def bot_func(client, message):
        if message.from_user.id not in ALLOWED_IDS:
            await message.reply_text("У вас нет прав для использования этого бота")
            return
        
        await message.reply_text("""/start - вывод всех команд\n/links - задать пользователя или чаты для уведомлений (в формате /links username или файл с ID)\n/getid - возвращает id закрытого чата\n/triggers - загрузить список триггерных слов\n/channels - загрузить список каналов для мониторинга""", disable_web_page_preview=True)
    
    
    @bot.on_message(filters.command("link"))
    async def bot_func(client, message):
        if message.from_user.id not in ALLOWED_IDS:
            await message.reply_text("У вас нет прав для использования этого бота")
            return
        
        args = message.text.split()[1:]
        if not args:
            await message.reply_text("Отправьте текст, содержащий ID чата или пользователя(никнейм), куда бот будет отправлять сообщения.")
        else:
            config = configparser.ConfigParser()
            config.read(f"{current_directory}/config.ini")
            config['DEFAULT']['links'] = ",".join(args)
            with open(f'{current_directory}/config.ini', 'w') as configfile:
                config.write(configfile)
            await message.reply_text(f"Теперь сообщения будут отправляться в чат {' '.join(args)}", disable_web_page_preview=True)
    
    @bot.on_message(filters.command("links"))
    async def bot_func(client, message):
        if message.from_user.id not in ALLOWED_IDS:
            await message.reply_text("У вас нет прав для использования этого бота")
            return

        args = message.text.split()[1:]
        if not args:
            await message.reply_text("Отправьте файл (links.txt), содержащий ID чатов или пользователей(никнеймы), куда бот будет отправлять сообщения (каждый ID с новой строки).")
        else:
            config = configparser.ConfigParser()
            config.read(f"{current_directory}/config.ini")
            config['DEFAULT']['links'] = ",".join(args)
            with open(f'{current_directory}/config.ini', 'w') as configfile:
                config.write(configfile)
            await message.reply_text(f"Теперь сообщения будут отправляться в чат {' '.join(args)}", disable_web_page_preview=True)


    @bot.on_message(filters.command("triggers"))
    async def bot_func(client, message):
        if message.from_user.id not in ALLOWED_IDS:
            await message.reply_text("У вас нет прав для использования этого бота")
            return
        
        await message.reply_text("Отправьте файл (triggers.txt), содержащий триггерные слова (каждое слово с новой строки).")

    @bot.on_message(filters.command("channels"))
    async def bot_func(client, message):
        if message.from_user.id not in ALLOWED_IDS:
            await message.reply_text("У вас нет прав для использования этого бота")
            return
        
        await message.reply_text("Отправьте файл (channels.txt), содержащий названия каналов для мониторинга (каждое название с новой строки).")

    @bot.on_message(filters.command("getid"))
    async def bot_func(client, message):
        if message.from_user.id not in ALLOWED_IDS:
            await message.reply_text("У вас нет прав для использования этого бота")
            return
        
        name_of_chat = " ".join(message.text.split()[1:])
        if not name_of_chat:
            await message.reply_text("Вы не указали название чата, для которого хотите узнать id")
        else:
            url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
            req = requests.get(url=url)
            if req.status_code != 200:
                logging.critical("Проблемы с API телеграмма")
                await message.reply_text("API телеграмма упал :(")
                return

            src = req.json()['result']
            for page in src:
                try:
                    if page['message']['chat']['title'] == name_of_chat:
                        await message.reply_text(f"ID вашего чата: {page['message']['chat']['id']}", disable_web_page_preview=True)
                        break
                except KeyError:
                    pass
            else:
                await message.reply_text("Чат не найден. Возможно, он пуст, отправьте туда любое сообщение.")


    @bot.on_message(filters.document)
    async def handle_file(client, message):
        if message.from_user.id not in ALLOWED_IDS:
            await message.reply_text("У вас нет прав для использования этого бота")
            return
        
        file_path = await message.download()
        file_name = message.document.file_name

        with open(file_path, "r") as f:
            lines = f.read().splitlines()

        if file_name == "links.txt":
            config = configparser.ConfigParser()
            config.read(f"{current_directory}/config.ini")
            config['DEFAULT']['links'] = ",".join(lines)
            with open(f'{current_directory}/config.ini', 'w') as configfile:
                config.write(configfile)
            await message.reply_text("Список чатов обновлен!")
        elif file_name == "triggers.txt":
            with open(f"{current_directory}/downloads/triggers.txt", "w") as f:
                f.write("\n".join(lines))
            await message.reply_text("Список триггерных слов обновлен!")
        elif file_name == "channels.txt":
            config = configparser.ConfigParser()
            config.read(f"{current_directory}/config.ini")
            config['DEFAULT']['channels'] = ",".join(lines)
            with open(f'{current_directory}/config.ini', 'w') as configfile:
                config.write(configfile)
            await message.reply_text("Список отслеживаемых каналов обновлен!")
        else:
            await message.reply_text("Неизвестный файл. Отправьте links.txt, triggers.txt или channels.txt для обновления данных.")
        
        config = configparser.ConfigParser()
        config.read(f"{current_directory}/config.ini")
        links_return = config['DEFAULT']['links'].replace(',', ', ')
        channels_return = config['DEFAULT']['channels'].replace(',', ', ')
        try:
            with open(f'{current_directory}/downloads/triggers.txt', 'r') as f:
                data = f.read().splitlines()
                triggers_return = ", ".join(data)
        except FileNotFoundError:
            triggers_return = ""

        await message.reply_text(f"Новый список групп/юзернеймов для возврата сообщений: {links_return}\nНовый список каналов для мониторинга: {channels_return}\nНовый список триггеров: {triggers_return}")
    
    

    @bot.on_message(filters.text & filters.private)
    async def unknown_command(client, message):
        if message.from_user.id not in ALLOWED_IDS:
            await message.reply_text("У вас нет прав для использования этого бота")
            return
        
        await message.reply_text("Неизвестная команда! Доступные команды:\n/help, /start, /links, /getid, /triggers, /channels")
    
    await compose(apps)

if __name__ == "__main__":
    asyncio.run(main())
