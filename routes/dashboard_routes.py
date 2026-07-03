resumes = Resume.query.all()
users = User.query.all()

total_candidates = len(resumes)

average_score = 0

if resumes:
    average_score = round(
        sum(r.ai_score or 0 for r in resumes) / len(resumes),
        1
    )

fraud_alerts = len([
    r for r in resumes
    if (r.ai_generated_probability or 0) > 70
])
return render_template(
    "dashboard/dashboard.html",
    resumes=resumes,
    users=users,
    analytics=analytics,
    total_candidates=total_candidates,
    average_score=average_score,
    fraud_alerts=fraud_alerts
)