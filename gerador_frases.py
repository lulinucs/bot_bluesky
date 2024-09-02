import cohere
import random
from dotenv import load_dotenv
import os
import json

load_dotenv()
COHERE_API_KEY = os.getenv('COHERE_API_KEY')
co = cohere.Client(COHERE_API_KEY)


def carregar_interesses(caminho_arquivo='interesses.json'):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            interesses = json.load(arquivo)
            return interesses
    except Exception as e:
        print(f"Erro ao carregar o arquivo de interesses: {e}")
        return []

def limpar_aspas(texto):
    #Remove aspas simples e duplas da frase gerada.
    return texto.replace('"', '').replace("'", '')

def gerar_frase():
    #Escolhe um interesse aletoriamente do arquivo interesses.json e gera uma frase
    interesses = carregar_interesses()
    if not interesses:
        return "Não foi possível carregar a lista de interesses."

    interesse = random.choice(interesses)
    #Edite o prompt abaixo para dar personalidade ao seu bot, tente manter o termo "poucas palavras" para respeitar o limite de caracteres do BlueSky.
    mensagem = f"Você é um criador de conteúdo criativo que usa poucas palavras. Crie uma frase sobre o seguinte tema: {interesse}"

    try:
        # Tenta gerar a frase duas vezes
        for _ in range(2):
            response = co.chat(message=mensagem)
            frase_gerada = limpar_aspas(response.text.strip())
            
            # Verifica se a frase gerada é menor que 270 graphemes
            if len(frase_gerada) <= 270:
                return frase_gerada
            
        # Se ambas as tentativas excederem o limite, trunca a frase
        return frase_gerada[:270] + '...'
    
    except Exception as e:
        print(f"Erro ao gerar a frase: {e}")
        return "Desculpe, houve um erro ao gerar a frase."

def gerar_resposta(texto_base):
    #Função para gerar uma resposta quando alguém interage com seu bot.
    
    #Aqui você pode editar este prompt também, para dar personalidade nas respostas.
    mensagem = f"Você é um criador de conteúdo espirituoso que usa poucas palavras. Crie uma resposta para a seguinte frase: {texto_base}"

    try:
        # Tenta gerar a resposta duas vezes
        for _ in range(2):
            response = co.chat(message=mensagem)
            resposta = limpar_aspas(response.text.strip())
            
            # Verifica se a resposta gerada é menor que 270 graphemes
            if len(resposta) <= 270:
                return resposta
            
        # Se ambas as tentativas excederem o limite, trunca a resposta
        return resposta[:270] + '...'
    
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        return "Desculpe, houve um erro ao gerar a resposta."

def agradecer(author_displayName):
    #Função para gerar uma frase de agradecimento quando alguém segue seu bot.

    mensagem = f"Você é um criador de conteúdo espirituoso que usa poucas palavras. Agradeça ao {author_displayName} por te seguir no Bluesky."
    try:
        # Tenta gerar a frase duas vezes
        for _ in range(2):
            response = co.chat(message=mensagem)
            frase_gerada = limpar_aspas(response.text.strip())
            
            # Verifica se a frase gerada é menor que 270 graphemes
            if len(frase_gerada) <= 270:
                return frase_gerada
            
        # Se ambas as tentativas excederem o limite, trunca a frase
        return frase_gerada[:270] + '...'
    
    except Exception as e:
        print(f"Erro ao gerar a frase: {e}")
        return "Desculpe, houve um erro ao gerar a frase."
