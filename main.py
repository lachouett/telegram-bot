from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8619884398:AAF6LfVgtxEExNRhTM181PdsHggAmAI0UCM"
ADMIN_ID = 5672707695

# ================= DATA =================

categories = ["chaussures", "T-shirt", "short", "pull"]

shoe_brands = ["Nike", "Adidas", "New Balance"]

shoe_models = {
    "Nike": ["Air Force 1", "TN"],
    "Adidas": ["Samba"],
    "New Balance": ["2002R"]
}

products = {
    "Nike_Air Force 1": {
        "img": "https://i.imgur.com/OZ8FQ0M.png"
    },
    "Nike_TN": {
        "img": "https://i.imgur.com/Z9qv7Qn.png"
    },
    "Adidas_Samba": {
        "img": "https://i.imgur.com/Q7SKX7N.png"
    },
    "New Balance_2002R": {
        "img": "https://i.imgur.com/Q7SKX7N.png"
    }
}

user_cart = {}
user_waiting_phone = {}

# ================= MENUS =================

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(c, callback_data=f"cat_{c}")]
        for c in categories
    ])


def shoe_brand_menu():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(b, callback_data=f"brand_{b}")]
         for b in shoe_brands] +
        [[InlineKeyboardButton("🛒 Voir panier", callback_data="cart")]]
    )


def shoe_model_menu(brand):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(m,
         callback_data=f"model_{brand}_{m}")]
         for m in shoe_models[brand]] +
        [[InlineKeyboardButton("⬅️ Retour", callback_data="back")]]
    )


def cart_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Commander", callback_data="checkout")],
        [InlineKeyboardButton("🗑 Vider panier", callback_data="clear")],
        [InlineKeyboardButton("⬅️ Retour", callback_data="back")]
    ])


def phone_menu():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("📱 Partager numéro",
         request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

# ================= START =================

async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE):

    user_cart[update.effective_user.id] = []

    await update.message.reply_text(
        "Bienvenue 👋 Choisis une catégorie :",
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

# -------- CATEGORIES --------

    if data.startswith("cat_"):

        cat = data.split("_")[1]

        if cat == "chaussures":

            await query.edit_message_text(
                "Choisis une marque 👟",
                reply_markup=shoe_brand_menu()
            )

        else:

            await query.edit_message_text(
                f"{cat} bientôt dispo 🔥",
                reply_markup=main_menu()
            )

# -------- BRANDS --------

    elif data.startswith("brand_"):

        brand = data.split("_")[1]

        await query.edit_message_text(
            "Choisis un modèle 👇",
            reply_markup=shoe_model_menu(brand)
        )

# -------- MODELS --------

    elif data.startswith("model_"):

        parts = data.split("_")

        brand = parts[1]
        model = parts[2]

        key = f"{brand}_{model}"

        user_cart[user_id].append(key)

        product = products.get(key)

        if product:

            await query.message.reply_photo(
                product["img"],
                caption=f"{model} ajouté au panier 🛒"
            )

# -------- CART --------

    elif data == "cart":

        cart = user_cart[user_id]

        if not cart:

            await query.edit_message_text(
                "Panier vide 🛒"
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
            "Panier vidé 🗑"
        )

# -------- CHECKOUT --------

    elif data == "checkout":

        user_waiting_phone[user_id] = True

        await query.message.reply_text(
            "Envoie ton numéro 📱",
            reply_markup=phone_menu()
        )

# -------- BACK --------

    elif data == "back":

        await query.edit_message_text(
            "Menu principal",
            reply_markup=main_menu()
        )

# ================= CONTACT =================

async def contact_handler(update: Update,
                          context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user

    if user.id not in user_waiting_phone:
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
        "Commande envoyée ✅",
        reply_markup=ReplyKeyboardRemove()
    )

    user_cart[user.id] = []
    user_waiting_phone[user.id] = False

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
