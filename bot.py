import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from droplet_manager import DropletManager

# Enable logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Get bot token and droplet name
token = os.getenv("BOT_TOKEN")
droplet_name = os.getenv("DROPLET_NAME")
if not token:
    raise ValueError("No BOT_TOKEN found in .env file")
if not droplet_name:
    raise ValueError("No DROPLET_NAME found in .env file")

# Define authorized user
AUTHORIZED_ID = 5303965494

# Define states
class ConsoleStates(StatesGroup):
    waiting_for_command = State()

# Initialize bot, dispatcher and droplet manager
bot = Bot(token=token)
dp = Dispatcher(storage=MemoryStorage())
droplet_manager = DropletManager()

# Middleware to check user authorization
async def check_auth(message: types.Message):
    if message.from_user.id != AUTHORIZED_ID:
        await message.answer("⛔ Access denied. This bot is private.")
        return False
    return True

# Command handler for /help
@dp.message(Command("help"))
async def help_command(message: types.Message):
    if not await check_auth(message):
        return

    help_text = """
🤖 AdminDO Bot
Your DigitalOcean Droplet Administrator

Available Commands:
/help - Show this help message
/console - Enter console mode to execute commands
/cancel - Cancel current operation
    """
    await message.answer(help_text)

# Command handler for /console
@dp.message(Command("console"))
async def console_command(message: types.Message, state: FSMContext):
    if not await check_auth(message):
        return

    await state.set_state(ConsoleStates.waiting_for_command)
    await message.answer(
        "📝 Enter the command you want to execute on the droplet.\n"
        "Use /cancel to exit console mode."
    )

# Handler for /cancel
@dp.message(Command("cancel"))
async def cancel_command(message: types.Message, state: FSMContext):
    if not await check_auth(message):
        return

    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Nothing to cancel.")
        return
    
    await state.clear()
    await message.answer("Console mode deactivated. ❌")

# Handler for console commands
@dp.message(ConsoleStates.waiting_for_command)
async def handle_console_command(message: types.Message, state: FSMContext):
    if not await check_auth(message):
        return

    command = message.text.strip()
    
    # Don't process commands that start with /
    if command.startswith('/'):
        return
    
    # Execute the command
    result = droplet_manager.execute_command(droplet_name, command)
    
    if "error" in result:
        await message.answer(f"❌ Error: {result['error']}")
    else:
        # Format the output in a code block for better readability
        output = result['output'] if result['output'] else "Command executed successfully (no output)"
        formatted_output = f"```\n{output}\n```"
        await message.answer(formatted_output, parse_mode="MarkdownV2")
    
    # Ask for the next command
    await message.answer("Enter another command or use /cancel to exit console mode.")

# Main function to start the bot
async def main():
    print("Starting AdminDO bot...")
    # Delete webhook before polling
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Set up the commands menu
    commands = [
        types.BotCommand(command="help", description="Show available commands"),
        types.BotCommand(command="console", description="Enter console mode to execute commands"),
        types.BotCommand(command="cancel", description="Cancel current operation"),
        # Add more commands here as needed
    ]
    await bot.set_my_commands(commands)
    
    # Start polling
    print("AdminDO bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}") 