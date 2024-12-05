import discord
from discord.ext import commands
from discord import app_commands, ui
from io import BytesIO
from freeGPT import Client
from PIL import Image
import os
import random
import string
from utils.config import basicconfig
import aiohttp

class ImageGenerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def generate_and_upload_image(self, api_key, prompt):
        """
        Generates an image based on the prompt and uploads it to IMG Hippo.

        Args:
            api_key (str): The API key for IMG Hippo.
            prompt (str): The prompt for image generation.

        Returns:
            str: The URL of the uploaded image.
        """
        try:
            resp = Client.create_generation("prodia", prompt)
            image = Image.open(BytesIO(resp))
            
            image_name = ''.join(random.choices(string.ascii_letters, k=10)) + ".png"
            temp_path = os.path.join(os.getcwd(), image_name)
            
            image.save(temp_path)
            
            url = 'https://api.imghippo.com/v1/upload'
            async with aiohttp.ClientSession() as session:
                form_data = aiohttp.FormData()
                form_data.add_field('file', open(temp_path, 'rb'), filename=image_name)
                form_data.add_field('api_key', api_key)
                
                async with session.post(url, data=form_data) as response:
                    if response.status == 200:
                        json_response = await response.json()
                        if json_response.get('success'):
                            return json_response['data']['url']
                        else:
                            raise Exception("Image upload failed: " + json_response.get('message', 'Unknown error'))
                    else:
                        raise Exception(f"Image upload failed with status code {response.status}")
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    @app_commands.command(name='imagine', description='Generate an image based on a prompt')
    @app_commands.describe(prompt='The prompt to generate an image from')
    async def imagine(self, interaction: discord.Interaction, prompt: str):
        prohibited_words = [
            "nude", "naked", "porn", "explicit", "sex", "sexual", "intercourse", "erotic", "fetish", "kinky", "bdsm",
            "hardcore", "orgy", "xxx", "strip", "stripper", "genitals", "penis", "vagina", "breasts", "boobs", "nipples",
            "buttocks", "butt", "ass", "anal", "masturbation", "ejaculation", "cum", "sperm", "orgasm", "moan",
            "incest", "bestiality", "pedophile", "child porn", "rape", "molest", "prostitute", "brothel", "escort",
            "underage", "teen sex", "milf", "daddy", "mommy", "dominatrix", "submission", "submissive", "dominant",
            "nsfw", "smut", "camgirl", "cam", "adult video", "adult film", "adult content", "softcore",
            "semen", "threesome", "gangbang", "hentai", "yaoi", "yuri", "tentacle", "vore", "lewd", "obscene",
            "provocative", "lingerie", "sex toy", "dildo", "vibrator", "orgy", "penetration", "roleplay", "panties",
            "thong", "strip club", "sugar daddy", "sugar baby", "latex fetish", "fetish wear", "sex worker", 
            "pegging", "voyeur", "voyeurism", "exhibitionism", "hooker", "escort service", "blowjob", "handjob", 
            "oral sex", "deepthroat", "pornography", "graphic content", "naughty", "dirty", "seductive",
            "provocative outfit", "porn star", "adult entertainer"
        ]


        for word in prohibited_words:
            if word in prompt.lower():
                await interaction.response.send_message(f"Your prompt may violate discord's TOS, please keep the prompts sfw.", ephemeral=True)
                return
                


        await interaction.response.defer(thinking=True)
        embed = discord.Embed(title='Image Generated', description=f'Prompt:```{prompt}```', color=discord.Color.green())
        
        url = await self.generate_and_upload_image(api_key=basicconfig.IMG_HIPPO_API_KEY, prompt=prompt)
        if url:
            embed.set_image(url=url)
            await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description="Failed to generate and upload the image.", color=discord.Color.red())
            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ImageGenerationCog(bot=bot))
