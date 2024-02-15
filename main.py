from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

# Dicionário para armazenar informações dos usuários
user_data = {}

# Dicionário que mapeia cada setor para sua lista de produtos
sector_products = {
    "Hospedagem": ["Toalha", "Sabonete", "Shampoo"],
    "Bar": ["Cerveja", "Vinho", "Refrigerante"],
    "Cozinha": ["Arroz", "Feijão", "Óleo"],
    "Buffet": ["Salada", "Carne", "Sobremesa"]
}

# Função para iniciar a conversa com o chatbot
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    context.user_data[user_id] = {}
    update.message.reply_text("Olá! Por favor, me informe seu nome e setor separados por vírgula.")

# Função para receber e armazenar nome e setor do usuário
def set_user_info(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    text = update.message.text
    name, sector = text.split(',')
    context.user_data[user_id]['name'] = name.strip()
    context.user_data[user_id]['sector'] = sector.strip()
    update.message.reply_text("Informações recebidas com sucesso! Agora você pode fazer seu pedido.")

# Função para listar os itens e permitir que o usuário faça o pedido
def make_order(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    sector = context.user_data[user_id]['sector']
    items = sector_products.get(sector)
    if items:
        items_text = "\n".join(items)
        update.message.reply_text(f"Lista de itens disponíveis para {sector}:\n{items_text}\n\nPor favor, digite os itens que deseja e as quantidades.")
    else:
        update.message.reply_text("Desculpe, não foi possível encontrar a lista de itens para o seu setor.")

# Função para receber o pedido do usuário
def receive_order(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    name = context.user_data[user_id]['name']
    sector = context.user_data[user_id]['sector']
    order_text = update.message.text
    # Aqui você pode processar o pedido, enviar para o seu número do Telegram, etc.
    update.message.reply_text(f"Pedido de {name} do setor {sector} recebido com sucesso! Obrigado.")

def main() -> None:
    updater = Updater("AAGyKdGHzgtGzkxE0VOR4qHGVH_REQZo-oE")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.regex(r'^[A-Za-z\s]+,[A-Za-z\s]+$'), set_user_info))
    dispatcher.add_handler(MessageHandler(filters.regex(r'^pedido$'), make_order))
    dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, receive_order))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
