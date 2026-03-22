import streamlit as st
from PIL import Image, ImageDraw
import random
import io

# Configuration de la page pour le mobile
st.set_page_config(page_title="ReaCraft Texture Studio", layout="centered")

def create_texture(size, base_color, highlight_color, shadow_color, detail_color, noise_val, pattern_type):
    # Création de l'image de base (RGBA pour la transparence)
    img = Image.new('RGBA', (size, size), base_color)
    draw = ImageDraw.Draw(img)

    # 1. Ajout du Bruit de fond (Texture organique)
    for x in range(size):
        for y in range(size):
            var = random.randint(-noise_val, noise_val)
            r = max(0, min(255, base_color[0] + var))
            g = max(0, min(255, base_color[1] + var))
            b = max(0, min(255, base_color[2] + var))
            draw.point((x, y), fill=(r, g, b, 255))

    # 2. Bordures 3D (Effet classique Minecraft)[cite: 1]
    # Lignes claires (Haut/Gauche)
    draw.line([(0, 0), (size-1, 0)], fill=highlight_color, width=1)
    draw.line([(0, 0), (0, size-1)], fill=highlight_color, width=1)
    # Lignes sombres (Bas/Droite)
    draw.line([(size-1, 0), (size-1, size-1)], fill=shadow_color, width=1)
    draw.line([(0, size-1), (size-1, size-1)], fill=shadow_color, width=1)

    # 3. Application du Pattern (Motif)
    if pattern_type == "Minerai (Ore)":
        # Coordonnées proportionnelles à la taille[cite: 1]
        density = size // 4
        for _ in range(density):
            px = random.randint(2, size-3)
            py = random.randint(2, size-3)
            draw.point((px, py), fill=detail_color)
            # Ombre sous le détail pour le relief[cite: 1]
            if py < size - 1:
                draw.point((px, py+1), fill=shadow_color)
    
    elif pattern_type == "Briques":
        for i in range(0, size, size//4):
            draw.line([(0, i), (size, i)], fill=shadow_color)
            offset = (size//8) if (i // (size//4)) % 2 == 0 else 0
            for j in range(offset, size, size//2):
                draw.line([(j, i), (j, i + size//4)], fill=shadow_color)

    return img

# --- INTERFACE GRAPHIQUE ---
st.title("🎨 ReaCraft Studio")
st.write("Générateur de textures Pixel-Perfect pour Minecraft.")

# Sidebar pour les réglages (optimisé mobile)
with st.expander("⚙️ Paramètres de la Texture", expanded=True):
    res = st.selectbox("Résolution", [16, 32, 64], index=0)
    pattern = st.radio("Pattern", ["Basique", "Minerai (Ore)", "Briques"])
    noise = st.slider("Intensité du grain (Bruit)", 0, 50, 15)

with st.expander("🌈 Palette de Couleurs"):
    c1, c2 = st.columns(2)
    with c1:
        base = st.color_picker("Couleur de Base", "#4664B4")
        high = st.color_picker("Reflet (Highlight)", "#78A0FF")
    with c2:
        shad = st.color_picker("Ombre (Shadow)", "#283C78")
        det = st.color_picker("Détails (Ore/Pattern)", "#B4DCFF")

# Conversion des couleurs hex en RGB[cite: 1]
hex_to_rgb = lambda h: tuple(int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

# Génération
if st.button("✨ Générer la Texture", use_container_width=True):
    final_img = create_texture(
        res, 
        hex_to_rgb(base), 
        hex_to_rgb(high), 
        hex_to_rgb(shad), 
        hex_to_rgb(det), 
        noise,
        pattern
    )

    # Affichage Pixel Perfect (Agrandi pour aperçu)
    st.subheader("Aperçu Production")
    st.image(final_img, width=300, output_format="PNG")

    # Préparation du téléchargement[cite: 1]
    buf = io.BytesIO()
    final_img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="💾 Télécharger l'Asset (.png)",
        data=byte_im,
        file_name=f"reacraft_{res}x_{pattern.lower()}.png",
        mime="image/png",
        use_container_width=True
    )