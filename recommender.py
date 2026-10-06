import pandas as pd


def get_recommendations(products, category, budget, preference):
    # Category and budget filter
    filtered = products[
        (products["category"] == category) &
        (products["price"] <= budget)
    ].copy()

    if filtered.empty:
        return filtered

    # Preference matching
    preference_words = preference.lower().split()

    def calculate_score(row):
        text = (
            str(row["description"]) + " " +
            str(row["brand"]) + " " +
            str(row["name"])
        ).lower()

        matches = sum(word in text for word in preference_words)

        preference_score = matches / max(len(preference_words), 1)

        # Rating contributes to the score
        rating_score = row["rating"] / 5

        return (preference_score * 0.7) + (rating_score * 0.3)

    filtered["match_score"] = filtered.apply(
        calculate_score,
        axis=1
    )

    # Highest match first
    filtered = filtered.sort_values(
        "match_score",
        ascending=False
    )

    return filtered.head(3)