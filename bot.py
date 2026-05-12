import os
import random
import io
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

CARDS_DIR = Path(__file__).parent / "cards"

SUIT_NAMES = {
    "Major Arcana": "Major Arcana",
    "Dynamism": "Dynamism",
    "Pattern": "Pattern",
    "Primordialism": "Primordialism",
    "Questing": "Questing",
}

CARD_DESCRIPTIONS = {
    # Major Arcana
    "0 Fool": "Yeni başlangıçlar, saf enerji, sonsuz potansiyel.",
    "1 Mage": "İrade, yaratıcılık, ustalık ve dönüşüm gücü.",
    "1 Cover Mage": "İrade, yaratıcılık, ustalık ve dönüşüm gücü.",
    "2 High Priestess": "Sezgi, gizem, bilinçdışı ve içsel bilgelik.",
    "03 The Empress": "Bereket, doğa, annelik, bolluk ve yaratıcılık.",
    "4 Tarot Emperor": "Otorite, yapı, düzen ve liderlik.",
    "5 The Heirophant": "Gelenek, manevi rehberlik ve kurumsal bilgelik.",
    "6 The Lovers": "Aşk, uyum, değerler ve önemli seçimler.",
    "7 The Chariot": "Zafer, irade gücü, kontrol ve azim.",
    "8 Strength": "İç güç, cesaret, sabır ve şefkat.",
    "9 The Hermit": "İç arayış, yalnızlık, rehberlik ve bilgelik.",
    "10 Wheel Fortune": "Döngüler, kader, dönüm noktaları ve şans.",
    "11 Justice": "Adalet, denge, hakikat ve sebep-sonuç.",
    "12 The Hanged Man": "Teslim oluş, bekleyiş, yeni bakış açısı ve fedakarlık.",
    "13 Death": "Dönüşüm, son ve yeni başlangıçlar, değişim.",
    "14 Temperance": "Denge, ılımlılık, sabır ve amaç.",
    "15 The Devil": "Bağlar, maddecilik, gölge yön ve kısıtlamalar.",
    "16 The Tower": "Ani değişim, yıkım, kurtuluş ve kırılma.",
    "17 The Star": "Umut, ilham, yenilenme ve maneviyat.",
    "18 Luna": "Sezgi, bilinçdışı, korkular ve hayal.",
    "19 The Sun": "Neşe, başarı, canlılık ve aydınlanma.",
    "20 Judgement": "Uyanış, yeniden doğuş, af ve yüksek çağrı.",
    "21 Gaia": "Tamamlanma, bütünlük, başarı ve dünya.",
}

def load_all_cards() -> list[dict]:
    cards = []
    extensions = {".tif", ".tiff", ".png", ".jpg", ".jpeg"}
    for suit_dir in CARDS_DIR.iterdir():
        if not suit_dir.is_dir():
            continue
        suit = suit_dir.name
        for card_file in suit_dir.iterdir():
            if card_file.suffix.lower() in extensions:
                # Strip extension and trailing dots for display name
                stem = card_file.stem.rstrip(".")
                # Skip alternate versions to avoid duplicates (keep originals)
                if "alternate" in stem.lower():
                    continue
                cards.append({
                    "name": stem,
                    "suit": suit,
                    "path": card_file,
                })
    return cards


ALL_CARDS = load_all_cards()


def card_to_discord_file(card: dict) -> tuple[discord.File, str]:
    """Convert a card image to a Discord-sendable PNG file."""
    with Image.open(card["path"]) as img:
        img = img.convert("RGB")
        # Resize to a reasonable Discord embed size (max 800px wide)
        max_width = 600
        if img.width > max_width:
            ratio = max_width / img.width
            img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
    filename = f"{card['suit']}_{card['name']}.png".replace(" ", "_")
    return discord.File(buf, filename=filename), filename


def build_card_embed(card: dict, index: int, total: int, filename: str) -> discord.Embed:
    suit_emojis = {
        "Major Arcana": "🌟",
        "Dynamism": "⚡",
        "Pattern": "🔷",
        "Primordialism": "🌿",
        "Questing": "⚔️",
    }
    emoji = suit_emojis.get(card["suit"], "🃏")
    title = f"{emoji} {card['name']}"
    if total > 1:
        title = f"Kart {index}/{total} — {title}"

    description = CARD_DESCRIPTIONS.get(card["name"], "")

    embed = discord.Embed(
        title=title,
        description=description if description else discord.utils.MISSING,
        color=discord.Color.dark_purple(),
    )
    embed.set_footer(text=f"Suit: {card['suit']} · Mage Tarot Cards (1st ed)")
    embed.set_image(url=f"attachment://{filename}")
    return embed


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree


@bot.event
async def on_ready():
    await tree.sync()
    print(f"{bot.user} olarak giriş yapıldı. {len(ALL_CARDS)} kart yüklendi.")


@tree.command(name="tarot", description="Rastgele Mage Tarot kartı çek")
@app_commands.describe(adet="Kaç kart çekmek istiyorsun? (1, 3 veya 5)")
@app_commands.choices(adet=[
    app_commands.Choice(name="1 kart", value=1),
    app_commands.Choice(name="3 kart", value=3),
    app_commands.Choice(name="5 kart", value=5),
])
async def tarot(interaction: discord.Interaction, adet: app_commands.Choice[int] = None):
    count = adet.value if adet else 1
    await interaction.response.defer()

    drawn = random.sample(ALL_CARDS, min(count, len(ALL_CARDS)))

    files = []
    embeds = []
    for i, card in enumerate(drawn, 1):
        file, filename = card_to_discord_file(card)
        embed = build_card_embed(card, i, len(drawn), filename)
        files.append(file)
        embeds.append(embed)

    await interaction.followup.send(embeds=embeds, files=files)


@tree.command(name="tarot_suit", description="Belirli bir takımdan rastgele kart çek")
@app_commands.describe(takim="Hangi takımdan kart çekmek istiyorsun?")
@app_commands.choices(takim=[
    app_commands.Choice(name="Major Arcana 🌟", value="Major Arcana"),
    app_commands.Choice(name="Dynamism ⚡", value="Dynamism"),
    app_commands.Choice(name="Pattern 🔷", value="Pattern"),
    app_commands.Choice(name="Primordialism 🌿", value="Primordialism"),
    app_commands.Choice(name="Questing ⚔️", value="Questing"),
])
async def tarot_suit(interaction: discord.Interaction, takim: app_commands.Choice[str]):
    suit_cards = [c for c in ALL_CARDS if c["suit"] == takim.value]
    if not suit_cards:
        await interaction.response.send_message("Bu takımda kart bulunamadı.", ephemeral=True)
        return

    await interaction.response.defer()
    card = random.choice(suit_cards)
    file, filename = card_to_discord_file(card)
    embed = build_card_embed(card, 1, 1, filename)
    await interaction.followup.send(embed=embed, file=file)


if __name__ == "__main__":
    bot.run(TOKEN)
