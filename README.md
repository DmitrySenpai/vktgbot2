<h1 align="center">vktgbot 2</h1>
<p align=center>
    <a target="_blank" href="https://www.python.org/downloads/" title="Python Version"><img src="https://img.shields.io/badge/python-%3E=_3.8-purple.svg"></a>
    <a target="_blank" href="https://github.com/DmitrySenpai/vktgbot2/releases"><img alt="docker image" src="https://img.shields.io/github/v/release/DmitrySenpai/vktgbot2?include_prereleases"></a>
    <a target="_blank" href="LICENSE" title="License: GPL-3.0"><img src="https://img.shields.io/github/license/DmitrySenpai/vktgbot2.svg?color=red"></a>
</p> 

<p align="center"><b>Telegram-бот для автоматической пересылки постов из ВКонтакте в Telegram.</b></p>

<p align="center">
    <img src="https://github.com/user-attachments/assets/965b5246-33cf-4af8-a5c2-fd242d8fa31a"/>
</p>

## О скрипте

Скрипт Python для автоматического репоста со страниц сообществ ВК в каналы или чаты Telegram. После настройки и запуска скрипта он будет проверять наличие новых постов в ВК каждые *N* секунд с помощью API ВК и, если таковые имеются, анализировать и отправлять их в Telegram.

Данный скрипт является форком [vktgbot](https://github.com/alcortazzo/vktgbot) .

## Как использовать скрипт

Вы можете вручную запустить скрипт с помощью Python или Docker и оставить его работать в фоновом режиме. Или вы можете настроить скрипт на автоматический запуск на удаленном сервере с помощью таких инструментов, как crontab, systemd и т. д. Или вы можете настроить скрипт на однократный запуск, если установите `VAR_SINGLE_START = True` в файле `.env`.

## Установка
```shell
# Клонирование репозиторий
$ git clone https://github.com/DmitrySenpai/vktgbot2.git

# если вы хотите клонировать определенную версию (например v1.1)
$ git clone -b v1.1 https://github.com/DmitrySenpai/vktgbot2.git

# Откройте каталог vktgbot2
$ cd vktgbot2
```

## Настройка
**Откройте файл конфигурации `.env` с помощью текстового редактора и задайте следующие переменные:**
```ini
VAR_TG_BOT_TOKEN = 1234567890:AAA-AaA1aaa1AAaaAa1a1AAAAA-a1aa1-Aa
VAR_VK_TOKEN = 00a0a0ab00f0a0ab00f0a6ab0c00000b0f000f000f0a0ab0a00b000000dd00000000de0
VAR_VK_TO_TG = '[
    ["domain_vk", -1234567890]
]'
```
* `VAR_TG_BOT_TOKEN` Это токен для вашего бота Telegram. Вы можете получить его здесь: [BotFather](https://t.me/BotFather).
* `VAR_VK_TOKEN` это персональный токен для вашего профиля ВК. Вы можете получить его здесь: [Как получить](https://github.com/DmitrySenpai/vktgbot2/blob/main/vk_access_token.md).

* `VAR_VK_TO_TG` В этом разделе указываете ссылку на группу/страницу ВК (указываем после vk.com/) и ID TG канала **(Вы должны добавить бота на этот TG канал как администратор!)**. Можно указать несколько групп/страниц ВК и каналов TG каналов по примеру:
```ini
VAR_VK_TO_TG = '[
    ["domain_vk", -1234567890],
    ["durov", -987654321]
]'
```

## Запуск
### С помощью Python
```shell
# install requirements
$ python3 -m pip install -r requirements.txt

# run script
$ python3 vktgbot
```
###  Docker
```shell
# change the working directory to docker
$ cd docker

# build and run docker
$ docker-compose up --build
```
## Лицензия
GPLv3<br/>
Original Creator - [alcortazzo](https://github.com/alcortazzo)<br>
Fork Author - [DmitrySenpai](https://github.com/DmitrySenpai/)
