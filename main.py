import requests
import os
import json
import time
from atproto import Client, client_utils
from gerador_frases import gerar_frase, gerar_resposta, agradecer
from dotenv import load_dotenv


load_dotenv()
BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
BLUESKY_APP_PASSWORD = os.getenv("BLUESKY_APP_PASSWORD")

client = Client(base_url='https://bsky.social')
client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)

PROCESSED_NOTIFICATIONS_FILE = 'processed_notifications.json'

def get_access_token():
    #Função para obter o token de acesso. Algumas funções utilizam a lib atproto e outras utilizam a HTTP API

    response = requests.post(
        "https://bsky.social/xrpc/com.atproto.server.createSession",
        json={"identifier": BLUESKY_HANDLE, "password": BLUESKY_APP_PASSWORD},
    )
    response.raise_for_status()
    session = response.json()
    return session["accessJwt"]

def get_notifications(access_token):
    #Função para obter a lista de notificações.

    url = "https://bsky.social/xrpc/app.bsky.notification.listNotifications"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 401:
        print("Erro de autenticação: Verifique o token de acesso e as permissões.")
        return None
    elif response.status_code == 404:
        print("Endpoint não encontrado: Verifique a URL do endpoint.")
        return None
    else:
        response.raise_for_status()
        return response.json()

def load_processed_notifications():
    #Função para carregar os IDs das notificações já processadas.

    if os.path.exists(PROCESSED_NOTIFICATIONS_FILE):
        with open(PROCESSED_NOTIFICATIONS_FILE, 'r') as file:
            return json.load(file)
    return set()

def save_processed_notifications(processed_notifications):
    #Função para salvar os IDs das notificações já processadas.
    
    with open(PROCESSED_NOTIFICATIONS_FILE, 'w') as file:
        json.dump(list(processed_notifications), file)

def follow_user(user_handle, author_did, author_displayName):
    #Função para seguir um usuário (follow back)

    print(f"Seguindo o usuário: {user_handle} Id: {author_did}")
    uri = client.follow(author_did).uri

    try:
        resposta = agradecer(author_displayName)
        tb = client_utils.TextBuilder()
        tb.text(resposta)
        tb.mention(' @'+user_handle, author_did)
        post = client.send_post(tb)
        print(f"Resposta criada com sucesso: {post.uri}")
        return post.uri
    except Exception as e:
        print(f"Erro ao criar resposta: {e}")
        return None


def mention_user(user_handle, author_did, text):
    #Função para responder um usuário quando ele te menciona.
    
    print(f"Respondendo o usuário: {user_handle}.")
    print(text)

    texto_base = text
    reply = gerar_resposta(texto_base)
    client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)
    tb = client_utils.TextBuilder()
    tb.text(reply)
    tb.mention(' @'+user_handle, author_did)
    post = client.send_post(tb)
    print(f"Resposta criada com sucesso: {post.uri}")


def postar_frase_automatica():
    #Função para postar automaticamente uma frase gerada no Bluesky
    try:
        frase = gerar_frase()
        client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)
        tb = client_utils.TextBuilder()
        tb.text(frase)
        post = client.send_post(tb)
        print(f"Postagem automática criada com sucesso: {post.uri}")
    except Exception as e:
        print(f"Erro ao criar postagem automática: {e}")



def process_notifications(notifications, processed_notifications):
    #Função para processar as notificações recebidas.

    new_processed_notifications = set(processed_notifications)
    for notification in notifications.get('notifications', []):
        notification_id = notification.get('cid')
        
        # Verifica se a notificação já foi processada
        if notification_id in processed_notifications:
            continue
        
        reason = notification.get('reason')
        author_handle = notification.get('author', {}).get('handle')  # Handle do autor da notificação
        post_id = notification.get('cid')  # ID do post associado à notificação
        author_did = notification.get('author', {}).get('did')
        author_displayName = notification.get('author', {}).get('displayName')
        if reason == 'mention' or reason == 'reply':
            # Extrair o handle mencionado do texto do post
            text = notification.get('record', {}).get('text', '')
            mention_user(author_handle, author_did, text)
                
        elif reason == 'follow':
            follow_user(author_handle, author_did, author_displayName)
        else:
            print(f"Notificação com motivo desconhecido: {reason}")
        
        # Adiciona o ID da notificação ao conjunto de notificações processadas
        new_processed_notifications.add(notification_id)

    # Salva as notificações processadas
    save_processed_notifications(new_processed_notifications)

def main():
    while True:
        try:
            access_token = get_access_token()
            if not access_token:
                time.sleep(30*60)
                continue

            notifications = get_notifications(access_token)
            processed_notifications = load_processed_notifications()
            process_notifications(notifications, processed_notifications)
            time.sleep(30*60)
            postar_frase_automatica()

            time.sleep(30*60) 
        except Exception as e:
            time.sleep(10*60)

if __name__ == "__main__":
    main()

