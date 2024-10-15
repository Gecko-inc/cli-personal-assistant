import os

from dotenv import load_dotenv

from services.gigachat import GigaChatService

if __name__ == "__main__":
    load_dotenv()
    secret_key = os.environ.get("SECRET_KEY")
    service = GigaChatService(secret_key=secret_key)
    while True:
        text = input("\nВведите запрос: ")
        service.request(text)
