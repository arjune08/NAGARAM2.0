"""NAGARAM 2.0 public experience and assistant API."""
from flask import Blueprint, jsonify, render_template, request

from app.extensions import db

main_bp = Blueprint("main", __name__)


def _platform_snapshot():
    """Read live platform numbers without making the landing page depend on seed data."""
    try:
        from models.issue import Issue
        total = Issue.query.count()
        resolved = Issue.query.filter(Issue.status.in_(["Resolved", "Closed", "Completed"])).count()
        civic = Issue.query.filter_by(issue_type="civic").count()
        agricultural = Issue.query.filter_by(issue_type="agricultural").count()
        return {"total": total, "resolved": resolved, "civic": civic, "agricultural": agricultural}
    except Exception:
        db.session.rollback()
        return {"total": 0, "resolved": 0, "civic": 0, "agricultural": 0}


@main_bp.route("/")
def landing():
    return render_template("main/landing.html", stats=_platform_snapshot())


@main_bp.route("/about")
def about():
    return render_template("main/about.html")


@main_bp.post("/api/chat")
def chat():
    """Zero-key assistant backed by live NAGARAM database context."""
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip().lower()
    stats = _platform_snapshot()

    if not message:
        answer = "Hi! I can help with civic complaints, agriculture support, schemes, and NAGARAM status."
    elif any(word in message for word in ("report", "complaint", "pothole", "garbage", "street light", "water")):
        answer = "Use the Citizen portal to report a civic issue. Add the location, category, description and a photo when possible."
    elif any(word in message for word in ("farmer", "crop", "pest", "soil", "irrigation", "agriculture")):
        answer = "Use the Farmer portal for crop guidance, soil and water advice, market information, schemes and expert consultations."
    elif any(word in message for word in ("status", "resolved", "how many", "issues")):
        answer = f"The connected database currently has {stats['total']} cases: {stats['resolved']} resolved, {stats['civic']} civic and {stats['agricultural']} agricultural."
    elif any(word in message for word in ("scheme", "subsidy", "government")):
        answer = "Open the Farmer portal to explore government-scheme information and eligibility guidance."
    else:
        answer = "I can help with civic complaints, agriculture, schemes, issue status, and choosing the right NAGARAM portal. Try: How do I report a pothole?"

    return jsonify({"answer": answer, "stats": stats})
