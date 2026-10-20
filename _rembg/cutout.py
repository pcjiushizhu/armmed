"""Remove background from product photo -> white background, auto-crop, save."""
from rembg import remove, new_session
from PIL import Image
import io

SRC = r"e:\MD6000P_Pro\宣传彩页\cc-6000p_pro\447473490938175283.jpg"
DST = r"E:\ArmMed\images\cc6000p_pro_carousel.png"

with open(SRC, "rb") as f:
    data = f.read()

session = new_session("isnet-general-use")
out = remove(data, session=session)  # RGBA bytes

img = Image.open(io.BytesIO(out)).convert("RGBA")

# Composite onto white
white = Image.new("RGBA", img.size, (255, 255, 255, 255))
comp = Image.alpha_composite(white, img)

# Auto-crop to alpha bounding box with margin
alpha = img.getchannel("A")
bbox = alpha.getbbox()
if bbox:
    mx = int((bbox[2] - bbox[0]) * 0.04)
    my = int((bbox[3] - bbox[1]) * 0.04)
    l = max(0, bbox[0] - mx); t = max(0, bbox[1] - my)
    r = min(img.width, bbox[2] + mx); b = min(img.height, bbox[3] + my)
    comp = comp.crop((l, t, r, b))

comp.convert("RGB").save(DST, "PNG", optimize=True)
print("OK ->", DST, comp.size)
