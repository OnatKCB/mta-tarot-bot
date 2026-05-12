"""Run once to convert all TIF cards to PNG for the web app."""
from pathlib import Path
from PIL import Image

CARDS_DIR = Path(__file__).parent / "cards"
WEB_CARDS_DIR = Path(__file__).parent / "web_cards"
MAX_WIDTH = 600

converted = 0
skipped = 0

for suit_dir in sorted(CARDS_DIR.iterdir()):
    if not suit_dir.is_dir():
        continue
    out_dir = WEB_CARDS_DIR / suit_dir.name
    out_dir.mkdir(parents=True, exist_ok=True)

    for card_file in sorted(suit_dir.iterdir()):
        if card_file.suffix.lower() not in {".tif", ".tiff", ".png", ".jpg", ".jpeg"}:
            continue
        if "alternate" in card_file.stem.lower():
            skipped += 1
            continue

        out_path = out_dir / (card_file.stem.rstrip(".") + ".png")
        if out_path.exists():
            skipped += 1
            continue

        try:
            with Image.open(card_file) as img:
                img = img.convert("RGB")
                if img.width > MAX_WIDTH:
                    ratio = MAX_WIDTH / img.width
                    img = img.resize((MAX_WIDTH, int(img.height * ratio)), Image.LANCZOS)
                img.save(out_path, format="PNG", optimize=True)
            print(f"  OK {suit_dir.name}/{out_path.name}")
            converted += 1
        except Exception as e:
            print(f"  SKIP {card_file.name}: {e}")
            skipped += 1

print(f"\nTamamlandı: {converted} kart dönüştürüldü, {skipped} atlandı.")
print(f"Şimdi index.html dosyasını tarayıcıda açabilirsin.")
