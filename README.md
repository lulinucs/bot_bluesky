
# Bluesky Bot

Este projeto é uma aplicação Python para interação automática com a rede social Bluesky. A aplicação utiliza a API do Bluesky e a API de linguagem natural da Cohere para gerar respostas automáticas, seguir usuários, e postar frases automáticas com base em interesses pré-definidos.

## Funcionalidades

- **Autenticação e Sessão**: Realiza login na conta Bluesky utilizando credenciais armazenadas em variáveis de ambiente.
- **Notificações**: Recupera e processa notificações do Bluesky, identificando menções, respostas e novos seguidores.
- **Interação Automática**:
  - **Seguir Usuários**: Segue automaticamente novos seguidores e envia uma mensagem de agradecimento.
  - **Responder Menções e Respostas**: Gera e envia respostas automáticas para menções e respostas recebidas.
  - **Postagem Automática**: Publica frases automaticamente em intervalos regulares, baseadas em interesses pré-definidos.
- **Gerenciamento de Estado**: Mantém um registro das notificações já processadas para evitar duplicação de ações.

## Estrutura do Projeto

- `main.py`: Arquivo principal contendo a lógica de autenticação, recuperação de notificações e processamento de interações.
- `gerador_frases.py`: Módulo responsável por gerar frases e respostas utilizando a API da Cohere.
- `interesses.json`: Arquivo JSON contendo uma lista de interesses que são usados para gerar frases temáticas.
- `.env`: Arquivo de configuração com variáveis de ambiente, incluindo credenciais da conta Bluesky e chave da API Cohere.
- `processed_notifications.json`: Arquivo JSON que armazena os IDs das notificações já processadas.

## Dependências

- **Python 3.8+**
- **Bibliotecas Python**:
  - `requests`
  - `os`
  - `json`
  - `time`
  - `dotenv`
  - `atproto` (Biblioteca de interação com a API Bluesky)
  - `cohere` (API de linguagem natural)

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/lulinucs/bot_bluesky
   cd bot_bluesky

2.  **Configure as variáveis de ambiente**: Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:
    
       ```bash
    BLUESKY_HANDLE=seu-handle.bsky.social
    BLUESKY_APP_PASSWORD=sua-senha-app
    COHERE_API_KEY=sua-chave-cohere` 
    
3.  **Prepare o arquivo de interesses**: Edite o arquivo `interesses.json` para incluir os temas sobre os quais deseja que as frases sejam geradas.

## Uso

Execute o script principal:

    python main.py` 

O script irá:

-   Autenticar na conta Bluesky.
-   Verificar notificações a cada 30 minutos.
-   Seguir novos seguidores e responder menções automaticamente.
-   Postar frases automáticas a cada 30 minutos.

## Personalização

-   **Interesses**: Edite o arquivo `interesses.json` para personalizar os temas das frases geradas.
-   **Tempo de Verificação**: O tempo de espera entre as verificações de notificações e postagens automáticas pode ser ajustado modificando o valor em `time.sleep()` na função `main()`.

## Referência

Algumas das funcionalidades deste bot são implementadas utilizando a biblioteca `atproto`, enquanto outras fazem uso da API HTTP do Bluesky. Para obter mais informações, você pode consultar a documentação de ambos os recursos:

- **[Documentação da API HTTP do Bluesky](https://docs.bsky.app/docs/category/http-reference)**: Fornece informações detalhadas sobre os endpoints e a utilização da API HTTP do Bluesky.
  
- **[Documentação da biblioteca atproto para Python](https://atproto.blue/en/latest/)**: Oferece a documentação completa sobre como usar a biblioteca `atproto` para interagir com o Bluesky em Python.
