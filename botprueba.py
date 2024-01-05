import telebot
import json
from datetime import datetime
import random
from difflib import SequenceMatcher

token = "6927816640:AAEhaTzLmHGcSb5_v96zv7iOp9P516TwADQ"
bot = telebot.TeleBot(token)

quien_es_presidente_activada = False
umbral_confianza = 0.6 

with open('intenciones.json', 'r') as file:
    intents_data = json.load(file)["intents"]

def calcular_similitud(palabra_clave, mensaje):
    return SequenceMatcher(None, palabra_clave, mensaje).ratio()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Bienvenido al chatBot de la república de Colombia")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    global quien_es_presidente_activada

    mensaje = message.text.lower()

    for intent in intents_data:
        max_similitud = max(calcular_similitud(palabra_clave, mensaje) for palabra_clave in intent["palabras_clave"])
        
        if quien_es_presidente_activada and any(palabra_clave in mensaje for palabra_clave in ["nacio", "nacimiento", "presidente"]):
                respuesta_local = "El presidente de Colombia nació en {lugar_nacimiento}."
                bot.send_message(message.chat.id, respuesta_local.format(lugar_nacimiento="Ciénaga de Oro"))
                quien_es_presidente_activada = False 
                return

        if max_similitud > umbral_confianza:
            if intent["tag"] == "quien_es_presidente":
                quien_es_presidente_activada = True
            else:
                quien_es_presidente_activada = False

            respuesta = random.choice(intent["respuestas"])
            if intent["tag"] == "saludo":
                bot.reply_to(message, respuesta)
                return
            if intent["tag"] == "despedida":
                bot.reply_to(message,respuesta)
                return 
            mensaje_respuesta = respuesta.format(hora=str(datetime.now().time())[:5], fecha=str(datetime.now().date()))
            bot.send_message(message.chat.id, mensaje_respuesta)
            return
        
    bot.reply_to(message, "No entendí tu mensaje.")

bot.infinity_polling()
