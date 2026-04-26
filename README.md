# Discord Bot de Mecânica

Este projeto cria um bot Discord em Python que entra em um canal de voz, faz uma contagem regressiva e reproduz áudio em português gerado pelo Google Text-to-Speech (gTTS).

## O que está pronto

- Comando `!entrar` para conectar o bot ao canal de voz do autor
- Comando `!mecanica` para iniciar o loop de mecânica
- Comando `!parar` para interromper o loop e desconectar
- Comando `!sair` para desconectar o bot do canal de voz
- Suporte a `.env` com `python-dotenv`
- `GitHub Actions` para verificar sintaxe Python

## Requisitos

- Python 3.10+
- `ffmpeg` instalado no sistema e disponível no PATH
- Token de bot do Discord

## Instalação

1. Abra o terminal na pasta do projeto.
2. Instale dependências:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Crie um arquivo `.env` a partir do `.env.example`:

```powershell
copy .env.example .env
```

4. Edite `.env` e adicione o token do seu bot:

```text
DISCORD_BOT_TOKEN=SEU_TOKEN_AQUI
```

## Como executar

No terminal:

```bash
python bot.py
```

## Criar repositório no GitHub

1. Copie `.env.example` para `.env`:

```powershell
copy .env.example .env
```

2. Preencha `GITHUB_TOKEN` no arquivo `.env` com um token pessoal do GitHub que tenha permissão para criar e editar repositórios.
3. Crie o repositório e envie os arquivos com o script:

```powershell
python github_upload.py netocarrara/bakragore
```

Se o repositório já existir, o script atualizará os arquivos existentes no branch `main`.

4. Abra a URL do repositório no GitHub.

> O script funciona mesmo sem ter `git` instalado localmente.

## Comandos disponíveis

- `!entrar` - Faz o bot entrar no canal de voz do autor.
- `!mecanica` - Inicia o loop da mecânica com temporizador e aviso sonoro.
- `!parar` - Para o loop e desconecta o bot.
- `!sair` - Desconecta o bot do canal de voz.

## Observações

- `ffmpeg` precisa estar instalado separadamente. No Windows, baixe o pacote pré-compilado e adicione `ffmpeg.exe` ao PATH.
- O bot usa gTTS e precisa de acesso à internet para gerar o áudio.
- O arquivo `.env` não deve ser enviado ao GitHub.

## Subir para o GitHub

```powershell
git init
git add .
git commit -m "Inicializa bot Discord com gTTS"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

Se quiser, posso ajudar a criar o repositório no GitHub e fazer o push passo a passo.
