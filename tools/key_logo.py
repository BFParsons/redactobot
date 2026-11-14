# Copyright 2026 The Redactobot Authors
# SPDX-License-Identifier: Apache-2.0

"""Key the v2 logo. Robot (left): remove only black connected to the border, so the screen and
inner shading stay. Wordmark (right): remove all black, letter counters included, by colour-to-alpha.
Writes a dark-theme and a light-theme (wordmark outlined) WebP, cropped to the art.
"""

import numpy as np
from PIL import Image
from scipy import ndimage

im = np.asarray(Image.open("logo2.jpg").convert("RGB")).astype(np.float32)
h, w, _ = im.shape
mx = im.max(axis=2)
art = mx > 40
ys, xs = np.where(art)
cols = art[int(h * 0.1) : int(h * 0.9)].any(axis=0)
# split between robot and wordmark: the widest empty column run in the middle third
gap_x = None
run = 0
best = 0
for x in range(int(w * 0.25), int(w * 0.5)):
    run = run + 1 if not cols[x] else 0
    if run > best:
        best, gap_x = run, x - run // 2
print("split at", gap_x)
labels, _ = ndimage.label(mx < 40)
border = set(
    np.unique(
        np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]])
    )
) - {0}
bg = np.isin(labels, list(border))
alpha = np.ones((h, w), np.float32)
rgb = im.copy()
LO, HI = 22, 70
soft = np.clip((mx - LO) / (HI - LO), 0, 1)
# robot side: border-connected dark fades out softly
left = np.zeros((h, w), bool)
left[:, :gap_x] = True
# Robot: a solid silhouette (art closed, holes filled, grown a few px) keeps its dark sprite
# outline intact; only black outside it is removed, with an anti-aliased edge.
body = ndimage.binary_closing(art & left, iterations=12)
body = ndimage.binary_fill_holes(body)
body = ndimage.binary_dilation(body, iterations=3) & left
edge = ndimage.gaussian_filter(body.astype(np.float32), 1.2)
alpha[left] = (
    np.maximum(edge[left], np.where(body, 1, 0)[left] * 0)
    if False
    else edge[left]
)
alpha[left & body] = np.maximum(alpha[left & body], 0.0)
# wordmark side: every dark pixel fades out (colour-to-alpha, unpremultiplied)
right = ~left
alpha[right] = soft[right]
un = np.clip(im / np.maximum(alpha, 1e-3)[..., None], 0, 255)
rgb[right] = un[right]


def save(a, c, name):
    out = np.dstack([c, a * 255]).astype(np.uint8)
    img = Image.fromarray(out, "RGBA")
    bbox = img.getchannel("A").point(lambda v: 255 if v > 12 else 0).getbbox()
    pad = 12
    img = img.crop(
        (
            max(0, bbox[0] - pad),
            max(0, bbox[1] - pad),
            min(w, bbox[2] + pad),
            min(h, bbox[3] + pad),
        )
    )
    img = img.resize((900, round(900 * img.height / img.width)), Image.LANCZOS)
    img.save(name + ".webp", quality=90, method=6)
    img.save(name + ".png")
    print(name, img.size)


save(alpha, rgb, "redactobot-logo")
# light theme: thin dark outline behind the wordmark so pale letters read on white
solid = alpha > 0.5
ring = ndimage.binary_dilation(solid, iterations=5) & ~solid & right
ink = np.array([30, 42, 46], np.float32)
a2, c2 = alpha.copy(), rgb.copy()
c2[ring] = rgb[ring] * alpha[ring, None] + ink * (1 - alpha[ring, None])
a2[ring] = 1
save(a2, c2, "redactobot-logo-light")
