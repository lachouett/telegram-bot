from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8619884398:AAE37x8gTin70b5g0Di6AKsTZHayFrxdHUII"
ADMIN_ID = 5672707695

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

        "Dior": [],

        "Salomon": [
            "XT-6XT"
        ],

        "Prada": [
            "Cup"
        ],

        "Balenciaga": [
            "Track"
        ]

    }

}

# --- CLAVIERS ---

def clavier_categories():
    boutons = [[cat] for cat in catalogue.keys()]
    return ReplyKeyboardMarkup(boutons, resize_keyboard=True)

def clavier_marques(categorie):
    boutons = [[marque] for marque in catalogue[categorie].keys()]
    boutons.append(["🔙 Retour"])
    return ReplyKeyboardMarkup(boutons, resize_keyboard=True)

def clavier_modeles(categorie, marque):
    modeles = catalogue[categorie][marque]

    if not modeles:
        boutons = [["Aucun modèle disponible"]]
    else:
        boutons = [[m] for m in modeles]

    boutons.append(["🔙 Retour"])
    return ReplyKeyboardMarkup(boutons, resize_keyboard=True)

# --- COMMANDES ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Bienvenue 👟\nChoisis une catégorie :",
        reply_markup=clavier_categories()
    )

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texte = update.message.text

    if texte == "🔙 Retour":
        context.user_data.clear()

        await update.message.reply_text(
            "Menu principal :",
            reply_markup=clavier_categories()
        )
        return

    if texte in catalogue:

        context.user_data["categorie"] = texte

        await update.message.reply_text(
            f"Choisis une marque pour {texte} :",
            reply_markup=clavier_marques(texte)
        )
        return

    if "categorie" in context.user_data:

        categorie = context.user_data["categorie"]

        if texte in catalogue[categorie]:

            context.user_data["marque"] = texte

            await update.message.reply_text(
                f"Modèles disponibles pour {texte} :",
                reply_markup=clavier_modeles(categorie, texte)
            )
            return

# --- LANCEMENT ---

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("Bot lancé...")

app.run_polling()
