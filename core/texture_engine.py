"""Core texture generation engine for MinePattern v1.0.0.

Modular, type-annotated class-based engine for generating Minecraft-style textures.
Supports multiple patterns with 3D bevels and noise.
"""

from typing import Tuple
from PIL import Image, ImageDraw
import random
from utils import RGBColor, clamp

class TextureEngine:
    def __init__(self, size: int = 16):
        self.size = size

    def create_texture(
        self,
        base_color: RGBColor,
        highlight_color: RGBColor,
        shadow_color: RGBColor,
        detail_color: RGBColor,
        noise_val: int = 15,
        pattern_type: str = "Basique"
    ) -> Image.Image:
        img = Image.new('RGB', (self.size, self.size), base_color)
        draw = ImageDraw.Draw(img)
        
        self._add_noise(img, draw, base_color, noise_val)
        self._add_bevels(draw)
        
        if pattern_type == "Minerai (Ore)":
            self._add_ore_pattern(draw, detail_color, shadow_color)
        elif pattern_type == "Briques":
            self._add_brick_pattern(draw, shadow_color)
        
        return img

    def _add_noise(self, img: Image.Image, draw: ImageDraw.ImageDraw, base: RGBColor, intensity: int) -> None:
        size = self.size
        for x in range(size):
            for y in range(size):
                var = random.randint(-intensity, intensity)
                r = clamp(base[0] + var)
                g = clamp(base[1] + var)
                b = clamp(base[2] + var)
                draw.point((x, y), fill=(r, g, b))

    def _add_bevels(self, draw: ImageDraw.ImageDraw) -> None:
        size = self.size
        draw.line([(0, 0), (size-1, 0)], fill=(255, 255, 255), width=1)
        draw.line([(0, 0), (0, size-1)], fill=(255, 255, 255), width=1)
        draw.line([(size-1, 0), (size-1, size-1)], fill=(0, 0, 0), width=1)
        draw.line([(0, size-1), (size-1, size-1)], fill=(0, 0, 0), width=1)

    def _add_ore_pattern(self, draw: ImageDraw.ImageDraw, detail: RGBColor, shadow: RGBColor) -> None:
        density = self.size // 4
        for _ in range(density):
            px, py = random.randint(2, self.size-3), random.randint(2, self.size-3)
            draw.point((px, py), fill=detail)
            if py < self.size - 1:
                draw.point((px, py + 1), fill=shadow)

    def _add_brick_pattern(self, draw: ImageDraw.ImageDraw, shadow: RGBColor) -> None:
        size = self.size
        brick_h = size // 4
        for i in range(0, size, brick_h):
            draw.line([(0, i), (size, i)], fill=shadow)
            offset = (size // 8) if (i // brick_h) % 2 == 0 else 0
            for j in range(offset, size, size // 2):
                draw.line([(j, i), (j, i + brick_h)], fill=shadow)
