import discord
from discord.ext import commands
from discord import app_commands, ui
from io import BytesIO
from freeGPTFix import Client
from PIL import Image
import os
import random
import string
from utils.config import basicconfig

class ImageGenerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = "pollinations" 
    
    async def generate_and_send_image(self, prompt):
        """
        Generates an image based on the prompt and returns the local file path.

        Args:
            prompt (str): The prompt for image generation.

        Returns:
            str: The path to the saved image.
        """
        try:
            resp = Client.create_generation(self.model, prompt)
            image = Image.open(BytesIO(resp))
            
            image_name = ''.join(random.choices(string.ascii_letters, k=10)) + ".png"
            temp_path = os.path.join(os.getcwd(), image_name)
            
            image.save(temp_path)
            return temp_path
        except Exception as e:
            print(f"Error: {e}")
            return None

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
                await interaction.response.send_message(
                    "Your prompt may violate Discord's TOS, please keep the prompts SFW.",
                    ephemeral=True
                )
                return

        await interaction.response.defer(thinking=True)
        embed = discord.Embed(
            title='Image Generated',
            description=f'Prompt:```{prompt}```',
            color=discord.Color.green()
        )
        
        embed.add_field(name='Source', value=self.model.capitalize())
        image_path = await self.generate_and_send_image(prompt=prompt)
        if image_path:
            file = discord.File(image_path, filename="generated.png")
            embed.set_image(url="attachment://generated.png")
            await interaction.followup.send(embed=embed, file=file)
            os.remove(image_path)
        else:
            embed = discord.Embed(
                title="Error",
                description="Failed to generate the image.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ImageGenerationCog(bot=bot))
