# SwiftBot

SwiftBot is an interactive Telegram bot designed to facilitate engaging conversations with the Gemini AI generative model, powered by Google. It offers various functionalities, including saving and loading conversations, managing instructions, and updating user preferences such as language.

## Features

- **Communicate with the Gemini Model**: Engage in conversations with the Gemini using text or media.
- **Save and Load History**: Easily save your conversation history and load it when needed.
- **Manage Instructions**: Set and update system instructions to customize your interactions.
- **Change Language**: Update your preferred language for interacting with the bot.
- **User-Friendly Menu**: An accessible menu to navigate through different functionalities.
- **Queue-Based Messaging**: All interactions are managed using queues to ensure smooth and efficient message handling.

## Commands

- `/start` - Start interacting with the bot and receive a welcome message.
- `/menu` - Display the main menu with available options.
- `/setinst <instruction>` - Set a new system instruction.
- `/delinst` - Delete the current system instruction.
- `/save <history_name>` - Save the conversation history with the specified name.
- `/delete <history_name>` - Delete the specified conversation history.
- `/load <history_name>` - Load a previously saved conversation history.
- `/clear` - Clear the current conversation history.
- `/language <language_code>` - Update the user's preferred language.

## Deployment Instructions

### Prerequisites

- Python 3.7+
- MongoDB instance
- Telegram bot token (obtained via BotFather on Telegram)
- Gemini API keys

### 1. Clone the Repository

```sh
git clone <repository-url>
cd <repository-name>
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root directory and add the following configurations:

```env
BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
GEMINI_API_KEYS=<YOUR_GEMINI_API_KEYS> (comma separated)
MONGO_URI=<YOUR_MONGODB_URI>
PROXY=<YOUR_PROXY>
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Run

Start the bot:

```sh
python main.py
```

Your bot should now be running and ready to interact with users.

## Contributing

Feel free to open issues or submit pull requests for any improvements or bug fixes.
