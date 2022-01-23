# **GalbiBot**
Un bot leggero basato su py-cord facile da hostare sul cloud

![help](https://i.imgur.com/0NSq11M.png)  ![info](https://i.imgur.com/l8ss3iI.png)

# Guida installazione su una macchina

**Per far funzionare il bot devi aver installato python e Git**

Scarica python [qui](https://www.python.org/downloads/).
Scarica Git [qui](https://git-scm.com/downloads)

Installa i requisiti:

`pip install -r requirements.txt`

#### Inserisci il token e il client id del tuo bot nel `.env` (Ottieni il token e il client id [qui](https://discord.com/developers/applications))
`TOKEN =metti il tuo token qui` `CLIENT_ID =metti il tuo Client ID

Avvia il bot

`py main.py` o `python3 main.py`

# Deploy su heroku

### ATTENZIONE **Prima di prosegure è necessario avere un account heroku se non lo hai crealo [qui](https://signup.heroku.com/login)**

[![](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https://github.com/Galbaninoh/GalbiBot)

# Generare il link d'invito

Per generare il link d'invito basta che sostituisci CLIENT_ID nel link qua sotto con il client id del tuo bot.

https://discord.com/oauth2/authorize?client_id=CLIENT_ID&permissions=8&scope=applications.commands%20bot

