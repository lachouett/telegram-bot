from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8619884398:AAF6LfVgtxEExNRhTM181PdsHggAmAI0UCM"
ADMIN_ID = 5672707695

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
    "chaussures": ["Nike","Adidas","New Balance","Asics","Saucony"],
    "T-shirt": ["Nike","Adidas","Lacoste","Ralph Lauren"],
    "pull": ["Nike","Adidas","Lacoste","Ralph Lauren"],
    "short": ["Nike","Adidas"],
    "veste": ["Nike","Adidas","The North Face"],
    "pantalon": ["Nike","Adidas"],
    "chapeau": ["Nike","New Era"]
}

shoe_models = {
    "Nike": ["Air Force 1","TN","Shox"],
    "Adidas": ["Samba","Gazelle"],
    "New Balance": ["2002R","9060"],
    "Asics": ["Gel NYC","Gel Kayano 14"],
    "Saucony": ["Progrid","Omni9"]
}

user_cart = {}
waiting_phone = {}

# ================= MENUS =================

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(c,
         callback_data=f"cat_{c}")]
        for c in categories
    ])

def brand_menu(cat):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(
            b,
            callback_data=f"brand_{cat}_{b}"
        )] for b in brands[cat]]
        +
        [[InlineKeyboardButton("🛒 Voir panier",
        callback_data="cart")]]
        +
        [[InlineKeyboardButton("⬅️ Menu",
        callback_data="back_main")]]
    )

def model_menu(cat,brand):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(
            m,
            callback_data=f"model_{cat}_{brand}_{m}"
        )] for m in shoe_models[brand]]
        +
        [[InlineKeyboardButton("⬅️ Retour",
        callback_data=f"cat_{cat}")]]
    )

def confirm_add_menu(cat,brand,item):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "✅ Oui",
            callback_data=f"add_{cat}_{brand}_{item}"
        )],
        [InlineKeyboardButton(
            "❌ Non",
            callback_data=f"cat_{cat}"
        )]
    ])

def confirm_order_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "✅ Oui",
            callback_data="confirm_order_yes"
        )],
        [InlineKeyboardButton(
            "❌ Non",
            callback_data="cart"
        )]
    ])

def confirm_phone_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "📱 Oui partager numéro",
            callback_data="phone_yes"
        )],
        [InlineKeyboardButton(
            "❌ Non continuer",
            callback_data="phone_no"
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

# ================= START =================

async def start(update: Update,
context: ContextTypes.DEFAULT_TYPE):

    user_cart[update.effective_user.id]=[]

    await update.message.reply_text(
        "Bienvenue 👋 Choisis une catégorie :",
        reply_markup=main_menu()
    )

# ================= CALLBACK =================

async def button(update: Update,
context: ContextTypes.DEFAULT_TYPE):

    query=update.callback_query
    await query.answer()

    data=query.data
    user_id=query.from_user.id

    if user_id not in user_cart:
        user_cart[user_id]=[]

    if data.startswith("cat_"):

        cat=data.split("_")[1]

        await query.edit_message_text(
            "Choisis une marque 👇",
            reply_markup=brand_menu(cat)
        )

    elif data.startswith("brand_"):

        parts=data.split("_")

        cat=parts[1]
        brand=parts[2]

        if cat=="chaussures":

            await query.edit_message_text(
                "Choisis un modèle 👇",
                reply_markup=model_menu(cat,brand)
            )

        else:

            await query.edit_message_text(
                f"Ajouter {brand} ({cat}) au panier ?",
                reply_markup=confirm_add_menu(cat,brand,brand)
            )

    elif data.startswith("model_"):

        parts=data.split("_")

        cat=parts[1]
        brand=parts[2]
        model=parts[3]

        await query.edit_message_text(
            f"Ajouter {brand} {model} au panier ?",
            reply_markup=confirm_add_menu(cat,brand,model)
        )

    elif data.startswith("add_"):

        parts=data.split("_")

        brand=parts[2]
        item=parts[3]

        product=f"{brand} {item}"

        user_cart[user_id].append(product)

        await query.edit_message_text(
            f"{product} ajouté au panier 🛒",
            reply_markup=cart_menu()
        )

    elif data=="cart":

        cart=user_cart[user_id]

        if not cart:

            await query.edit_message_text(
                "Panier vide 🛒",
                reply_markup=main_menu()
            )

        else:

            text="\n".join(cart)

            await query.edit_message_text(
                f"Ton panier:\n{text}",
                reply_markup=cart_menu()
            )

    elif data=="clear":

        user_cart[user_id].clear()

        await query.edit_message_text(
            "🗑 Panier vidé.",
            reply_markup=main_menu()
        )

    elif data=="checkout":

        await query.edit_message_text(
            "Es-tu sûr de vouloir commander ?",
            reply_markup=confirm_order_menu()
        )

    elif data=="confirm_order_yes":

        await query.edit_message_text(
            "Souhaites-tu partager ton numéro ?",
            reply_markup=confirm_phone_menu()
        )

    elif data=="phone_yes":

        waiting_phone[user_id]=True

        await query.message.reply_text(
            "Clique sur le bouton ci-dessous pour partager ton numéro 📱",
            reply_markup=phone_menu()
        )

    elif data=="phone_no":

        await send_order(context,user_id,"Non fourni")

        await query.edit_message_text(
            "Commande envoyée sans numéro ✅"
        )

    elif data=="back_main":

        await query.edit_message_text(
            "Choisis une catégorie 👇",
            reply_markup=main_menu()
        )

# ================= CONTACT FIX =================

async def contact_handler(update: Update,
context: ContextTypes.DEFAULT_TYPE):

    user=update.message.from_user

    if not update.message.contact:
        return

    if user.id not in waiting_phone:
        return

    phone=update.message.contact.phone_number

    await send_order(context,user.id,phone)

    await update.message.reply_text(
        "Commande envoyée ✅",
        reply_markup=ReplyKeyboardRemove()
    )

    waiting_phone[user.id]=False

# ================= SEND ORDER =================

async def send_order(context,user_id,phone):

    cart=user_cart.get(user_id,[])

    produits="\n".join(cart)

    message=(
        f"📦 NOUVELLE COMMANDE\n\n"
        f"📞 Numéro: {phone}\n\n"
        f"🛍 Produits:\n{produits}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=message
    )

    user_cart[user_id].clear()

# ================= TEXT =================

async def text_handler(update: Update,
context: ContextTypes.DEFAULT_TYPE):

    await start(update,context)

# ================= RUN =================

app=ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CallbackQueryHandler(button))

app.add_handler(MessageHandler(
    filters.CONTACT,
    contact_handler
))

app.add_handler(MessageHandler(
    filters.TEXT & ~filters.COMMAND,
    text_handler
))

print("Bot lancé 🚀")

app.run_polling()
