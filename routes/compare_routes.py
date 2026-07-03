from flask import Blueprint
from flask import request
from flask import jsonify

from services.comparison_service import compare_candidates

# ==========================================
# BLUEPRINT
# ==========================================

compare_bp = Blueprint(

    "compare",

    __name__
)

# ==========================================
# COMPARE CANDIDATES
# ==========================================

@compare_bp.route("/compare", methods=["POST"])
def compare_candidates_route():

    data = request.json

    candidates = data.get(

        "candidates",

        []
    )

    results = compare_candidates(

        candidates
    )

    return jsonify(results)