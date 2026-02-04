# AURA Outfit Recommendation Engine (Rule-Based v1)

color_rules = {
    "white": ["blue", "black", "brown"],
    "blue": ["black", "grey", "white"],
    "black": ["blue", "grey"],
    "grey": ["black", "blue"],
    "red": ["black", "blue"],
    "green": ["black", "brown"],
    "yellow": ["blue", "black"],
    "brown": ["blue", "white"]
}

garment_rules = {
    "shirt": ["jeans", "jacket"],
    "tshirt": ["jeans", "jacket"],
    "jeans": ["shirt", "tshirt", "jacket"],
    "jacket": ["shirt", "tshirt", "jeans"]
}


def recommend_outfit(category, color):
    print(f"\n👕 Input Item: {color} {category}")

    if category not in garment_rules:
        print("No rules found for this garment.")
        return

    possible_matches = garment_rules[category]
    color_matches = color_rules.get(color, [])

    print("\n✨ AURA Outfit Suggestion:")

    for garment in possible_matches:
        if garment == "jeans":
            for c in color_matches:
                print(f"- {c} jeans")
        elif garment in ["shirt", "tshirt"]:
            for c in color_matches:
                print(f"- {c} {garment}")
        elif garment == "jacket":
            for c in color_matches:
                print(f"- {c} jacket")


# 🔽 Example test
recommend_outfit("shirt", "white")
