#!/usr/bin/env python3
"""Generate Enervit Athletes Guide PDF presentation for sales team."""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, Color
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import os

# Constants
W, H = landscape(A4)
RED = HexColor("#E30613")
DARK = HexColor("#1a1a1a")
GRAY = HexColor("#666666")
LIGHT_BG = HexColor("#f5f5f5")
WHITE = white

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Enervit_Athletes_Guide_2026.pdf")

# Register fonts with Czech diacritics support
pdfmetrics.registerFont(TTFont('Arial', '/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', '/System/Library/Fonts/Supplemental/Arial Italic.ttf'))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', '/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf'))

# Font name mapping
FONT = 'Arial'
FONT_BOLD = 'Arial-Bold'
FONT_ITALIC = 'Arial-Italic'


def draw_red_bar(c, y=0, height=8*mm):
    """Draw a red accent bar."""
    c.setFillColor(RED)
    c.rect(0, y, W, height, fill=1, stroke=0)


def draw_page_number(c, num, total):
    """Draw page number at bottom right."""
    c.setFillColor(GRAY)
    c.setFont(FONT, 8)
    c.drawRightString(W - 20*mm, 10*mm, f"{num} / {total}")


def draw_image_safe(c, path, x, y, width=None, height=None, mask='auto'):
    """Draw an image with error handling."""
    try:
        img = ImageReader(path)
        c.drawImage(img, x, y, width=width, height=height, mask=mask, preserveAspectRatio=True)
    except Exception as e:
        print(f"Warning: Could not load image {path}: {e}")


def draw_rounded_rect(c, x, y, w, h, radius=4*mm, fill_color=None, stroke_color=None):
    """Draw a rounded rectangle."""
    c.saveState()
    if fill_color:
        c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
    c.roundRect(x, y, w, h, radius, fill=1 if fill_color else 0, stroke=1 if stroke_color else 0)
    c.restoreState()


def draw_bullet(c, x, y, text, font_size=11):
    """Draw a bullet point with text."""
    c.setFillColor(RED)
    c.circle(x + 3, y + 3, 3, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont(FONT, font_size)
    c.drawString(x + 12, y, text)


TOTAL_PAGES = 7


def page_cover(c):
    """Page 1: Cover page."""
    # Full dark background
    c.setFillColor(DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Red accent stripe at top
    c.setFillColor(RED)
    c.rect(0, H - 12*mm, W, 12*mm, fill=1, stroke=0)

    # Red diagonal accent
    c.setFillColor(Color(227/255, 6/255, 19/255, alpha=0.15))
    c.saveState()
    path = c.beginPath()
    path.moveTo(W * 0.55, 0)
    path.lineTo(W, 0)
    path.lineTo(W, H)
    path.lineTo(W * 0.35, H)
    path.close()
    c.clipPath(path, stroke=0)
    c.setFillColor(Color(227/255, 6/255, 19/255, alpha=0.08))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.restoreState()

    # Images on the right side (collage)
    img_size = 85*mm
    margin = 8*mm
    right_x = W - img_size - 25*mm

    # Top image
    draw_rounded_rect(c, right_x, H - img_size - 30*mm, img_size, img_size, radius=6*mm, fill_color=HexColor("#333333"))
    c.saveState()
    path = c.beginPath()
    path.roundRect(right_x, H - img_size - 30*mm, img_size, img_size, 6*mm)
    c.clipPath(path, stroke=0)
    draw_image_safe(c, os.path.join(ASSETS, "gravel-rider.png"),
                    right_x, H - img_size - 30*mm, img_size, img_size)
    c.restoreState()

    # Bottom image
    draw_rounded_rect(c, right_x - 20*mm, 25*mm, img_size, img_size - 10*mm, radius=6*mm, fill_color=HexColor("#333333"))
    c.saveState()
    path = c.beginPath()
    path.roundRect(right_x - 20*mm, 25*mm, img_size, img_size - 10*mm, 6*mm)
    c.clipPath(path, stroke=0)
    draw_image_safe(c, os.path.join(ASSETS, "hockey-player.png"),
                    right_x - 20*mm, 25*mm, img_size, img_size - 10*mm)
    c.restoreState()

    # Logo
    draw_image_safe(c, os.path.join(ASSETS, "enervit-logo.png"),
                    35*mm, H - 55*mm, width=100*mm, height=35*mm)

    # Title
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 38)
    c.drawString(35*mm, H - 90*mm, "Athletes Guide")
    c.setFont(FONT_BOLD, 38)
    c.setFillColor(RED)
    c.drawString(35*mm, H - 105*mm, "2026")

    # Subtitle
    c.setFillColor(Color(1, 1, 1, alpha=0.7))
    c.setFont(FONT, 14)
    c.drawString(35*mm, H - 125*mm, "Průvodce spoluprací")
    c.drawString(35*mm, H - 140*mm, "pro ambasadory a sportovce")

    # Red line separator
    c.setStrokeColor(RED)
    c.setLineWidth(3)
    c.line(35*mm, H - 148*mm, 120*mm, H - 148*mm)

    # Bottom info
    c.setFillColor(Color(1, 1, 1, alpha=0.5))
    c.setFont(FONT, 10)
    c.drawString(35*mm, 20*mm, "enervit.cz  |  hello@enervit.cz")
    c.drawString(35*mm, 12*mm, "@enervit_czsk  |  @sportujlepe")


def page_intro(c):
    """Page 2: Introduction."""
    # White background
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_red_bar(c, H - 8*mm)

    # Section number
    c.setFillColor(RED)
    c.circle(35*mm, H - 30*mm, 12, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 12)
    c.drawCentredString(35*mm, H - 34*mm, "01")

    # Title
    c.setFillColor(DARK)
    c.setFont(FONT_BOLD, 28)
    c.drawString(50*mm, H - 35*mm, "Vítej v týmu Enervit")

    # Left column - text
    left_x = 35*mm
    text_width = W * 0.5

    y = H - 60*mm
    c.setFillColor(DARK)
    c.setFont(FONT, 12)

    texts = [
        "Tento dokument slouží jako vodítko pro naši",
        "společnou komunikaci. Naším cílem je, aby propojení",
        "tvého sportovního výkonu a značky Enervit působilo",
        "přirozeně, odborně a autenticky.",
        "",
        "Jako ambasador Enervitu reprezentuješ značku,",
        "která stojí za kvalitní sportovní výživou.",
        "Spolupráce je oboustranně výhodná — my podpoříme",
        "tvůj výkon a ty nám pomůžeš oslovit další sportovce.",
    ]

    for line in texts:
        if line == "":
            y -= 8*mm
        else:
            c.drawString(left_x, y, line)
            y -= 6.5*mm

    # Highlight box
    y -= 10*mm
    draw_rounded_rect(c, left_x, y - 5*mm, 140*mm, 28*mm, radius=4*mm, fill_color=HexColor("#FEF0F0"))
    c.setFillColor(RED)
    c.setFont(FONT_BOLD, 11)
    c.drawString(left_x + 8*mm, y + 12*mm, "Klíčové oblasti spolupráce:")
    c.setFillColor(DARK)
    c.setFont(FONT, 10)
    c.drawString(left_x + 8*mm, y + 1*mm, "Web & Blog  ·  Sociální sítě  ·  Vybavení  ·  Content & PR")

    # Right column - image
    img_x = W * 0.55
    img_y = 25*mm
    img_w = W * 0.4
    img_h = H - 55*mm

    draw_rounded_rect(c, img_x, img_y, img_w, img_h, radius=6*mm, fill_color=HexColor("#EEEEEE"))
    c.saveState()
    path = c.beginPath()
    path.roundRect(img_x, img_y, img_w, img_h, 6*mm)
    c.clipPath(path, stroke=0)
    draw_image_safe(c, os.path.join(ASSETS, "hero-cyclists.png"),
                    img_x, img_y, img_w, img_h)
    c.restoreState()

    # Red bar at bottom of image
    c.setFillColor(RED)
    c.rect(img_x, img_y, img_w, 4*mm, fill=1, stroke=0)

    draw_page_number(c, 2, TOTAL_PAGES)


def draw_pillar_card(c, x, y, w, h, number, title, description, bullets):
    """Draw a pillar card."""
    # Card background
    draw_rounded_rect(c, x, y, w, h, radius=4*mm, fill_color=WHITE)

    # Red top bar
    c.setFillColor(RED)
    c.rect(x, y + h - 3*mm, w, 3*mm, fill=1, stroke=0)

    # Number circle
    c.setFillColor(RED)
    c.circle(x + 16*mm, y + h - 16*mm, 10, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 10)
    c.drawCentredString(x + 16*mm, y + h - 19.5*mm, str(number))

    # Title
    c.setFillColor(DARK)
    c.setFont(FONT_BOLD, 13)
    c.drawString(x + 28*mm, y + h - 18*mm, title)

    # Description
    c.setFillColor(GRAY)
    c.setFont(FONT, 9)
    desc_y = y + h - 30*mm
    c.drawString(x + 8*mm, desc_y, description)

    # Bullets
    bullet_y = desc_y - 12*mm
    for bullet_text in bullets:
        draw_bullet(c, x + 8*mm, bullet_y, bullet_text, font_size=9)
        bullet_y -= 7*mm


def page_pillars_1(c):
    """Page 3: Pillars 1 & 2."""
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_red_bar(c, H - 8*mm)

    # Section number
    c.setFillColor(RED)
    c.circle(35*mm, H - 30*mm, 12, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 12)
    c.drawCentredString(35*mm, H - 34*mm, "02")

    # Title
    c.setFillColor(DARK)
    c.setFont(FONT_BOLD, 28)
    c.drawString(50*mm, H - 35*mm, "Jak spolu spolupracujeme")

    # Card dimensions
    card_w = (W - 35*mm - 35*mm - 15*mm) / 2
    card_h = H - 70*mm
    card_y = 20*mm

    # Card 1 - Web & Blog
    draw_pillar_card(c, 35*mm, card_y, card_w, card_h,
                     1, "Osobní web a blog",
                     "Tvůj web je tvou digitální vizitkou.",
                     [
                         "Logo Enervit s proklikem na enervit.cz",
                         "Zmínka o produktech v reportech ze závodů",
                         "Tipy a zkušenosti pro ostatní sportovce",
                         "Přirozené začlenění do obsahu",
                     ])

    # Card 2 - Social Media
    draw_pillar_card(c, 35*mm + card_w + 15*mm, card_y, card_w, card_h,
                     2, "Facebook a Instagram",
                     "Buduj komunitu přirozených příspěvků.",
                     [
                         "Pravidelné fotky s produkty celou sezónu",
                         "Označování @enervit_czsk a @sportujlepe",
                         "Reels a videa přímo z místa dění",
                         "Sdílení novinek, soutěží a seminářů",
                     ])

    draw_page_number(c, 3, TOTAL_PAGES)


def page_pillars_2(c):
    """Page 4: Pillars 3 & 4."""
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_red_bar(c, H - 8*mm)

    # Continuation label
    c.setFillColor(GRAY)
    c.setFont(FONT, 10)
    c.drawString(35*mm, H - 25*mm, "Jak spolu spolupracujeme (pokračování)")

    # Card dimensions
    card_w = (W - 35*mm - 35*mm - 15*mm) / 2
    card_h = H - 55*mm
    card_y = 20*mm

    # Card 3 - Equipment
    draw_pillar_card(c, 35*mm, card_y, card_w, card_h,
                     3, "Vybavení a reprezentace",
                     "Reprezentuješ značku přímo v terénu.",
                     [
                         "Logo na závodním i tréninkovém oblečení",
                         "Branding na vybavení (helma, kolo, láhve)",
                         "Bidon Enervit u stupňů vítězů",
                         "Samolepky a nášivky na vybavení",
                     ])

    # Card 4 - Content & PR
    draw_pillar_card(c, 35*mm + card_w + 15*mm, card_y, card_w, card_h,
                     4, "Content a PR spolupráce",
                     "Tvá data jsou cenné pro další propagaci.",
                     [
                         "Fotky a informace z klíčových závodů",
                         "Cca 10 kvalitních fotek s produkty",
                         "Zmínky o Enervitu v rozhovorech",
                         "Účast na videích, focení a seminářích",
                     ])

    draw_page_number(c, 4, TOTAL_PAGES)


def page_gallery(c):
    """Page 5: Photo gallery."""
    c.setFillColor(DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Red accent at top
    c.setFillColor(RED)
    c.rect(0, H - 8*mm, W, 8*mm, fill=1, stroke=0)

    # Title
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 28)
    c.drawString(35*mm, H - 38*mm, "Naši sportovci v akci")

    c.setFillColor(Color(1, 1, 1, alpha=0.6))
    c.setFont(FONT, 12)
    c.drawString(35*mm, H - 52*mm, "Autentické momenty ze závodů, tréninků a každodenního sportu")

    # Gallery grid - 4 images
    images = [
        ("gravel-rider.png", "Gravel cyklista"),
        ("gel-bike.png", "Gel na kole"),
        ("hockey-player.png", "Hokejista"),
        ("mtb-forest.png", "MTB v lese"),
    ]

    img_w = (W - 35*mm - 35*mm - 3 * 8*mm) / 4
    img_h = H - 80*mm
    start_x = 35*mm
    start_y = 18*mm

    for i, (filename, label) in enumerate(images):
        x = start_x + i * (img_w + 8*mm)

        # Rounded rect background
        draw_rounded_rect(c, x, start_y, img_w, img_h, radius=4*mm, fill_color=HexColor("#333333"))

        # Clip and draw image
        c.saveState()
        path = c.beginPath()
        path.roundRect(x, start_y, img_w, img_h, 4*mm)
        c.clipPath(path, stroke=0)
        draw_image_safe(c, os.path.join(ASSETS, filename),
                        x, start_y, img_w, img_h)
        c.restoreState()

        # Red bottom accent
        c.setFillColor(RED)
        c.rect(x, start_y, img_w, 3*mm, fill=1, stroke=0)

    draw_page_number(c, 5, TOTAL_PAGES)


def page_social(c):
    """Page 6: Social media & tips."""
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_red_bar(c, H - 8*mm)

    # Section number
    c.setFillColor(RED)
    c.circle(35*mm, H - 30*mm, 12, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 12)
    c.drawCentredString(35*mm, H - 34*mm, "03")

    # Title
    c.setFillColor(DARK)
    c.setFont(FONT_BOLD, 28)
    c.drawString(50*mm, H - 35*mm, "Sociální sítě a tipy")

    # Left column - profiles
    left_x = 35*mm
    col_w = (W - 35*mm - 35*mm - 20*mm) / 2

    # Profiles box
    draw_rounded_rect(c, left_x, 20*mm, col_w, H - 65*mm, radius=4*mm, fill_color=LIGHT_BG)

    c.setFillColor(DARK)
    c.setFont(FONT_BOLD, 14)
    c.drawString(left_x + 10*mm, H - 65*mm, "Naše profily")

    # Instagram
    profile_y = H - 88*mm
    draw_rounded_rect(c, left_x + 8*mm, profile_y, col_w - 16*mm, 20*mm, radius=3*mm, fill_color=WHITE)
    c.setFillColor(HexColor("#E1306C"))
    c.circle(left_x + 20*mm, profile_y + 10*mm, 8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 8)
    c.drawCentredString(left_x + 20*mm, profile_y + 7.5*mm, "IG")
    c.setFillColor(DARK)
    c.setFont(FONT_BOLD, 11)
    c.drawString(left_x + 32*mm, profile_y + 11*mm, "@enervit_czsk")
    c.setFillColor(GRAY)
    c.setFont(FONT, 9)
    c.drawString(left_x + 32*mm, profile_y + 3*mm, "Instagram")

    # Facebook
    profile_y -= 28*mm
    draw_rounded_rect(c, left_x + 8*mm, profile_y, col_w - 16*mm, 20*mm, radius=3*mm, fill_color=WHITE)
    c.setFillColor(HexColor("#1877F2"))
    c.circle(left_x + 20*mm, profile_y + 10*mm, 8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 8)
    c.drawCentredString(left_x + 20*mm, profile_y + 7.5*mm, "FB")
    c.setFillColor(DARK)
    c.setFont(FONT_BOLD, 11)
    c.drawString(left_x + 32*mm, profile_y + 11*mm, "@sportujlepe")
    c.setFillColor(GRAY)
    c.setFont(FONT, 9)
    c.drawString(left_x + 32*mm, profile_y + 3*mm, "Facebook")

    # Web
    profile_y -= 28*mm
    draw_rounded_rect(c, left_x + 8*mm, profile_y, col_w - 16*mm, 20*mm, radius=3*mm, fill_color=WHITE)
    c.setFillColor(RED)
    c.circle(left_x + 20*mm, profile_y + 10*mm, 8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 7)
    c.drawCentredString(left_x + 20*mm, profile_y + 7.5*mm, "WEB")
    c.setFillColor(DARK)
    c.setFont(FONT_BOLD, 11)
    c.drawString(left_x + 32*mm, profile_y + 11*mm, "enervit.cz")
    c.setFillColor(GRAY)
    c.setFont(FONT, 9)
    c.drawString(left_x + 32*mm, profile_y + 3*mm, "Oficiální web")

    # Right column - tips
    right_x = left_x + col_w + 20*mm

    c.setFillColor(DARK)
    c.setFont(FONT_BOLD, 14)
    c.drawString(right_x, H - 65*mm, "Tipy pro příspěvky")

    tips = [
        ("1", "Buď autentický", "Fotky nemusí být strojené. Zátiší s výbavou,\nfotka z tréninku nebo momentka s bidonem."),
        ("2", "Publikuj pravidelně", "Sdílej fotky s Enervitem průběžně celou sezónu.\nKonzistentnost je klíčová."),
        ("3", "Označuj profily", "U každého příspěvku nezapomeň označit\n@enervit_czsk a @sportujlepe."),
        ("4", "Toč Reels", "Videa přímo z místa dění mají obrovský\ndosah na sociálních sítích."),
    ]

    tip_y = H - 88*mm
    for num, title, desc in tips:
        # Number circle
        c.setFillColor(RED)
        c.circle(right_x + 6*mm, tip_y + 6*mm, 8, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 9)
        c.drawCentredString(right_x + 6*mm, tip_y + 3.5*mm, num)

        # Tip title
        c.setFillColor(DARK)
        c.setFont(FONT_BOLD, 11)
        c.drawString(right_x + 18*mm, tip_y + 6*mm, title)

        # Tip description
        c.setFillColor(GRAY)
        c.setFont(FONT, 9)
        for i, line in enumerate(desc.split('\n')):
            c.drawString(right_x + 18*mm, tip_y - 2*mm - i * 4.5*mm, line)

        tip_y -= 32*mm

    draw_page_number(c, 6, TOTAL_PAGES)


def page_contact(c):
    """Page 7: Contact / CTA."""
    # Full red background
    c.setFillColor(RED)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Subtle dark overlay pattern
    c.setFillColor(Color(0, 0, 0, alpha=0.05))
    c.rect(0, 0, W * 0.4, H, fill=1, stroke=0)

    # White content area (centered)
    content_w = 200*mm
    content_h = 100*mm
    content_x = (W - content_w) / 2
    content_y = (H - content_h) / 2

    # Title
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 36)
    c.drawCentredString(W / 2, content_y + content_h - 10*mm, "Připraven spolupracovat?")

    # Subtitle
    c.setFillColor(Color(1, 1, 1, alpha=0.85))
    c.setFont(FONT, 14)
    c.drawCentredString(W / 2, content_y + content_h - 30*mm,
                        "Kontaktuj nás a staň se součástí týmu sportovců,")
    c.drawCentredString(W / 2, content_y + content_h - 42*mm,
                        "kteří důvěřují Enervitu.")

    # CTA Button
    btn_w = 70*mm
    btn_h = 16*mm
    btn_x = (W - btn_w) / 2
    btn_y = content_y + 15*mm

    draw_rounded_rect(c, btn_x, btn_y, btn_w, btn_h, radius=btn_h/2, fill_color=WHITE)
    c.setFillColor(RED)
    c.setFont(FONT_BOLD, 14)
    c.drawCentredString(W / 2, btn_y + 4.5*mm, "hello@enervit.cz")

    # Bottom info
    c.setFillColor(Color(1, 1, 1, alpha=0.6))
    c.setFont(FONT, 10)
    c.drawCentredString(W / 2, 25*mm, "enervit.cz  |  @enervit_czsk  |  @sportujlepe")

    # Logo at bottom
    draw_image_safe(c, os.path.join(ASSETS, "enervit-logo.png"),
                    (W - 60*mm) / 2, 8*mm, 60*mm, 14*mm)

    draw_page_number(c, 7, TOTAL_PAGES)


def main():
    c = canvas.Canvas(OUTPUT, pagesize=landscape(A4))
    c.setTitle("Enervit Athletes Guide 2026")
    c.setAuthor("Enervit CZ/SK")
    c.setSubject("Průvodce spoluprací pro ambasadory")

    pages = [
        page_cover,
        page_intro,
        page_pillars_1,
        page_pillars_2,
        page_gallery,
        page_social,
        page_contact,
    ]

    for i, page_func in enumerate(pages):
        page_func(c)
        if i < len(pages) - 1:
            c.showPage()

    c.save()
    print(f"PDF generated: {OUTPUT}")
    print(f"Pages: {len(pages)}")


if __name__ == "__main__":
    main()
