# Mage Tarot Bot

**Mage Tarot Bot** is a Discord bot built around an original fantasy-themed tarot card deck. The cards are custom-designed artwork across 5 unique suits — Major Arcana, Dynamism, Pattern, Primordialism, and Questing — totaling ~78 unique cards.

## Commands

The bot runs two slash commands:

- `/tarot` — draws 1, 3, or 5 random cards from the full deck
- `/tarot_suit` — draws a single card from a chosen suit

Each card is sent as a Discord embed with its artwork and a short Turkish description (currently complete for Major Arcana).

## Deck Structure

The deck replaces traditional tarot suit names (Wands, Cups, Swords, Pentacles) with original fantasy equivalents, while keeping the standard 14-card minor arcana structure (Ace through 10, Page, Knight, King, Queen). Major Arcana follows the classic 22-card sequence with renamed cards such as "Gaia" instead of The World and "Luna" instead of The Moon.

| Suit | Cards |
|---|---|
| Major Arcana 🌟 | 22 |
| Dynamism ⚡ | 14 |
| Pattern 🔷 | 14 |
| Primordialism 🌿 | 14 |
| Questing ⚔️ | 14 |

## Technical Details

Built with Python using discord.py and Pillow. Card artwork is stored as `.tif` originals and converted to PNG on the fly before being sent to Discord. A `web_cards/` folder containing pre-converted PNGs is also included, ready for static web use.

### Dependencies

```
discord.py>=2.3.0
Pillow>=10.0.0
python-dotenv>=1.0.0
```

### Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file and add your Discord bot token: `DISCORD_TOKEN=your_token_here`
4. Run the bot: `python bot.py`
