"""
EmotionalManaging · Flask Server
Auteur : David Marchal
Sons hébergés sur Cloudflare R2
"""
from flask import Flask, render_template, jsonify, request
import os, json
import anthropic

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
        "title": "Assez Travaillé",
        "tag": "Sonnerie · Remastered",
        "desc": "Une composition ciselée note après note. Le résultat d'heures passées à équilibrer chaque détail.",
        "price": "0,99 €",
        "paypal": "https://paypal.me/DavidMarchal144/0.99",
    },
    {
        "id": "changeffect_remastered",
        "filename": "changeffect_remastered.mp3",
        "title": "ChangEffect",
        "tag": "Sonnerie · Effet x4",
        "desc": "Un effet sonore distinctif, remastérisé quatre fois pour une texture parfaite.",
        "price": "0,99 €",
        "paypal": "https://paypal.me/DavidMarchal144/0.99",
    },
]

for s in SOUNDS:
    s["url"] = f"{R2_BASE}/{s['filename']}"

# Catalogue formaté pour le prompt Claude
CATALOGUE_TEXT = "\n".join(
    f'- id:"{s["id"]}" | titre:"{s["title"]}" | style:{s["tag"]} | desc:{s["desc"]}'
    for s in SOUNDS
)

SYSTEM_PROMPT = f"""Tu es l'assistant de vente d'EmotionalManaging, une boutique de sonneries originales créées par David Marchal.
Tu aides les visiteurs à trouver la sonnerie parfaite pour eux, avec une personnalité chaleureuse, directe et légèrement cool.

Voici le catalogue complet (7 sons à 0,99€ chacun) :
{CATALOGUE_TEXT}

Règles :
- Réponds TOUJOURS en JSON valide avec ce format exact :
  {{"message": "ton texte ici", "recommend": "id_du_son_ou_null"}}
- Recommande un son précis quand c'est pertinent (utilise l'id exact du catalogue).
- Texte court et punchy (2-3 phrases max). Pas de markdown.
- Si l'utilisateur demande à écouter, dis-lui d'appuyer sur le bouton play de la carte.
- Pousse doucement vers l'achat sans être insistant.
- Si hors-sujet, ramène subtilement vers les sonneries.
"""


@app.route("/")
def index():
    return render_template("index.html", sounds=SOUNDS)


@app.route("/api/sounds")
def api_sounds():
    return jsonify(SOUNDS)


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Endpoint IA — reçoit {messages: [...]} et retourne la réponse Claude."""
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "messages requis"}), 400

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return jsonify({"error": "ANTHROPIC_API_KEY manquante"}), 500

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=256,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        raw = response.content[0].text.strip()

        # Parse JSON retourné par Claude
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"message": raw, "recommend": None}

        return jsonify(parsed)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
