# McWhitelistBot
## [EN]
A Discord bot that allows you to whitelist players on a Minecraft server.

### How it works
1. A player creates a request for whitelisting a certain account by typing `.whitelist [Minecraft username]` into a text channel on the Discord server.
2. A previosly defined text channel gets a private message by the bot where admins can decide whether the player is allowed to get whitelisted or not.
3. The player is added to a database which can then be accessed by a Minecraft plugin.

### Requirements
* A minecraft server
* A database
* A Discord server
* One Discord bot per Minecraft server (available via the [Discord developer portal](https://discord.com/developers/applications))

### Environment variables
* `LOGGING_LEVEL`
* `BOT_TOKEN`: Token for the Discord bot
* `SERVER IP`: The Minecraft Server IP (just for informing the players about it)
* `ADMIN_CHANNEL_ID`: ID of a Discord server's text channel for commands performed by admins
* `CHANNEL_ID_REQUESTS`: Channel ID for requests that have to be accepted / denied
* `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`

If you want to receive mail notifications about critical errors: (credentials for the account the mails will be sent from)
* `MAIL_PASSWORD`, `SMTP_SERVER`, `MAIL_LOGIN` (username)
* `RECEIVER_EMAILS`: List of e-mail receivers, sperated by spaces (set it via `export RECEIVER_EMAILS="abc@def.de qwertz@example.com"`)

### Table creation pattern
```
create table dc_users
(
    ID         int auto_increment
               primary key,
    uuid       varchar(64)  not null,
    dc_id      bigint       not null,
    first_name varchar(255) null,
    classs     varchar(255) null,
    date       datetime     not null
);
```
(some attributes may be better to remove for your personal use)

## [DE]
Ein Discord-Bot, um Spieler auf einem Minecraft-Server zu whitelisten.

### Wie funktioniert es?
1. Ein Spieler stellt eine Anfrage, gewhitelistet zu werden, indem er `.whitelist [Minecraft-Benutzername]` in einen Textkanal auf dem Discord-Server schreibt.
2. Ein zuvor festgelegter Text-Kanal auf einem Server bekommt eine Nachricht vom Bot, in der Admins entscheiden können, ob der Spieler gewhitelistet werden soll oder nicht.
3. Der Spieler wird einer Datenbank hinzugefügt, die z. B. von einem Minecraft-Plugin ausgelesen werden kann.

### Voraussetzungen
* Ein Minecraft-Server
* Eine Datenbank
* Ein Discord-Server
* Ein Discord-Bot pro Minecraft-Server (verfügbar im [Discord developer portal](https://discord.com/developers/applications))

Der deutsche Text enthält nicht alle Informationen, daher für genaueres den englischen Text darüber lesen!
