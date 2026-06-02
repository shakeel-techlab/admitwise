
from datetime import datetime
from data.universities import UNIVERSITIES


def calculate_merit(matric_obtained, matric_total, fsc_obtained, fsc_total, net_score, criteria):
    matric_pct = (matric_obtained / matric_total) * 100
    fsc_pct = (fsc_obtained / fsc_total) * 100
    net_pct = net_score

    matric_w = criteria.get("matric_weight", 10)
    fsc_w = criteria.get("fsc_weight", 50)
    net_w = criteria.get("net_weight", 40)

    total_weight = matric_w + fsc_w + net_w
    if total_weight == 0:
        return 0

    merit = (matric_pct * matric_w + fsc_pct * fsc_w + net_pct * net_w) / total_weight
    return round(merit, 2)


def get_admission_probability(merit_score, fsc_percent, net_score, criteria, field):
    min_net = criteria.get("min_net", 0)
    min_fsc = 50

    if fsc_percent < min_fsc:
        return "Very Low", 0
    if min_net > 0 and net_score < min_net:
        return "Very Low", 0

    if merit_score >= 80:
        return "High", merit_score
    elif merit_score >= 65:
        return "Medium", merit_score
    elif merit_score >= 50:
        return "Low", merit_score
    else:
        return "Very Low", merit_score


def predict(matric_obtained, matric_total, fsc_obtained, fsc_total, net_score, field, city=None):
    fsc_percent = (fsc_obtained / fsc_total) * 100
    results = []

    for uni in UNIVERSITIES:
        if field not in uni["fields"]:
            continue

        criteria = uni["merit_criteria"].get(field)
        if not criteria:
            continue

        merit = calculate_merit(
            matric_obtained, matric_total,
            fsc_obtained, fsc_total,
            net_score, criteria
        )

        probability, score = get_admission_probability(merit, fsc_percent, net_score, criteria, field)

        # Calculate distance score for location relevance
        distance_score = None
        if city and uni.get("city") and city != "Select City":
            if uni["city"].lower() == city.lower() or uni["city"] == "Multiple Campuses":
                distance_score = "Nearby"
            else:
                distance_score = "Far"

        # Days until deadline
        try:
            deadline_date = datetime.strptime(uni["deadline"], "%Y-%m-%d")
            days_left = (deadline_date - datetime.now()).days
        except Exception:
            days_left = None

        results.append({
            "university": uni,
            "merit_score": merit,
            "probability": probability,
            "distance": distance_score,
            "days_left": days_left,
            "field": field,
        })

    # Sort by merit score descending
    results.sort(key=lambda x: x["merit_score"], reverse=True)
    return results


def get_merit_gap(merit_score, probability):
    if probability == "High":
        return None
    elif probability == "Medium":
        gap = 80 - merit_score
        return f"+{gap:.1f} merit points needed for High chance"
    elif probability == "Low":
        gap = 65 - merit_score
        return f"+{gap:.1f} merit points needed for Medium chance"
    else:
        gap = 50 - merit_score
        return f"+{gap:.1f} merit points needed for Low chance"
