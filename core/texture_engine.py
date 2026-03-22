"""Core texture generation engine for MinePattern v1.0.0 — Analog HUD Edition.

Modular, type-annotated class-based engine for generating Minecraft-style textures.
Supports 5 distinct surface patterns with 3D bevels and organic noise.

Patterns:
    - Basique       : Flat noisy surface with edge bevels.
    - Minerai (Ore) : Scattered pixel clusters for ore veins.
    - Briques       : Horizontal brick rows with mortar lines.
    - Cobblestone   : Random rounded stone cells.
    - Planches      : Horizontal wood planks with grain lines.
"""

from typing import Tuple
from PIL import Image, ImageDraw
import random
from utils import RGBColor, clamp


class TextureEngine:
    """Generate pixel-art Minecraft-style textures at arbitrary sizes."""

    def __init__(self, size: int = 16):
        """Initialize the engine with a target texture size.

        Args:
            size: Width and height of the square output texture (pixels).
        """
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
        """Generate a texture image using the given palette and pattern.

        Args:
            base_color:      RGB tuple for the base fill color.
            highlight_color: RGB tuple for light edge highlights.
            shadow_color:    RGB tuple for dark edges and mortar/joints.
            detail_color:    RGB tuple for ore veins or decorative details.
            noise_val:       Intensity of pixel-by-pixel color variation (0–60).
            pattern_type:    Which surface pattern to render.

        Returns:
            A PIL Image (RGB mode) of size (self.size × self.size).
        """
        # Fill base and apply organic noise
        img = Image.new('RGB', (self.size, self.size), base_color)
        draw = ImageDraw.Draw(img)
        self._add_noise(img, draw, base_color, noise_val)

        # Add classic Minecraft pixel bevels on all edges
        self._add_bevels(draw, highlight_color, shadow_color)

        # Dispatch to the correct surface pattern
        if pattern_type == "Minerai (Ore)":
            self._add_ore_pattern(draw, detail_color, shadow_color)
        elif pattern_type == "Briques":
            self._add_brick_pattern(draw, shadow_color)
        elif pattern_type == "Cobblestone":
            self._add_cobblestone_pattern(draw, shadow_color, highlight_color)
        elif pattern_type == "Planches":
            self._add_plank_pattern(draw, shadow_color, highlight_color)

        return img

    # ─── Private helpers ──────────────────────────────────────────────────

    def _add_noise(
        self,
        img: Image.Image,
        draw: ImageDraw.ImageDraw,
        base: RGBColor,
        intensity: int
    ) -> None:
        """Add per-pixel random color variation to simulate organic texture.

        Args:
            img:       Target image (used for pixel access).
            draw:      ImageDraw bound to img.
            base:      Base RGB color to vary around.
            intensity: Max ± variation per channel.
        """
        size = self.size
        for x in range(size):
            for y in range(size):
                var = random.randint(-intensity, intensity)
                r = clamp(base[0] + var)
                g = clamp(base[1] + var)
                b = clamp(base[2] + var)
                draw.point((x, y), fill=(r, g, b))

    def _add_bevels(
        self,
        draw: ImageDraw.ImageDraw,
        highlight: RGBColor,
        shadow: RGBColor
    ) -> None:
        """Draw classic 1-pixel Minecraft-style bevel edges.

        Top and left edges use the highlight color (light source).
        Bottom and right edges use the shadow color.

        Args:
            draw:      ImageDraw bound to the image.
            highlight: Bright bevel color (top/left).
            shadow:    Dark bevel color (bottom/right).
        """
        s = self.size
        # Highlight (top + left)
        draw.line([(0, 0), (s - 1, 0)], fill=highlight, width=1)
        draw.line([(0, 0), (0, s - 1)], fill=highlight, width=1)
        # Shadow (bottom + right)
        draw.line([(s - 1, 0), (s - 1, s - 1)], fill=shadow, width=1)
        draw.line([(0, s - 1), (s - 1, s - 1)], fill=shadow, width=1)

    def _add_ore_pattern(
        self,
        draw: ImageDraw.ImageDraw,
        detail: RGBColor,
        shadow: RGBColor
    ) -> None:
        """Add scattered ore vein pixel clusters.

        Each cluster is a 2×2 group of detail pixels with a small shadow
        pixel below to simulate depth inside the stone.

        Args:
            draw:   ImageDraw bound to the image.
            detail: Bright ore color.
            shadow: Dark drop-shadow under each ore pixel.
        """
        density = max(4, self.size // 3)
        for _ in range(density):
            px = random.randint(2, self.size - 4)
            py = random.randint(2, self.size - 4)
            # 2×2 cluster
            draw.point((px, py),         fill=detail)
            draw.point((px + 1, py),     fill=detail)
            draw.point((px, py + 1),     fill=detail)
            draw.point((px + 1, py + 1), fill=detail)
            # Drop shadow below the cluster
            if py + 2 < self.size:
                draw.point((px, py + 2), fill=shadow)

    def _add_brick_pattern(
        self,
        draw: ImageDraw.ImageDraw,
        shadow: RGBColor
    ) -> None:
        """Draw Minecraft-style horizontal brick rows with mortar.

        Alternating rows are offset by half a brick width to create
        the classic staggered brick layout.

        Args:
            draw:   ImageDraw bound to the image.
            shadow: Mortar/joint color (drawn as 1-pixel lines).
        """
        size = self.size
        brick_h = max(2, size // 4)  # Height of each brick row
        brick_w = size // 2          # Width of each brick

        for row_idx, y in enumerate(range(0, size, brick_h)):
            # Horizontal mortar line
            draw.line([(0, y), (size, y)], fill=shadow)
            # Vertical mortar lines, offset every other row
            offset = (brick_w // 2) if row_idx % 2 == 0 else 0
            for x in range(offset, size, brick_w):
                draw.line([(x, y), (x, min(y + brick_h, size))], fill=shadow)

    def _add_cobblestone_pattern(
        self,
        draw: ImageDraw.ImageDraw,
        shadow: RGBColor,
        highlight: RGBColor
    ) -> None:
        """Draw a random cobblestone cell pattern.

        Randomly seeds "stone cell centers" and draws rounded blobby
        outlines around them to mimic Minecraft cobblestone.

        Args:
            draw:      ImageDraw bound to the image.
            shadow:    Dark grout color between stones.
            highlight: Light edge glint on the top of each stone.
        """
        size = self.size
        # Number of stones scales with texture size
        num_stones = max(3, size // 4)
        centers = [
            (random.randint(2, size - 3), random.randint(2, size - 3))
            for _ in range(num_stones)
        ]
        for cx, cy in centers:
            r = random.randint(size // 8, size // 5)
            # Draw bounding box of the stone in shadow color
            draw.ellipse(
                [(cx - r, cy - r), (cx + r, cy + r)],
                outline=shadow
            )
            # Small highlight glint in the top-left of the stone
            if cx - r + 1 >= 0 and cy - r + 1 >= 0:
                draw.point((cx - r // 2, cy - r // 2), fill=highlight)

    def _add_plank_pattern(
        self,
        draw: ImageDraw.ImageDraw,
        shadow: RGBColor,
        highlight: RGBColor
    ) -> None:
        """Draw horizontal wood plank rows with grain lines.

        Each plank row gets a dark separation line at the top and
        a subtle highlight line one pixel below to simulate the
        beveled edge of a wooden plank.

        Args:
            draw:      ImageDraw bound to the image.
            shadow:    Dark separation/grain color.
            highlight: Light edge reflection on each plank.
        """
        size = self.size
        plank_h = max(2, size // 4)  # Height of each plank

        for row_idx, y in enumerate(range(0, size, plank_h)):
            # Top separation line (dark joint)
            draw.line([(0, y), (size, y)], fill=shadow)
            # Highlight line 1 pixel below the joint
            if y + 1 < size:
                draw.line([(0, y + 1), (size, y + 1)], fill=highlight)
            # Horizontal grain line in the middle of the plank
            mid = y + plank_h // 2
            if mid < size:
                for x in range(0, size, 2):
                    # Dashed grain line for wood texture realism
                    draw.point((x, mid), fill=shadow)
