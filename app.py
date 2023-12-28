from flask import Flask, request
import sett
import services

app = Flask(__name__)

@app.route('/bemvindo', methods=['GET'])
def bemvindo():
    # Rota de boas-vindas
    return 'Olá mundo! Em que posso ser útil no dia de hoje?'

@app.route('/webhook', methods=['GET'])
def verificar_token():
    # Obtém o token da query parameters
    token = request.args.get('hub.verify_token')
    
    # Verifica se o token recebido é igual ao definido no arquivo de configuração
    if token == sett.token:
        return 'Token correto'
    else:
        return 'Token incorreto'
     
@app.route('/webhook', methods=['POST'])
def receber_mensagens():
    try:
        # Obtém o corpo da requisição como JSON
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        
        # Substitui o início do número de telefone com base em padrões específicos
        number = services.replace_start_brasil(message['from'])
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        

        # Obtém o texto da mensagem do WhatsApp
        text = services.obter_mensagem_whatsapp(message)

        # Chama a função para administrar a lógica do chatbot
        services.administrar_chatbot(text, number, messageId, name)
        
        return 'enviado'

    except Exception as e:
        # Retorna uma mensagem de erro caso haja uma exceção durante o processamento
        return 'Erro ao processar mensagem: ' + str(e), 500

if __name__ == '__main__':
    # Inicia a aplicação Flask
    app.run()
