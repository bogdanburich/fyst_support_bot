# Telegram bot for FYST support

Bot replies for user messages if support doesn't answer in the same chat in 30 seconds.
Bot checks if it's support user or not using username. If username ends with "_fyst" substring, this user is considered as support.
If user haven't got his answer from support yet, there will be no additional messages to this chat till support answer.
Messages about deleting or adding users doesn't counts as messages.

## Setup

There are two images to run: one for Mac and one for Linux with specified tag, so there are two docker-compose files to run

- docker-compose build && docker-compose up

## Extra

- docker build --platform=linux/amd64 . for - Linux build created on Mac
