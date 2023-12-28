import requests
import sett
import json
import time



def obter_mensagem_whatsapp(message):
    # Verifica se 'type' está presente na mensagem
    if 'type' not in message:
        text = 'mensagem não reconhecida'
    
    # Se o tipo de mensagem for 'text', extrai o corpo da mensagem
    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']

    return text



def enviar_mensagem_whatsapp(data):
    try:
        # Obtém o token e URL do WhatsApp do arquivo de configuração
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url

        # Define os cabeçalhos para a requisição
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}

        # Envia a mensagem via requisição POST
        response = requests.post(whatsapp_url,
                                 headers=headers, 
                                 data=data)
        # Verifica o código de status da resposta
        if response.status_code == 200:
            return 'mensagem enviada', 200
        else:
            return 'erro ao enviar mensagem', response.status_code
    except Exception as e:
        return 'Erro ao enviar a mensagem: ' + str(e), 403



def text_Message(number, text):
    # Converte os parâmetros em um formato JSON para a mensagem
    data = json.dumps(
        {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data 



def buttonReply_Message(number, options, body, footer, sedd, messageId):
    buttons = []

    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data
    


def ListReply_Message(number, options, body, footer, sedd, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                
                "id": sedd + "_btn_" + str(i + 1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opções",
                    "sections": [
                        {
                            "title": "Seções",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data



def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data



def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data



def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id



def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data




def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data




def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data




def administrar_chatbot(text,number, messageId, name):
    text = text.lower() #mensaje que envio el usuario
    list = []
    print("mensaje del usuario: ",text)

    markRead = markRead_Message(messageId)
    list.append(markRead)
    time.sleep(2)

    if "hola" in text:
        body = "Olá👋 Bemvindo a Henrique Pysolutions, como posso de ajudar?"
        footer = "Equipe Henrique"
        options = ["✅ servicios", "📅 agendar uma conversa comigo"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        replyReaction = replyReaction_Message(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)
    elif "servicios" in text:
        body = "Tenho alguns serviços disponiveis. Quais desses serviços gostaria de explorar?"
        footer = "Equipe Henrique"
        options = ["Automação de WhatsApp", "Automação para instagram", "bot para telegram"]

        listReplyData = ListReply_Message(number, options, body, footer, "sed2",messageId)
        sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))

        list.append(listReplyData)
        list.append(sticker)
    elif "Automação de WhatsApp" in text:
        body = "Boa escolha. Gostaria de receber um PDF com mais informações?"
        footer = "Equipo Bigdateros"
        options = ["✅ Sim, enviar um PDF.", "⛔ Não, obrigado."]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData)
    elif "Sim, enviar um PDF" in text:
        sticker = sticker_Message(number, get_media_id("pelfet", "sticker"))
        textMessage = text_Message(number,"Genial, por favor espera un momento.")

        enviar_mensagem_whatsapp(sticker)
        enviar_mensagem_whatsapp(textMessage)
        time.sleep(3)

        document = document_Message(number, sett.document_url, "Boa 👍🏻", "Automação de WhasApp")
        enviar_mensagem_whatsapp(document)
        time.sleep(3)

        body = "Gostaria de agendar uma reunião comigo para conversar mais sobre esse serviço?"
        footer = "Equipe Henrique"
        options = ["✅ Sim, agendar uma reunião", "NÃO, brigado." ]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed4",messageId)
        list.append(replyButtonData)
    elif "Sim, agendar uma reunião" in text :
        body = "Excelente. Por favor, selecciona una data e  hora para a reunião:"
        footer = "Equipe Henrique"
        options = ["📅 10: manhã 10:00 AM", "📅 7 de Janeiro, 2:00 PM", "📅 8 de Janeiro, 4:00 PM"]

        listReply = ListReply_Message(number, options, body, footer, "sed5",messageId)
        list.append(listReply)
    elif "7 de janeiro, 2:00 pm" in text:
        body = "Excelente, Foi selecionado uma reunião para 7 de janeiro às 2:00 PM. Te enviarei um lembrete um dia antes. Necessita de algo amais?"
        footer = "Equipe Henrique"
        options = ["✅ Sim, por favor", "❌ Não, obrigado."]


        buttonReply = buttonReply_Message(number, options, body, footer, "sed6",messageId)
        list.append(buttonReply)
    elif "Não, obrigado." in text:
        textMessage = text_Message(number,"Perfeito! Lembre-se também, que tenho serviços gratuitos de análise de bugs😊")
        list.append(textMessage)
    else :
        data = text_Message(number,"Desculpe, Não entendi o que digitou. Quer que eu te ajude com mais alguma outra opção?")
        list.append(data)

    for item in list:
        enviar_mensagem_whatsapp(item)

#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.

def replace_start_brasil(s):
    if s.startswith("55"):
        return "55" + s[2:]
    else:
        return s