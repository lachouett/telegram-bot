from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8619884398:AAF6LfVgtxEExNRhTM181PdsHggAmAI0UCM"
ADMIN_ID = 5672707695

# ================= CATEGORIES =================

categories = [
    "chaussures",
    "T-shirt",
    "pull",
    "short",
    "veste",
    "pantalon",
    "chapeau"
]

brands = {

    "chaussures": [
        "Nike",
        "Adidas",
        "New Balance",
        "Asics",
        "Saucony"
    ],

    "T-shirt": [
        "Nike",
        "Adidas",
        "Lacoste",
        "Ralph Lauren"
    ],

    "pull": [
        "Nike",
        "Adidas",
        "Lacoste",
        "Ralph Lauren"
    ],

    "short": [
        "Nike",
        "Adidas"
    ],

    "veste": [
        "Nike",
        "Adidas",
        "The North Face"
    ],

    "pantalon": [
        "Nike",
        "Adidas"
    ],

    "chapeau": [
        "Nike",
        "New Era"
    ]

}

# MODELES UNIQUEMENT CHAUSSURES

shoe_models = {

    "Nike": [
        "Air Force 1",
        "TN",
        "Shox"
    ],

    "Adidas": [
        "Samba",
        "Gazelle"
    ],

    "New Balance": [
        "2002R",
        "9060"
    ],

    "Asics": [
        "Gel NYC",
        "Gel Kayano 14"
    ],

    "Saucony": [
        "Progrid",
        "Omni9"
    ]

}

user_cart = {}
waiting_phone = {}

# ================= MENUS =================

def main_menu():

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            c,
            callback_data=f"cat_{c}"
        )]
        for c in categories
    ])


def brand_menu(cat):

    return InlineKeyboardMarkup(

        [[InlineKeyboardButton(
            b,
            callback_data=f"brand_{cat}_{b}"
        )] for b in brands[cat]]

        +

        [[InlineKeyboardButton(
            "🛒 Voir panier",
            callback_data="cart"
        )]]

        +

        [[InlineKeyboardButton(
            "⬅️ Retour",
            callback_data="back_main"
        )]]

    )


def shoe_model_menu(cat, brand):

    return InlineKeyboardMarkup(

        [[InlineKeyboardButton(
            m,
            callback_data=f"model_{cat}_{brand}_{m}"
        )] for m in shoe_models[brand]]

        +

        [[InlineKeyboardButton(
            "⬅️ Retour",
            callback_data=f"cat_{cat}"
        )]]

    )


def after_add_menu(cat):

    return InlineKeyboardMarkup([

        [InlineKeyboardButton(
            "⬅️ Continuer achats",
            callback_data=f"cat_{cat}"
        )],

        [InlineKeyboardButton(
            "🛒 Voir panier",
            callback_data="cart"
        )]

    ])


def cart_menu():

    return InlineKeyboardMarkup([

        [InlineKeyboardButton(
            "✅ Commander",
            callback_data="checkout"
        )],

        [InlineKeyboardButton(
            "🗑 Vider panier",
            callback_data="clear"
        )],

        [InlineKeyboardButton(
            "⬅️ Continuer achats",
            callback_data="back_main"
        )]

    ])


def phone_menu():

    return ReplyKeyboardMarkup(

        [[KeyboardButton(
            "📱 Partager mon numéro",
            request_contact=True
        )]],

        resize_keyboard=True,
        one_time_keyboard=True

    )

# ================= START =================

async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE):

    user_cart[update.effective_user.id] = []

    await update.message.reply_text(
        "Menu principal",
        reply_markup=main_menu()
    )

# ================= CALLBACK =================

async def button(update: Update,
                 context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = query.from_user.id

    if user_id not in user_cart:
        user_cart[user_id] = []

# -------- CATEGORY --------

    if data.startswith("cat_"):

        cat = data.split("_")[1]

        await query.edit_message_text(
            "Choisis une marque 👇",
            reply_markup=brand_menu(cat)
        )

# -------- BRAND --------

    elif data.startswith("brand_"):

        parts = data.split("_")

        cat = parts[1]
        brand = parts[2]

        if cat == "chaussures":

            await query.edit_message_text(
                "Choisis un modèle 👇",
                reply_markup=shoe_model_menu(cat, brand)
            )

        else:

            item = f"{cat} {brand}"

            user_cart[user_id].append(item)

            await query.edit_message_text(
                f"{item} ajouté au panier 🛒",
                reply_markup=after_add_menu(cat)
            )

# -------- MODEL (CHAUSSURES) --------

    elif data.startswith("model_"):

        parts = data.split("_")

        cat = parts[1]
        brand = parts[2]
        model = parts[3]

        item = f"{brand} {model}"

        user_cart[user_id].append(item)

        await query.edit_message_text(
            f"{item} ajouté au panier 🛒",
            reply_markup=after_add_menu(cat)
        )

# -------- CART --------

    elif data == "cart":

        cart = user_cart[user_id]

        if not cart:

            await query.edit_message_text(
                "Panier vide 🛒",
                reply_markup=main_menu()
            )

        else:

            text = "\n".join(cart)

            await query.edit_message_text(
                f"Ton panier:\n{text}",
                reply_markup=cart_menu()
            )

# -------- CLEAR --------

    elif data == "clear":

        user_cart[user_id] = []

        await query.edit_message_text(
            "Panier vidé 🗑",
            reply_markup=main_menu()
        )

# -------- CHECKOUT --------

    elif data == "checkout":

        waiting_phone[user_id] = True

        await query.message.reply_text(
            "Partage ton numéro 📱 pour qu’un vendeur te contacte rapidement.",
            reply_markup=phone_menu()
        )

# -------- BACK --------

    elif data == "back_main":

        await query.edit_message_text(
            "Menu principal",
            reply_markup=main_menu()
        )

# ================= CONTACT =================

async def contact_handler(update: Update,
                          context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user

    if user.id not in waiting_phone:
        return

    phone = update.message.contact.phone_number

    cart = user_cart.get(user.id, [])

    text = (
        f"📦 NOUVELLE COMMANDE\n\n"
        f"Client: {user.full_name}\n"
        f"Phone: {phone}\n\n"
        f"Produits:\n"
        + "\n".join(cart)
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=text
    )

    await update.message.reply_text(
        "Commande envoyée ✅ Un vendeur te contactera bientôt.",
        reply_markup=ReplyKeyboardRemove()
    )

    user_cart[user.id] = []
    waiting_phone[user.id] = False

# ================= RUN =================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CallbackQueryHandler(button))

app.add_handler(MessageHandler(
    filters.CONTACT,
    contact_handler
))

print("Bot lancé 🚀")

app.run_polling()
