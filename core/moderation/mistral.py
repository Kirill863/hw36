
from mistralai import Mistral
from pprint import pprint


def is_bad_review(
    review_text: str,
    api_key: str,
    grades: dict,
) -> bool:
    """
    Проверяет текст отзыва на наличие нежелательного контента с помощью Mistral Moderation API.
    
    :param review_text: Текст отзыва для проверки.
    :param api_key: API-ключ от Mistral AI.
    :param grades: Словарь с порогами для категорий (из settings).
    :return: True, если отзыв содержит нежелательный контент; False — иначе.
    """

    client = Mistral(api_key=api_key)

    try:
        response = client.classifiers.moderate_chat(
            model="mistral-moderation-latest",
            inputs=[{"role": "user", "content": review_text}],
        )

        result = response.results[0].category_scores

        # Округляем до двух знаков после запятой для удобства
        rounded_result = {key: round(value, 2) for key, value in result.items()}

        pprint(rounded_result)

        # Проверяем, превышает ли значение пороговое
        flagged = {
            category: score >= threshold
            for category, score in rounded_result.items()
            if category in grades and isinstance(score, float)
        }

        # Если хотя бы одна категория превышает порог — отзыв нежелательный
        return any(flagged.values())

    except Exception as e:
        print(f"[Mistral API Error] Не удалось выполнить модерацию: {e}")
        return False  # В случае ошибки считаем, что отзыв безопасен