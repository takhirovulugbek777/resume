import requests

bot_token = '6809856711:AAFOihMbrCVSzUdXQ1VFz2u8fJuOfZ99Fp4'  # Replace with your Telegram bot token
url = f'https://api.telegram.org/bot{bot_token}/getUpdates'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    if data.get('result') and data['result']:
        chat_id = data['result'][0]['message']['chat']['id']
        print(f"The chat ID is: {chat_id}")
    else:
        print("No messages found in the chat.")
else:
    print(f"Failed to get updates. Status code: {response.status_code}")
