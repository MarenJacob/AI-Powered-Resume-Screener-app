def generate_recommendation(score):

    try:
        score = float(score)

    except:
        score = 0

    if score >= 80:

        return {
            "decision": "Hire",
            "reason": "Strong candidate with excellent role compatibility."
        }

    elif score >= 55:

        return {
            "decision": "Consider",
            "reason": "Moderate compatibility. Further evaluation recommended."
        }

    else:

        return {
            "decision": "Reject",
            "reason": "Low compatibility for this role."
        }