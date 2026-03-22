"""Main entry point for MinePattern v1.0.0 - Professional mobile/desktop texture generator.

Optimized for landscape mobile, responsive UI, modular design.
Fully annotated, PWA-ready for Android/desktop compatibility.
"""

import streamlit as st
from PIL import Image
import io
from typing import Tuple
from core.texture_engine import TextureEngine
from utils import hex_to_rgb, rgb_to_hex

# Page config - Wide for landscape, mobile optimized
st.set_page_config(
    page_title="MinePattern Texture Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for pro UI/UX - Mobile landscape friendly
st.markdown("""
<style>
.main .block-container {
    padding-top: 1rem;
    padding-right: 1rem;
    padding-left: 1rem;
    padding-bottom: 1rem;
    max-width: 100%;
}
.stButton > button {
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: all 0.2s;
}
.stButton > button:hover {
    box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    transform: translateY(-2px);
}
.color-picker {
    border-radius: 8px !important;
}
.metric-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 1rem;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🎨 MinePattern v1.0.0")
    st.caption("Texture Studio professionnel - Optimisé mobile/desktop (Android PWA-ready)")

    # Responsive columns for controls/preview
    if st.session_state.get('wide_mode', True):
        col1, col2 = st.columns([1, 1])
    else:
        col1, col2 = st.columns([1, 0])

    with col1:
        st.subheader("⚙️ Paramètres avancés")
        
        # Controls - Touch-friendly sliders
        res = st.selectbox("Résolution", [16, 32, 64, 128], index=0, help="Taille pixel-perfect Minecraft")
        pattern = st.selectbox("Motif", ["Basique", "Minerai (Ore)", "Briques"], index=0)
        noise = st.slider("Grain", 0, 50, 15, help="Texture organique")
        
        st.subheader("🌈 Palette professionnelle")
        c1, c2 = st.columns(2)
        with c1:
            base = st.color_picker("Base", "#4664B4", key="base1")
            high = st.color_picker("Reflet", "#78A0FF", key="high1")
        with c2:
            shad = st.color_picker("Ombre", "#283C78", key="shad1")
            det = st.color_picker("Détail", "#B4DCFF", key="det1")

        if st.button("✨ Générer Texture Pro", use_container_width=True):
            engine = TextureEngine(res)
            texture = engine.create_texture(
                hex_to_rgb(base),
                hex_to_rgb(high),
                hex_to_rgb(shad),
                hex_to_rgb(det),
                noise,
                pattern
            )

            # Save to session for preview
            st.session_state.texture = texture
            st.session_state.filename = f"minepattern_v1_{res}_{pattern.lower()}.png"
            st.rerun()

    with col2:
        st.subheader("🔍 Aperçu HD (Zoomable)")
        if 'texture' in st.session_state:
            texture = st.session_state.texture
            
            # Pixel-perfect zoom preview
            col_zoom1, col_zoom2 = st.columns(2)
            with col_zoom1:
                st.image(texture, width=200, caption="Taille native", use_column_width=True)
            with col_zoom2:
                st.image(texture.resize((texture.width * 8, texture.height * 8), Image.NEAREST), 
                        width=200, caption="Zoom x8 pixels", use_container_width=True)

            # Download pro
            buf = io.BytesIO()
            texture.save(buf, format="PNG")
            st.download_button(
                label="💾 Exporter PNG Production",
                data=buf.getvalue(),
                file_name=st.session_state.filename,
                mime="image/png",
                use_container_width=True
            )
            
            # Stats metrics for pro feel
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("Taille", f"{texture.width}x{texture.height}")
            with col_m2:
                st.metric("Fichier", f"{len(buf.getvalue()):,} octets")
            with col_m3:
                st.metric("Patterns", pattern)

    # Footer pro
    st.markdown("---")
    st.caption("✅ MinePattern v1.0.0 | Fonctionnel Android/Desktop | UI Landscape Mobile | Code modulaire & annoté | Streamlit Cloud Ready")

if __name__ == "__main__":
    main()

