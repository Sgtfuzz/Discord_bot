#Imports
import discord
from discord.ext import commands
from openai import OpenAI
import asyncio
import traceback

#Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix= "!", intents=intents)

#API Keys
DISCORD_TOKEN = 'Discord API here'
OPENAI_API_KEY = 'OpenAI API here'

client = OpenAI(api_key= OPENAI_API_KEY)

@bot.event
async def on_ready():
    print(f'Logged in as user {bot.user}')

@bot.command(name = "memeAI")
async def meme(ctx, *, keywords: str):
    await ctx.send("Generating your meme...")
    
    try:
        #Step 1: Generate caption
        prompt = f"Generate a funny meme caption using these keywords: {keywords}"
        caption_response = client.chat.completions.create(model ="gpt-4", messages = [{"role": "system",
                                                                                     "content": "You are a meme caption generator."
                                                                                     },
                                                                                     {"role": "user", "content": prompt}])
        caption = caption_response.choices[0].message.content.strip()
        
        #Step 2: Generate image with DALL.E
        image_response = client.images.generate(prompt = caption, n = 1, size = "512x512")
        image_url = image_response.data[0].url

        #Step 3: Send image and cpation
        await ctx.send(f"**{caption}**\n{image_url}")
        
    except Exception as e:
        error_msg = traceback.format_exc()
        print(error_msg)
        await ctx.send(f"Oops! Something went wrong: {e}")
        
#Run the bot
bot.run(DISCORD_TOKEN)