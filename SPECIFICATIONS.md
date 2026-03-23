# Cahier des Charges : MinePattern v1.0.0

## 1. Vision du Projet
**MinePattern** est un studio de création de textures pixel-art spécialisé pour Minecraft. L'objectif est de fournir aux modders et créateurs un outil rapide, ergonomique et visuellement "premium" pour générer des textures cohérentes (blocs, minerais, planches) directement depuis un navigateur ou un appareil mobile.

---

## 2. Objectifs Stratégiques
- **Productivité** : Réduire le temps de création de textures de base (stone variants, ores).
- **Accessibilité** : Interface PWA exploitable sur PC et Mobile (optimisée landscape).
- **Esthétique** : Immersion via un design système "Analog HUD" (Tactical Softness).

---

## 3. Spécifications Fonctionnelles

### 3.1 Moteur de Génération (Texture Engine)
- **Résolutions supportées** : 16x16 (standard), 32x32, 64x64, 128x128.
- **Patterns Procéduraux** :
    - *Basique* : Surface unie avec grain organique.
    - *Minerai (Ore)* : Clusters de pixels pour veines précieuses.
    - *Briques* : Structure géométrique avec mortier.
    - *Cobblestone* : Cellules de pierre arrondies aléatoires.
    - *Planches* : Lignes de bois avec veinage.
- **Filtres** : Intensité du bruit (Noise) réglable pour une texture plus ou moins "organique".

### 3.2 Contrôle de la Palette
- **Édition Directe** : Contrôle précis de 4 teintes (Base, Reflet, Ombre, Détail).
- **Presets Intégrés** : Palettes rapides (Stone, Diamond, Gold, Obsidian, Emerald).

### 3.3 Interface & Visualisation
- **Vue Pixel-Perfect** : Interpolation NEAREST pour éviter le flou de zoom.
- **Zoom Dynamique** : De x1 à x16.
- **Mode Grille (Tiles)** : Aperçu 4x4 pour tester la "tesselation" (répétition du motif).
- **HUD Clean** : Masquage des éléments Streamlit natifs pour une immersion totale.

### 3.4 Exportation
- **Format** : PNG Production (couleur 32-bit).
- **Nommage** : Automatisé selon résolution et pattern.

---

## 4. Design System : "The Analog HUD"
Le design suit une direction artistique de type **Interface Tactique Rétro-Futuriste**.
- **Couleurs** : Base Charcoal (#131313) et accents Or/Jaune instrumentaux (#F1E09C).
- **Typographie** : Space Grotesk (Labels techniques, All-Caps) et Inter (Contenu).
- **Formes** : Rayons de courbure extrêmes (Pill geometry - 3rem).
- **Effets** : Glassmorphism, tonal layering (pas de bordures 1px), animations de type "powering-up".

---

## 5. Spécifications Techniques
- **Langage** : Python 3.x
- **Framework UI** : Streamlit
- **Traitement d'Image** : Pillow (PIL)
- **Versioning** : Git / GitHub (pointnod/MinePattern)
- **Wrapper PWA** : index.html avec Manifest JSON et iframe responsive.

---

## 6. Roadmap & Évolutions Futures
- [ ] Support des calques (Layers).
- [ ] Export direct vers des pack de ressources Minecraft (.mcmeta).
- [ ] Galerie de presets communautaires.
- [ ] Outils de dessin manuel pour retouches pixel-art directes.
