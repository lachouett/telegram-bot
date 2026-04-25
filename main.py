from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8619884398:AAHu8Uq4yUyfpxWL38u0DDyg_yLyaToW3xY"

# --- CATALOGUE COMPLET ---

catalogue = {

    "Chaussures": {

        "Nike": [
            "Air Force",
            "TN",
            "Air Max 90",
            "Air Max 95",
            "Shox",
            "Vomero",
            "Dunk",
            "Taekwondo"
        ],

        "Adidas": [
            "Spezial",
            "Campus",
            "Gazelle",
            "Samba",
            "Taekwondo"
        ],

        "Asics": [
            "Gel NYC",
            "Kayano 14"
        ],

        "New Balance": [
            "2002R",
            "NB1000",
            "NB2000",
            "NB740",
            "530",
            "550",
            "9060"
        ],

        "Saucony": [
            "Omni9"
        ],

        "Salomon": [
            "XT-6XT"
        ],

        "Prada": [
            "Cup"
        ],

        "Balenciaga": [
            "Track"
        ],

        "Dior": [
            "B22",
            "B30"
        ]

    }

}

# --- CLAVIERS ---

def clavier_categories():
    boutons = [[cat] for cat in catalogue.keys()]
    return ReplyKeyboardMarkup(boutons, resize_keyboard=True)


def clavier_marques(categorie):
    boutons = [[marque] for marque in catalogue[categorie]]
    boutons.append(["🔙 Retour"])
    return ReplyKeyboardMarkup(boutons, resize_keyboard=True)


def clavier_modeles(categorie, marque):
    modeles = catalogue[categorie][marque]

    boutons = [[modele] for modele in modeles]

    boutons.append(["🔙 Retour"])

    return ReplyKeyboardMarkup(boutons, resize_keyboard=True)


# --- START ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "👟 Bienvenue\nChoisis une catégorie :",
        reply_markup=clavier_categories()
    )


# --- MESSAGES ---

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texte = update.message.text

    # 🔙 RETOUR
    if texte == "🔙 Retour":

        if "marque" in context.user_data:
            del context.user_data["marque"]

            categorie = context.user_data["categorie"]

            await update.message.reply_text(
                "Choisis une marque :",
                reply_markup=clavier_marques(categorie)
            )
            return

        if "categorie" in context.user_data:
            del context.user_data["categorie"]

        await update.message.reply_text(
            "Menu principal :",
            reply_markup=clavier_categories()
        )
        return


    # 📦 Catégorie choisie
    if texte in catalogue:

        context.user_data["categorie"] = texte

        await update.message.reply_text(
            "Choisis une marque :",
            reply_markup=clavier_marques(texte)
        )
        return


    # 🏷️ Marque choisie
    if "categorie" in context.user_data:

        categorie = context.user_data["categorie"]

        if texte in catalogue[categorie]:

            context.user_data["marque"] = texte

            await update.message.reply_text(
                f"Modèles disponibles pour {texte} :",
                reply_markup=clavier_modeles(categorie, texte)
            )
            return


    # 👟 Modèle choisi
    if "marque" in context.user_data:

        await update.message.reply_text(
            f"✅ Tu as sélectionné : {texte}"
        )


# --- LANCEMENT ---

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, message)
)

print("Bot lancé...")

app.run_polling()
