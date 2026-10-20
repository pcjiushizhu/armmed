"""Cut out the bladder scanner from the desk photo, brighten the white shell, export transparent PNG."""
from rembg import remove, new_session
from PIL import Image, ImageEnhance
import os

SRC = r"c:\Users\pc\AppData\Local\Temp\WeChat Files\37046803292056818.jpg"
OUT = r"e:\ArmMed\images\cc6000p_pro_cutout.png"
PREVIEW = r"e:\ArmMed\_rembg\preview_white.png"

img = Image.open(SRC).convert("RGB")
session = new_session("isnet-general-use")
res = remove(
    img,
    session=session,
    alpha_matting=True,
    alpha_matting_foreground_threshold=250,
    alpha_matting_background_threshold=20,
    alpha_matting_erode_size=8,
).convert("RGBA")

# auto crop with margin
alpha = res.getchannel("A")
bbox = alpha.getbbox()
if bbox:
    mx = int((bbox[2] - bbox[0]) * 0.03)
    my = int((bbox[3] - bbox[1]) * 0.03)
    l = max(0, bbox[0] - mx)
    t = max(0, bbox[1] - my)
    r = min(res.width, bbox[2] + mx)
    b = min(res.height, bbox[3] + my)
    res = res.crop((l, t, r, b))

# brighten shell / clean white, keep screen contrast
rgb = res.convert("RGB")
rgb = ImageEnhance.Brightness(rgb).enhance(1.07)
rgb = ImageEnhance.Contrast(rgb).enhance(1.03)
rgb = ImageEnhance.Color(rgb).enhance(1.08)

# lift white point so the shell reads as clean bright white
def lift(v):
    lo, hi = 210, 250
    if v <= lo:
        return v
    return int(min(255, lo + (v - lo) * (255 - lo) / (hi - lo)))

rgb = rgb.point(lift)
res = Image.merge("RGBA", (*rgb.split(), res.getchannel("A")))
res.save(OUT, "PNG", optimize=True)

white = Image.new("RGBA", res.size, (255, 255, 255, 255))
Image.alpha_composite(white, res).convert("RGB").save(PREVIEW, "PNG")
print("OK", res.size, "->", OUT)
