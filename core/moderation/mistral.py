
from mistralai import Mistral
from pprint import pprint

# mistral.py

from mistralai import Mistral
from pprint import pprint


def is_bad_review(review_text: str, api_key: str, grades: dict) -> bool:
    client = Mistral(api_key=api_key)

    response = client.classifiers.moderate_chat(
        model="mistral-moderation-latest",
        inputs=[{"role": "user", "content": review_text}],
    )

    result = response.results[0].category_scores
    rounded_result = {key: round(value, 2) for key, value in result.items()}

    pprint(rounded_result)

    flagged = {
        category: score >= threshold
        for category, score in rounded_result.items()
        if category in grades and isinstance(score, float)
    }

    return any(flagged.values())