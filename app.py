"""
EmotionalManaging · Flask Server
Auteur : David Marchal
Sons hébergés sur Cloudflare R2
"""

from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

R2_BASE = "https://pub-461f0e7bf3a34890a4732878c36699ab.r2.dev"

SOUNDS = [
    {
        "id": "drugs",
        "filename": "Drugsreal.mp3",
        "title": "Drugs",
        "tag": "Sonnerie · Électro",
        "desc": "Un beat électrique et hypnotique. Idéal pour marquer chaque notification d'une touche unique.",
        "price": "0,99 €",
        "paypal": "https://paypal.me/DavidMarchal144/0.99",
    },
    {
        "id": "fm",
        "filename": "Fmreal.mp3",
        "title": "FM",
        "tag": "Sonnerie · Onde",
        "desc": "Des fréquences modulées, comme un signal capté à l'aube. Chaleureux et distinctif.",
        "price": "0,99 €",
        "paypal": "https://paypal.me/DavidMarchal144/0.99",
    },
    {
        "id": "hamme",
        "filename": "Hammereal.mp3",
        "title": "Hamme",
        "tag": "Sonnerie · Impact",
        "desc": "Une frappe nette et affirmée. Pour ne jamais manquer un appel important.",
        "price": "0,99 €",
        "paypal": "https://paypal.me/DavidMarchal144/0.99",
    },
    {
        "id": "playafm",
        "filename": "Playafmreal.mp3",
        "title": "Playa FM",
        "tag": "Sonnerie · Groove",
        "desc": "Un groove solaire, parfait pour les appels qui arrivent comme une bonne nouvelle.",
        "price": "0,99 €",
        "paypal": "https://paypal.me/DavidMarchal144/0.99",
    },
    {
        "id": "wtf",
        "filename": "Wtfreal.mp3",
        "title": "WTF",
        "tag": "Sonnerie · Surprise",
        "desc": "Le son qui fait lever la tête. Pour les appels qui changent tout.",
        "price": "0,99 €",
        "paypal": "https://paypal.me/DavidMarchal144/0.99",
    },
    {
        "id": "assez_travaille_remastered",
        "filename": "assez_travaille_remastered.mp3",
        "title": "Assez_Travaillé_remastered",
        "tag": "Sonnerie · assez_travaille_Remastered",
        "desc": "Une composition ciselée note après note. Le résultat d'heures passées à équilibrer chaque détail.",
        "price": "0,99 €",
        "paypal": "https://paypal.me/DavidMarchal144/0.99",
    },
    {
        "id": "changeffect_remastered",
        "filename": "changeffect_remastered.mp3",
        "title": "changeffect_remastered",
        "tag": "Sonnerie · changeffect_remastered",
        "desc": "Un effet sonore distinctif, remastérisé quatre fois pour une texture parfaite.",
        "price": "0,99 €",
        "paypal": "https://paypal.me/DavidMarchal144/0.99",
    },
]

# Injecter l'URL complète R2 dans chaque son
for s in SOUNDS:
    s["url"] = f"{R2_BASE}/{s['filename']}"


@app.route("/")
def index():
    return render_template("index.html", sounds=SOUNDS)


@app.route("/api/sounds")
def api_sounds():
    return jsonify(SOUNDS)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
