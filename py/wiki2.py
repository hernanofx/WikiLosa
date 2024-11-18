from wiki_chatbot import setup_chatbot, run_cli_interface

WIKI_URL = "https://wiki.testing.losa0.com"  # Reemplaza con tu URL
chatbot = setup_chatbot(WIKI_URL)
run_cli_interface(chatbot)