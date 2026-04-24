from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8619884398:AAH1dBUDKUQCD1jC4VLBSXDlQVkt5SaKvK4"
ADMIN_ID = 5672707695

# ---------- CATEGORIES ----------
categories = ["Chaussures", "T-shirt", "Short", "Pull", "Pantalon", "Chapeau", "Veste"]

# ---------- CHAUSSURES ----------
shoe_brands = ["Nike", "Adidas", "Asics", "New Balance", "Saucony"]

shoe_models = {
    "Nike": ["Air Force 1", "TN", "Shox", "Air Max 95", "Air Max 90", "Dunk", "P-6000", "Vomero"],
    "Adidas": ["Samba", "Gazelle", "Campus", "Spezial"],
    "New Balance": ["2002R", "1906R", "9060", "530", "550", "327"],
    "Asics": ["Gel NYC", "Gel Kayano 14", "Gel Cumulus 16", "Gel Nimbus 10.1", "Kayano 12.1", "Gel 1130", "GT-2160"],
    "Saucony": ["Omni9"]
}

# ---------- VÊTEMENTS ----------
clothing_brands = ["Louis Vuitton", "Gucci", "Prada", "Amiri", "Stone Island", "CP Company", "Fendi", "Ralph Lauren"]

pants_brands = ["Nike", "Adidas", "Stone Island"]

# ---------- VESTES ----------
vest_types = ["Jacket", "Doudoune", "Imperméable"]

vest_brands = {
    "Jacket": ["Stone Island", "CP Company", "Burberry"],
    "Doudoune": ["Stone Island", "CP Company", "Burberry"],
    "Imperméable": ["Stone Island", "CP Company"]
}

# ---------- CHAPEAUX ----------
hat_beanie = ["Gucci", "Louis Vuitton", "Lacoste"]
hat_cap = ["Fendi", "Gucci"]

# ---------- TEMP DATA ----------
user_waiting_custom = {}
user_custom_message = {}

# ---------- MENUS ----------
def main_menu():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(c, callback_data=f"cat_{c}")] for c in categories]
    )

# ---------- CHAUSSURES ----------
def shoe_brand_menu():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(b, callback_data=f"shoe_brand_{b}")] for b in shoe_brands] +
        [[InlineKeyboardButton("⬅️ Retour", callback_data="back_main")]]
    )

def shoe_model_menu(brand):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(m, callback_data=f"shoe_model_{brand}_{m}")] for m in shoe_models[brand]] +
        [[InlineKeyboardButton("⬅️ Retour", callback_data="back_shoes")]]
    )

# ---------- VÊTEMENTS ----------
def clothing_menu(category):
    if category == "Pantalon":
        brands = pants_brands
    else:
        brands = clothing_brands

    keyboard = [[InlineKeyboardButton(b, callback_data=f"cloth_{category}_{b}")] for b in brands]
    keyboard.append([InlineKeyboardButton("⭐ Recherche personnalisée", callback_data=f"custom_{category}")])
    keyboard.append([InlineKeyboardButton("⬅️ Retour", callback_data="back_main")])

    return InlineKeyboardMarkup(keyboard)

# ---------- VESTES ----------
def vest_type_menu():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(v, callback_data=f"vest_{v}")] for v in vest_types] +
        [[InlineKeyboardButton("⬅️ Retour", callback_data="back_main")]]
    )

def vest_brand_menu(v_type):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(b, callback_data=f"vest_brand_{v_type}_{b}")] for b in vest_brands[v_type]] +
        [[InlineKeyboardButton("⬅️ Retour", callback_data="cat_Veste")]]
    )

# ---------- CHAPEAUX ----------
def hat_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Bonnet", callback_data="hat_beanie")],
        [InlineKeyboardButton("Casquette", callback_data="hat_cap")],
        [InlineKeyboardButton("⬅️ Retour", callback_data="back_main")]
    ])

def hat_brand_menu(type_):
    brands = hat_beanie if type_ == "beanie" else hat_cap

    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(b, callback_data=f"hat_brand_{type_}_{b}")] for b in brands] +
        [[InlineKeyboardButton("⬅️ Retour", callback_data="cat_Chapeau")]]
    )

# ---------- CONFIRM ----------
def confirm_menu(text):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Confirmer", callback_data=f"confirm_{text}")],
        [InlineKeyboardButton("⬅️ Retour", callback_data="back_main")]
    ])

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenue sur le Shop !\n\nChoisis une catégorie 👇",
        reply_markup=main_menu()
    )

# ---------- AUTO MESSAGE ----------
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_waiting_custom.get(user_id):
        user_custom_message[user_id] = update.message.text
        user_waiting_custom[user_id] = False

        keyboard = [
            [InlineKeyboardButton("✅ Envoyer", callback_data="send_custom")],
            [InlineKeyboardButton("❌ Annuler", callback_data="cancel_custom")]
        ]

        await update.message.reply_text(
            f"📦 Ta demande :\n\n{update.message.text}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await update.message.reply_text("👋 Choisis une catégorie 👇", reply_markup=main_menu())

# ---------- CALLBACK ----------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # catégories
    if data.startswith("cat_"):
        cat = data.split("_")[1]

        if cat == "Chaussures":
            await query.edit_message_text("👟 Choisis une marque 👇", reply_markup=shoe_brand_menu())

        elif cat == "Veste":
            await query.edit_message_text("🧥 Type de veste 👇", reply_markup=vest_type_menu())

        elif cat == "Chapeau":
            await query.edit_message_text("🧢 Choisis 👇", reply_markup=hat_menu())

        else:
            await query.edit_message_text("👕 Choisis une marque 👇", reply_markup=clothing_menu(cat))

    # chaussures marques
    elif data.startswith("shoe_brand_"):
        brand = data.split("_")[2]
        await query.edit_message_text("👟 Modèles 👇", reply_markup=shoe_model_menu(brand))

    # chaussures modèles
    elif data.startswith("shoe_model_"):
        _, _, brand, model = data.split("_", 3)
        await query.edit_message_text(
            f"Tu veux : {model} ({brand}) ?",
            reply_markup=confirm_menu(f"{brand} - {model}")
        )

    # vêtements
    elif data.startswith("cloth_"):
        _, cat, brand = data.split("_", 2)
        await query.edit_message_text(
            f"{brand} ?",
            reply_markup=confirm_menu(f"{brand} ({cat})")
        )

    # vestes types
    elif data.startswith("vest_"):
        v = data.split("_")[1]
        await query.edit_message_text("Choisis une marque 👇", reply_markup=vest_brand_menu(v))

    # vestes marques
    elif data.startswith("vest_brand_"):
        _, _, v_type, brand = data.split("_")
        await query.edit_message_text(
            f"{brand} ({v_type}) ?",
            reply_markup=confirm_menu(f"{brand} - {v_type}")
        )

    # chapeaux
    elif data == "hat_beanie":
        await query.edit_message_text("Bonnet 👇", reply_markup=hat_brand_menu("beanie"))

    elif data == "hat_cap":
        await query.edit_message_text("Casquette 👇", reply_markup=hat_brand_menu("cap"))

    elif data.startswith("hat_brand_"):
        _, _, type_, brand = data.split("_")
        await query.edit_message_text(
            f"{brand} ?",
            reply_markup=confirm_menu(f"{brand} ({type_})")
        )

    # custom
    elif data.startswith("custom_"):
        cat = data.split("_")[1]
        user_waiting_custom[query.from_user.id] = cat

        await query.edit_message_text(
            f"🔍 Recherche personnalisée ({cat})\n\nExemple : Nike TN noir taille 42"
        )

    # confirm
    elif data.startswith("confirm_"):
        text = data.replace("confirm_", "")

        user = query.from_user.username or "No username"

        await query.edit_message_text("✅ Commande envoyée !")

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🛒 Nouvelle commande\n\n@{user}\n{text}"
        )

    # custom send
    elif data == "send_custom":
        msg = user_custom_message.get(query.from_user.id)

        await query.edit_message_text("✅ Envoyé !")

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🔍 Demande custom\n\n@{query.from_user.username}\n{msg}"
        )

    elif data == "cancel_custom":
        await query.edit_message_text("❌ Annulé", reply_markup=main_menu())

    elif data == "back_main":
        await query.edit_message_text("👋 Catégories 👇", reply_markup=main_menu())

# ---------- RUN ----------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))
app.add_handler(CallbackQueryHandler(button))

print("Bot lancé...")
app.run_polling()