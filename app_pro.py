"""Main entry point for MinePattern v1.0.0 — Analog HUD Edition.

Design System: "The Analog HUD" — tactical softness, glassmorphism, tonal depth.
Fully annotated, PWA-ready for Android/desktop compatibility.
"""

import streamlit as st
from PIL import Image
import io
from core.texture_engine import TextureEngine
from utils import hex_to_rgb, rgb_to_hex

# ─── Page Configuration ───────────────────────────────────────────────────────
# Wide layout for landscape and desktop views.
st.set_page_config(
    page_title="MinePattern — Analog HUD",
    page_icon="🟨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Design System CSS ────────────────────────────────────────────────────────
# Implements the "Analog HUD" design tokens from DESIGN.md:
#   - Charcoal surface hierarchy (#131313 → #1c1b1b → #2a2a2a → #353534)
#   - Muted gold primary (#f1e09c / #d4c483)
#   - Space Grotesk font for tactical readouts
#   - No borders — tonal color shifts define depth
#   - Glassmorphism for floating panels
#   - Extreme corner radii (3rem pill geometry)
#   - Primary used sparingly as a "tactical light"
st.markdown("""
<style>
/* ── Google Fonts ─────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500&display=swap');

/* ── Global Reset & Surface ──────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #131313;
    color: #e5e2e1;
}

/* ── Block Container — Full Width ────────────────────── */
.main .block-container {
    padding: 1.5rem 2rem;
    max-width: 100%;
    background-color: #131313;
}

/* ── Hide Streamlit Chrome ───────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }

/* ── HUD App Title ───────────────────────────────────── */
.hud-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 600;
    letter-spacing: 0.08rem;
    text-transform: uppercase;
    color: #f1e09c;
    margin-bottom: 0.1rem;
}
.hud-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    color: #6b6866;
    letter-spacing: 0.04rem;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* ── Module Panels (tonal layering, no border) ──────── */
.module-panel {
    background-color: #1c1b1b;
    border-radius: 2rem;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.module-panel-high {
    background-color: #2a2a2a;
    border-radius: 1.5rem;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}

/* ── Section Labels ──────────────────────────────────── */
.hud-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.1rem;
    text-transform: uppercase;
    color: #f1e09c;
    margin-bottom: 0.6rem;
    display: block;
}

/* ── Primary CTA Button ──────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #f1e09c 0%, #d4c483 100%) !important;
    color: #131313 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.06rem !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 3rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: 0 4px 24px rgba(212, 196, 131, 0.15) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #d4c483 0%, #b8a85a 100%) !important;
    box-shadow: 0 6px 32px rgba(212, 196, 131, 0.3) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active {
    opacity: 0.7 !important;
    transform: translateY(0px) !important;
}

/* ── Download Button (tertiary style) ───────────────── */
.stDownloadButton > button {
    background: transparent !important;
    color: #f1e09c !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.05rem !important;
    text-transform: uppercase !important;
    border: 1px solid rgba(241, 224, 156, 0.25) !important;
    border-radius: 3rem !important;
    transition: all 0.2s ease-in-out !important;
}
.stDownloadButton > button:hover {
    background: rgba(241, 224, 156, 0.08) !important;
    border-color: rgba(241, 224, 156, 0.5) !important;
}

/* ── Selectbox & Slider Overrides ────────────────────── */
.stSelectbox > div > div, .stSlider > div {
    border-radius: 1rem !important;
}
.stSelectbox [data-baseweb="select"] > div {
    background-color: #2a2a2a !important;
    border: none !important;
    border-radius: 1rem !important;
    color: #e5e2e1 !important;
}
.stSlider [data-baseweb="slider"] {
    margin-top: 0.2rem;
}
/* Slider track fill color — primary gold */
[data-baseweb="slider"] [role="slider"] {
    background: #f1e09c !important;
    border-color: #f1e09c !important;
}

/* ── Metric Cards ────────────────────────────────────── */
[data-testid="metric-container"] {
    background-color: #2a2a2a;
    border-radius: 1.5rem;
    padding: 0.8rem 1rem;
}
[data-testid="metric-container"] label {
    color: #f1e09c !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.08rem !important;
    text-transform: uppercase !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: #e5e2e1 !important;
}

/* ── Preset Chip Buttons ─────────────────────────────── */
.chip-row { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }
.chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background-color: #353534;
    border-radius: 2rem;
    padding: 0.3rem 0.8rem;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.06rem;
    text-transform: uppercase;
    color: #e5e2e1;
    cursor: pointer;
    border: none;
    transition: background 0.15s;
}
.chip-dot {
    width: 6px; height: 6px;
    border-radius: 1px;
    display: inline-block;
}
.chip:hover { background-color: #464644; }

/* ── Image Preview Container ─────────────────────────── */
.preview-wrap {
    background-color: #1c1b1b;
    border-radius: 2rem;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}
/* Glassmorphism overlay for preview label */
.preview-label {
    background: rgba(53, 53, 52, 0.6);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 2rem;
    padding: 0.3rem 0.9rem;
    font-size: 0.6rem;
    letter-spacing: 0.08rem;
    text-transform: uppercase;
    color: #f1e09c;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
}

/* ── Color Pickers ───────────────────────────────────── */
.stColorPicker > div { border-radius: 1rem !important; }
.stColorPicker label {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.06rem !important;
    text-transform: uppercase !important;
    color: #a09d9b !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Preset Palettes ──────────────────────────────────────────────────────────
# Each preset defines (base, highlight, shadow, detail) in hex.
PRESETS = {
    "Stone":    {"base": "#808080", "high": "#A0A0A0", "shad": "#505050", "det": "#C0C0C0"},
    "Diamond":  {"base": "#3CB8D5", "high": "#7AECFF", "shad": "#1A7A8C", "det": "#BFFFFF"},
    "Gold":     {"base": "#D4A017", "high": "#FFD94A", "shad": "#8C6800", "det": "#FFF0A0"},
    "Obsidian": {"base": "#1C0D2B", "high": "#3D2255", "shad": "#0A0514", "det": "#6B44A0"},
    "Emerald":  {"base": "#17A85A", "high": "#4AFFAA", "shad": "#0A5C30", "det": "#A0FFD0"},
}

# Dot colors for the HUD chips (shown next to preset name).
PRESET_DOTS = {
    "Stone": "#808080", "Diamond": "#3CB8D5", "Gold": "#D4A017",
    "Obsidian": "#3D2255", "Emerald": "#17A85A",
}


def apply_preset(name: str) -> None:
    """Inject a preset palette into session state color pickers."""
    p = PRESETS[name]
    st.session_state["base1"] = p["base"]
    st.session_state["high1"] = p["high"]
    st.session_state["shad1"] = p["shad"]
    st.session_state["det1"]  = p["det"]


def render_tile_grid(texture: Image.Image, cols: int = 4) -> Image.Image:
    """Return a tiled grid image (cols x cols) of the texture for preview."""
    w, h = texture.width, texture.height
    grid = Image.new("RGB", (w * cols, h * cols))
    for row in range(cols):
        for col in range(cols):
            grid.paste(texture, (col * w, row * h))
    return grid


def main():
    # ── HUD Header ─────────────────────────────────────────────────────────
    st.markdown('<p class="hud-title">🟨 MinePattern</p>', unsafe_allow_html=True)
    st.markdown('<p class="hud-subtitle">Analog HUD · Texture Studio · v1.0.0</p>', unsafe_allow_html=True)

    # ── Main Layout: Controls | Preview ────────────────────────────────────
    col_ctrl, col_prev = st.columns([1, 1.4], gap="large")

    # ── LEFT PANEL — Controls ───────────────────────────────────────────────
    with col_ctrl:

        # — Preset Palette Chips —
        st.markdown('<span class="hud-label">⬡ Presets</span>', unsafe_allow_html=True)
        chip_html = '<div class="chip-row">'
        for name, dot_color in PRESET_DOTS.items():
            chip_html += (
                f'<span class="chip" onclick="">'
                f'<span class="chip-dot" style="background:{dot_color}"></span>'
                f'{name}</span>'
            )
        chip_html += '</div>'
        st.markdown(chip_html, unsafe_allow_html=True)

        # Streamlit buttons for preset selection (functional fallback)
        preset_cols = st.columns(len(PRESETS))
        for i, (name, _) in enumerate(PRESETS.items()):
            with preset_cols[i]:
                if st.button(name, key=f"preset_{name}", use_container_width=True):
                    apply_preset(name)
                    st.rerun()

        st.markdown("---")

        # — Texture Parameters —
        st.markdown('<span class="hud-label">⚙ Paramètres</span>', unsafe_allow_html=True)
        res = st.selectbox(
            "Résolution",
            [16, 32, 64, 128],
            index=0,
            help="Taille pixel-perfect Minecraft (16 = 1 bloc standard)"
        )
        pattern = st.selectbox(
            "Motif",
            ["Basique", "Minerai (Ore)", "Briques", "Cobblestone", "Planches"],
            index=0,
            help="Type de surface à générer"
        )
        noise = st.slider(
            "Grain / Noise",
            0, 60, 15,
            help="Intensité de la variation organique pixel par pixel"
        )

        # — Color Palette —
        st.markdown("---")
        st.markdown('<span class="hud-label">🎨 Palette</span>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            base = st.color_picker("Base", "#808080", key="base1")
            high = st.color_picker("Reflet", "#A0A0A0", key="high1")
        with c2:
            shad = st.color_picker("Ombre",  "#505050", key="shad1")
            det  = st.color_picker("Détail", "#C0C0C0", key="det1")

        # — Generate Button —
        st.markdown("---")
        if st.button("✦ Générer la texture", use_container_width=True):
            engine = TextureEngine(res)
            texture = engine.create_texture(
                hex_to_rgb(base),
                hex_to_rgb(high),
                hex_to_rgb(shad),
                hex_to_rgb(det),
                noise,
                pattern
            )
            # Persist texture & filename in session state
            st.session_state.texture  = texture
            st.session_state.filename = f"minepattern_{res}px_{pattern.lower().replace(' ', '_')}.png"
            st.rerun()

    # ── RIGHT PANEL — Preview ───────────────────────────────────────────────
    with col_prev:
        st.markdown('<span class="hud-label">🔭 Aperçu</span>', unsafe_allow_html=True)

        if "texture" not in st.session_state:
            # Empty state — placeholder message
            st.markdown(
                '<div style="background:#1c1b1b;border-radius:2rem;padding:3rem;'
                'text-align:center;color:#6b6866;font-size:0.75rem;letter-spacing:0.05rem;">'
                'Aucune texture générée<br><span style="color:#353534;">↑ Configure &amp; génère</span>'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            texture: Image.Image = st.session_state.texture

            # — Zoom Level Selector —
            zoom = st.select_slider(
                "Zoom",
                options=[1, 2, 4, 8, 16],
                value=8,
                format_func=lambda x: f"×{x}",
                help="Zoom pixel-perfect par interpolation NEAREST"
            )

            # — View Mode —
            view_mode = st.radio(
                "Vue",
                ["Pixel · Native", "Pixel · Zoomé", "Grille · 4×4"],
                horizontal=True,
                label_visibility="collapsed"
            )

            zoomed = texture.resize(
                (texture.width * zoom, texture.height * zoom),
                Image.NEAREST
            )
            grid = render_tile_grid(texture, cols=4)

            if view_mode == "Pixel · Native":
                st.image(texture, caption=f"Native {texture.width}×{texture.height}px",
                         use_container_width=False, width=min(texture.width * 4, 300))
            elif view_mode == "Pixel · Zoomé":
                st.image(zoomed, caption=f"Zoom ×{zoom}  —  {zoomed.width}×{zoomed.height}px",
                         use_container_width=True)
            else:
                grid_zoom = grid.resize(
                    (grid.width * max(1, zoom // 2), grid.height * max(1, zoom // 2)),
                    Image.NEAREST
                )
                st.image(grid_zoom, caption="Grille 4×4 — aperçu bloc tiled",
                         use_container_width=True)

            st.markdown("---")

            # — Metrics (HUD readouts) —
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Résolution", f"{texture.width}×{texture.height}")
            with m2:
                st.metric("Motif", pattern.split(" ")[0])
            with m3:
                # File size requires saving first
                buf = io.BytesIO()
                texture.save(buf, format="PNG")
                st.metric("Poids PNG", f"{len(buf.getvalue())} B")

            # — Export Button —
            buf.seek(0)
            st.download_button(
                label="⬇ Exporter PNG",
                data=buf.getvalue(),
                file_name=st.session_state.filename,
                mime="image/png",
                use_container_width=True
            )


if __name__ == "__main__":
    main()
