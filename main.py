from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8619884398:AAF6LfVgtxEExNRhTM181PdsHggAmAI0UCM"
ADMIN_ID = 5672707695

# ================= DATA =================

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
    "chaussures": ["Nike","Adidas","New Balance"],
    "T-shirt": ["Nike","Adidas","Lacoste"],
    "pull": ["Nike","Adidas","Lacoste"],
    "short": ["Nike","Adidas"],
    "veste": ["Nike","Adidas"],
    "pantalon": ["Nike","Adidas"],
    "chapeau": ["Nike"]
}

shoe_models = {
    "Nike": ["Air Force 1","TN"],
    "Adidas": ["Samba"],
    "New Balance": ["2002R"]
}

user_cart = {}
waiting_phone = {}

# ================= MENUS =================

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(c, callback_data=f"cat_{c}")]
        for c in categories
    ])

def brand_menu(cat):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(b, callback_data=f"brand_{cat}_{b}")]
         for b in brands[cat]]
        +
        [[InlineKeyboardButton("🛒 Voir panier", callback_data="cart")]]
        +
        [[InlineKeyboardButton("⬅️ Menu", callback_data="back_main")]]
    )

def model_menu(cat, brand):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(m, callback_data=f"model_{cat}_{brand}_{m}")]
         for m in shoe_models[brand]]
        +
        [[InlineKeyboardButton("⬅️ Retour", callback_data=f"cat_{cat}")]]
    )

def confirm_order_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Oui", callback_data="confirm_order_yes")],
        [InlineKeyboardButton("❌ Non", callback_data="cart")]
    ])

def phone_keyboard():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("📱 Partager mon numéro", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def cart_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Commander", callback_data="checkout")],
        [InlineKeyboardButton("🗑 Vider panier", callback_data="clear")],
        [InlineKeyboardButton("⬅️ Continuer achats", callback_data="back_main")]
    ])

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_cart[update.effective_user.id] = []
    await update.message.reply_text(
        "Bienvenue 👋 Choisis une catégorie :",
        reply_markup=main_menu()
    )

# ================= CALLBACK =================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = query.from_user.id

    if user_id not in user_cart:
        user_cart[user_id] = []

    # CAT
    if data.startswith("cat_"):
        cat = data.split("_")[1]
        await query.edit_message_text(
            "Choisis une marque 👇",
            reply_markup=brand_menu(cat)
        )

    # BRAND
    elif data.startswith("brand_"):
        _, cat, brand = data.split("_", 2)

        if cat == "chaussures":
            await query.edit_message_text(
                "Choisis un modèle 👇",
                reply_markup=model_menu(cat, brand)
            )
        else:
            product = f"{cat} {brand}"
            user_cart[user_id].append(product)

            await query.edit_message_text(
                f"{product} ajouté au panier 🛒",
                reply_markup=cart_menu()
            )

    # MODEL
    elif data.startswith("model_"):
        _, cat, brand, model = data.split("_", 3)

        product = f"{brand} {model}"
        user_cart[user_id].append(product)

        await query.edit_message_text(
            f"{product} ajouté au panier 🛒",
            reply_markup=cart_menu()
        )

    # CART
    elif data == "cart":
        cart = user_cart[user_id]

        if not cart:
            await query.edit_message_text("Panier vide 🛒", reply_markup=main_menu())
        else:
            text = "\n".join(cart)
            await query.edit_message_text(f"Ton panier:\n{text}", reply_markup=cart_menu())

    # CLEAR
    elif data == "clear":
        user_cart[user_id].clear()
        await query.edit_message_text("🗑 Panier vidé.", reply_markup=main_menu())

    # CHECKOUT (FIX ICI)
    elif data == "checkout":
        context.user_data["cart"] = user_cart[user_id]

        await query.message.reply_text(
            "📞 Pour finaliser ta commande, clique sur le bouton en bas 👇",
            reply_markup=phone_keyboard()
        )

    # BACK
    elif data == "back_main":
        await query.edit_message_text(
            "Choisis une catégorie 👇",
            reply_markup=main_menu()
        )

# ================= CONTACT =================

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.contact:
        return

    user = update.message.from_user
    phone = update.message.contact.phone_number
    cart = context.user_data.get("cart", [])

    await update.message.reply_text(
        "Commande envoyée ✅",
        reply_markup=ReplyKeyboardRemove()
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"📦 NOUVELLE COMMANDE\n\n"
            f"👤 {user.full_name}\n"
            f"📞 {phone}\n\n"
            f"🛍 Produits:\n" + "\n".join(cart)
        )
    )

    user_cart[user.id].clear()

# ================= TEXT =================

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# ================= RUN =================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

print("Bot lancé 🚀")
app.run_polling()
