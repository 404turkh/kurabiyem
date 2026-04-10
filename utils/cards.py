import io
from datetime import timezone
from PIL import Image, ImageDraw, ImageFont

def fit_text(draw, text, font_path, max_width, start_size, min_size=18):
    size = start_size
    while size >= min_size:
        try:
            font = ImageFont.truetype(font_path, size)
        except Exception:
            return ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            return font
        size -= 2

    try:
        return ImageFont.truetype(font_path, min_size)
    except Exception:
        return ImageFont.load_default()

async def create_welcome_card(member):
    width, height = 1100, 400
    card = Image.new("RGBA", (width, height), (20, 18, 34, 255))
    draw = ImageDraw.Draw(card, "RGBA")

    draw.rounded_rectangle((18, 18, width - 18, height - 18), radius=34, fill=(28, 26, 44, 255))
    draw.rounded_rectangle((28, 28, width - 28, height - 28), radius=30, outline=(255, 190, 235, 255), width=3)

    draw.ellipse((720, -80, 1100, 220), fill=(255, 120, 210, 55))
    draw.ellipse((650, 120, 980, 430), fill=(130, 120, 255, 60))
    draw.ellipse((-120, 180, 200, 460), fill=(255, 220, 120, 35))

    avatar_asset = member.display_avatar.with_size(256)
    avatar_bytes = await avatar_asset.read()
    avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA").resize((190, 190))

    mask = Image.new("L", (190, 190), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 190, 190), fill=255)

    avatar_circle = Image.new("RGBA", (190, 190), (0, 0, 0, 0))
    avatar_circle.paste(avatar, (0, 0), mask)

    border = Image.new("RGBA", (214, 214), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border)
    border_draw.ellipse((0, 0, 213, 213), fill=(255, 190, 235, 255))
    border_draw.ellipse((9, 9, 204, 204), fill=(28, 26, 44, 255))

    card.paste(border, (58, 92), border)
    card.paste(avatar_circle, (70, 104), avatar_circle)

    bold_font = "DejaVuSans-Bold.ttf"
    regular_font = "DejaVuSans.ttf"

    try:
        title_font = ImageFont.truetype(bold_font, 48)
        small_font = ImageFont.truetype(regular_font, 24)
        info_font = ImageFont.truetype(regular_font, 28)
    except Exception:
        title_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        info_font = ImageFont.load_default()

    name_font = fit_text(draw, member.display_name, bold_font, 600, 42, 22)
    created_str = member.created_at.astimezone(timezone.utc).strftime("%Y-%m-%d")

    draw.text((320, 70), "WELCOME TO THE SERVER", font=title_font, fill=(255, 255, 255, 255))
    draw.text((320, 138), member.display_name, font=name_font, fill=(255, 210, 240, 255))
    draw.text((320, 190), f"User: {member}", font=small_font, fill=(220, 220, 240, 255))

    draw.rounded_rectangle((320, 240, 960, 294), radius=18, fill=(50, 46, 72, 255))
    draw.text((344, 253), f"Member Count: {member.guild.member_count}", font=info_font, fill=(255, 255, 255, 255))

    draw.rounded_rectangle((320, 315, 960, 369), radius=18, fill=(50, 46, 72, 255))
    draw.text((344, 328), f"Account Created: {created_str}", font=info_font, fill=(255, 255, 255, 255))

    output = io.BytesIO()
    card.save(output, format="PNG")
    output.seek(0)
    return output
