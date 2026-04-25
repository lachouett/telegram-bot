from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8619884398:AAF6LfVgtxEExNRhTM181PdsHggAmAI0UCM"
ADMIN_ID = 5672707695

# --- DONNÉES ---

catalogue = {

    "Chaussures": {
        "Nike": [],
        "Adidas": [],
        "Asics": [],
        "New Balance": [],
        "Saucony": [],
        "Dior": [],
        "Salomon": [],
        "Prada": [],
        "Balenciaga": []
    },

    "T-shirt": {
        "Nike": [],
        "Adidas": [],
        "Dior": [],
        "Louis Vuitton": [],
        "Gucci": [],
        "Lacoste": [],
        "Prada": [],
        "Stone Island": [],
        "Casa Blanca": [],
        "Balenciaga": [],
        "Ralph Laurent": [],
        "Moncler": [],
        "Bape": [],
        "Essential": [],
        "Fendi": []
    },

    "Short": {
        "Nike": [],
        "Adidas": [],
        "Dior": [],
        "Louis Vuitton": [],
        "Gucci": [],
        "Lacoste": [],
        "Prada": [],
        "Stone Island": [],
        "Casa Blanca": [],
        "Balenciaga": [],
        "Ralph Laurent": [],
        "Moncler": [],
        "Bape": [],
        "Essential": [],
        "Fendi": []
    },

    "Maillot de bain": {
        "Nike": [],
        "Adidas": [],
        "Dior": [],
        "Louis Vuitton": [],
        "Gucci": [],
        "Lacoste": [],
        "Fendi": []
    },

    "Casquette": {
        "Nike": [],
        "Adidas": [],
        "Gucci": [],
        "Dior": [],
        "Fendi": [],
        "Burberry": []
    },

    "Bonnet": {
        "Nike": [],
        "Lacoste": [],
        "Adidas": [],
        "Louis Vuitton": [],
        "Fendi": [],
        "Ralph Laurent": []
    },

    "Jacket": {
        "Stone Island": [],
        "CP Compagnie": [],
        "Ralph Laurent": [],
        "Lacoste": [],
        "Burberry": [],
        "Nike": [],
        "Adidas": []
    },

    "Imperméable": {
        "Stone Island": [],
        "CP Compagnie": [],
        "Ralph Laurent": [],
        "Lacoste": [],
        "Nike": [],
        "Adidas": []
    },

    "Doudoune": {
        "Stone Island": [],
        "CP Compagnie": [],
        "Ralph Laurent": [],
        "Lacoste": [],
        "Burberry": [],
        "Nike": [],
        "Adidas": []
    },

    "Pantalon": {

    },

    "Ceinture": {
        "Gucci": [],
        "Calvin Klein": [],
        "Louis Vuitton": [],
        "Fendi": []
    },

    "Caleçon": {
        "Calvin Klein": []
    }

}

# --- FONCTIONS ---

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
        boutons = [[modele] for modele in modeles]

    boutons.append(["🔙 Retour"])
    return ReplyKeyboardMarkup(boutons, resize_keyboard=True)

# --- COMMANDES ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bienvenue 👋\nChoisis un type d'habit :",
        reply_markup=clavier_categories()
    )

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texte = update.message.text

    # Retour menu principal
    if texte == "🔙 Retour":
        context.user_data.clear()
        await update.message.reply_text(
            "Menu principal :",
            reply_markup=clavier_categories()
        )
        return

    # Catégorie choisie
    if texte in catalogue:
        context.user_data["categorie"] = texte

        await update.message.reply_text(
            f"Marques disponibles pour {texte} :",
            reply_markup=clavier_marques(texte)
        )
        return

    # Marque choisie
    if "categorie" in context.user_data:

        categorie = context.user_data["categorie"]

        if texte in catalogue[categorie]:

            context.user_data["marque"] = texte

            await update.message.reply_text(
                f"Modèles pour {texte} :",
                reply_markup=clavier_modeles(categorie, texte)
            )
            return


# --- LANCEMENT BOT ---

app = ApplicationBuilder().token("8619884398:AAF6LfVgtxEExNRhTM181PdsHggAmAI0UCM").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("Bot lancé...")
app.run_polling()
