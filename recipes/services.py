
import os
from google import genai


def generate_recipe(products, minutes, vegetarian=False, language="ru"):
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    if not api_key:
        raise ValueError("GEMINI_API_KEY не найден в .env")

    if language == "kk":
        prompt = f"""
        Сен кәсіби аспазсың.
        Берілген өнімдерден рецепт жаса.

        Өнімдер: {products}
        Дайындау уақыты: {minutes} минут
        Етсіз режим: {"Иә" if vegetarian else "Жоқ"}

        Жауап қазақ тілінде болсын.
        Рецепт құрылымы:
        1. Тағам атауы
        2. Ингредиенттер және мөлшері
        3. Дайындау уақыты
        4. Дайындау қадамдары
        5. Аспаз кеңесі
        """
    else:
        prompt = f"""
        Ты профессиональный шеф-повар.
        Создай рецепт из указанных продуктов.

        Продукты: {products}
        Время приготовления: {minutes} минут
        Без мяса: {"Да" if vegetarian else "Нет"}

        Ответ на русском языке.
        Структура:
        1. Название блюда
        2. Ингредиенты с количеством
        3. Время приготовления
        4. Пошаговое приготовление
        5. Совет повара
        """

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        if not response.text:
            raise ValueError("Gemini вернул пустой ответ")

        return response.text

    finally:
        client.close()
