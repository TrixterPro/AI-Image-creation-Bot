# Image Generation Discord Bot

A Discord bot that enables seamless image generation using the `/imagine` command. It's quick to set up and easy to use!

## Features
- Slash command `/imagine` for generating images.
- Fallback `!sync` command to manually sync slash commands, if necessary.
- Supports the ImgHippo API for image generation.

---

## Installation & Setup

### Prerequisites
1. Ensure you have Python 3.8+ installed.
2. Clone or download this repository to your local machine.

### Step 1: Install Dependencies
Run the following command in your terminal to install the required libraries:
```bash
pip install -r requirements.txt
```
### Step 2: Generate and Configure config.yml
- Run the bot initially to generate the config.yml file:
```bash
python main.py
```
- Open the generated config.yml file and configure it with your details. The default config looks like this:
```yml
# Your discord bot token get it by creating an application at https://discord.com/developers/applications
TOKEN: ''

# Prefix is for the !sync command (used to sync slash commands if needed)
PREFIX: '!'

# IMG_HIPPO_API_KEY is for accessing the ImgHippo API.
IMG_HIPPO_API_KEY: ''
```
- Replace TOKEN with your bot's token (instructions below).
- Replace IMG_HIPPO_API_KEY with your ImgHippo API key.


### How to Get Your Discord Bot Token
- Go to the Discord Developer Portal.
- Click on New Application and name your application.
- Navigate to the Bot tab on the left and click Add Bot.
- Under the bot settings, click Reset Token to generate a bot token.
- Copy the token and paste it into the TOKEN field in your config.yml.
- Make sure you enable all the Gateway Intents in the Bot tab.
![image_2024-12-06_181240534](https://github.com/user-attachments/assets/7c16144f-1507-4919-a406-01c290310b54)


### Running the Bot
- After configuring the config.yml, you can start the bot with:
```bash
python main.py
```
---

### Usage
Once the bot is online:
- Use the /imagine command to generate images.
- If you do not see the /imagine command:
    - Run the !sync command to manually sync the slash commands.
    - Restart your Discord client if the commands are still not visible.

---
### Troubleshooting
- Ensure the bot has the necessary permissions in your Discord server to register and use slash commands.
- If issues persist, double-check the TOKEN in your config.yml and ensure it's valid.

### Contributing
Feel free to contribute to this project by submitting issues or creating pull requests. All contributions are welcome!

### License
This project is licensed under the MIT License. See the LICENSE file for details.
