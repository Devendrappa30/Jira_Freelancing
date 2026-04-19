import os
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-me')

# ── Mail config ────────────────────────────────────────────────────────────
app.config['MAIL_SERVER']   = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT']     = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS']  = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME', '')

mail = Mail(app)
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', 'Devendrappa@outlook.com')

# ── Context processor: inject current year into all templates ──────────────
@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

# ═══════════════════════════════════════════════════════════════════════════
# SITE DATA  — edit everything here; templates auto-update
# ═══════════════════════════════════════════════════════════════════════════

PROFILE = {
    "name":        "Devendrappa",
    "title":       "Jira Implementation Expert & Agile Project Manager",
    "tagline":     "I turn chaotic project trackers into lean, automated Jira machines.",
    "sub_tagline": "Certified ScrumMaster · 10+ Years · Bangalore, India",
    "email":       "Devendrappa@outlook.com",
    "phone":       "+91 9483017604",
    "linkedin":    "https://www.linkedin.com/in/Devendrappa",
    "location":    "Bengaluru, Karnataka, India",
    "availability":"Available for Freelance Projects",
    "response_time":"Replies within 4 hours",
    "certifications": [
        {"name": "Certified ScrumMaster (CSM)", "issuer": "Scrum Alliance", "icon": "🏅"},
        {"name": "Google Project Management",   "issuer": "Coursera / Google", "icon": "🎓"},
        {"name": "Generative AI for PMs",       "issuer": "PMI",              "icon": "🤖"},
    ],
    "stats": [
        {"value": "10+",  "label": "Years Experience"},
        {"value": "50+",  "label": "Projects Delivered"},
        {"value": "95%",  "label": "On-Time Delivery"},
        {"value": "15%",  "label": "Cost Savings Avg"},
    ],
    "tools": [
        "Jira Software", "Jira Service Management", "Confluence",
        "Trello", "Asana", "MS Project",
        "Slack", "Power BI", "Tableau",
    ],
    "methodologies": ["Scrum", "Kanban", "SAFe", "Waterfall", "Hybrid Agile", "XP", "Lean"],
}

SERVICES = [
    {
        "id":    "jira-setup",
        "icon":  "⚙️",
        "title": "Jira Project Setup",
        "price": "From ₹15,000",
        "short": "From scratch to sprint-ready in days — not weeks.",
        "desc":  "I set up Jira Software or Jira Service Management tailored to your team's exact workflow. Boards, issue types, statuses, permissions, components, versions — everything configured correctly the first time.",
        "features": [
            "Scrum or Kanban board configuration",
            "Custom issue types, statuses & transitions",
            "Components, labels, fix versions setup",
            "Permission schemes & notification rules",
            "User roles, groups & access control",
            "Project roadmap & backlog structure",
            "Confluence space linking (if needed)",
        ],
        "delivery": "3–7 business days",
    },
    {
        "id":    "jira-implementation",
        "icon":  "🚀",
        "title": "End-to-End Jira Implementation",
        "price": "From ₹40,000",
        "short": "Full lifecycle delivery — discovery to go-live.",
        "desc":  "A complete, phased Jira implementation following a proven methodology: Requirements → Design → Build → UAT → Go-Live → Handover. Your team gets a Jira that actually fits the way they work.",
        "features": [
            "Requirements gathering & stakeholder interviews",
            "As-Is / To-Be process mapping",
            "Jira architecture design document",
            "Full configuration build (workflows, automations, screens)",
            "Data migration from existing tools",
            "UAT support & sign-off",
            "Team training & recorded walkthroughs",
            "30-day post go-live support",
        ],
        "delivery": "2–6 weeks",
    },
    {
        "id":    "workflow-automation",
        "icon":  "⚡",
        "title": "Workflow & Automation Design",
        "price": "From ₹20,000",
        "short": "Eliminate manual updates. Let Jira work for you.",
        "desc":  "Custom Jira Automation rules that save your team hours every week — auto-transitions, smart assignments, escalation alerts, cross-project triggers, Slack/email notifications, and more.",
        "features": [
            "Automation rule audit of existing setup",
            "Subtask → Parent auto-transition rules",
            "SLA breach alerts & escalation chains",
            "Sprint auto-creation & closure rules",
            "Cross-project syncing & triggers",
            "Slack / email / webhook integrations",
            "Automation performance monitoring",
        ],
        "delivery": "1–2 weeks",
    },
    {
        "id":    "agile-coaching",
        "icon":  "🎯",
        "title": "Agile Coaching & Scrum Setup",
        "price": "From ₹25,000",
        "short": "Build a team that ships. Consistently.",
        "desc":  "I coach your team on Scrum or Kanban practices, help you run effective ceremonies, define a healthy Definition of Done, and set up Jira to reflect real Agile metrics — velocity, burndown, cycle time.",
        "features": [
            "Scrum / Kanban framework selection",
            "Sprint planning & ceremony facilitation",
            "Backlog refinement & story pointing",
            "Definition of Ready / Done creation",
            "Velocity, burndown & CFD setup in Jira",
            "Team retrospective facilitation",
            "Agile maturity assessment & roadmap",
        ],
        "delivery": "Ongoing / 4-week sprints",
    },
    {
        "id":    "dashboards-reporting",
        "icon":  "📊",
        "title": "Dashboards & Leadership Reporting",
        "price": "From ₹12,000",
        "short": "Real-time visibility for teams and executives.",
        "desc":  "Custom Jira dashboards for every stakeholder layer — sprint health for developers, epic progress for product managers, risk/blocker overviews for leadership, and team workload for delivery managers.",
        "features": [
            "Sprint health & burndown dashboard",
            "Leadership delivery overview",
            "Epic & milestone tracking view",
            "Team workload & capacity heatmap",
            "Risk, blocker & dependency boards",
            "Two-dimensional filter statistics",
            "Scheduled email reports (EazyBI / Jira Gadgets)",
        ],
        "delivery": "3–5 business days",
    },
    {
        "id":    "jira-support",
        "icon":  "🛡️",
        "title": "Ongoing Jira Support & AMC",
        "price": "From ₹8,000/month",
        "short": "Your dedicated Jira admin — without the full-time hire.",
        "desc":  "Monthly retainer support: user management, permission fixes, new project setups, automation updates, health checks, and a guaranteed 24-hour response SLA for any Jira issue your team encounters.",
        "features": [
            "Unlimited user management & access requests",
            "24-hour response SLA on all issues",
            "Monthly Jira health check report",
            "New project setups (up to 3/month)",
            "Automation rule updates & fixes",
            "Atlassian version & plugin management",
            "Monthly 1-hour strategy call",
        ],
        "delivery": "Monthly retainer",
    },
]
   PORTFOLIO = [
    {
        "id": 1,
        "client": "Glasscolab (CRM Implementation)",
        "industry": "SaaS / Technology",
        "platform": "Jira Software",
        "title": "Software Simplified Workflow",
        "challenge": "Existing workflow had 9 confusing statuses with dead-end transitions. Developers were unsure which status to use, leading to cluttered boards and poor visibility.",
        "solution": "Designed and implemented a clean 5-status 'Software Simplified' workflow: To Do → In Progress → In-Review → Ready for Demo → Done. Added 'Any' transition rules and automation support.",
        "results": [
            "Reduced from 9 statuses to 5 clean ones",
            "60% faster team onboarding",
            "Eliminated board clutter and confusion",
            "Deployed across the entire Glasscolab project space"
        ],
        "image": "WorkFlow.png",
        "tags": ["Workflow Design", "Scrum", "Simplification"]
    },
    {
        "id": 2,
        "client": "DevTech Solutions",
        "industry": "IT Services",
        "platform": "Jira Software",
        "title": "Subtasks → Story Auto-Transition Automation",
        "challenge": "Developers wasted time manually updating parent Story status every time subtasks were completed (40+ manual updates per sprint).",
        "solution": "Built a smart Jira Automation rule: When ALL subtasks move to 'Done', the parent Story automatically transitions to 'Done'. Rule owned by Devendrappa.",
        "results": [
            "Eliminated 40+ manual updates per sprint",
            "Board accuracy improved to nearly 100%",
            "Rule executes in under 2 seconds",
            "Zero false positives over 3 months"
        ],
        "image": "Automation.png",
        "tags": ["Automation", "Workflow", "Efficiency"]
    },
    {
        "id": 3,
        "client": "DevTech Solutions",
        "industry": "IT Services",
        "platform": "Jira Software",
        "title": "Leadership Delivery Overview Dashboard",
        "challenge": "C-level stakeholders had no real-time visibility. They relied on stale weekly PDF reports.",
        "solution": "Created a live Leadership Dashboard showing active risks, blockers, completed vs upcoming epics, top blockers with owners, and two-dimensional epic statistics.",
        "results": [
            "Real-time risk & blocker tracking",
            "4 out of 4 epics completed on time",
            "Executive reporting time reduced from 3 hours to 0",
            "Full visibility into upcoming pipeline (5 epics)"
        ],
        "image": "Lidershipdashboards.png",
        "tags": ["Dashboards", "Leadership", "Reporting"]
    },
    {
        "id": 4,
        "client": "DevTech Solutions",
        "industry": "IT Services",
        "platform": "Jira Software",
        "title": "Custom Fields & Risk Tracking Schema",
        "challenge": "Risks, compliance, and vendor issues were buried in comments with no structured tracking.",
        "solution": "Designed rich custom field schema including Risk Category, Probability, Impact, Risk Score, Mitigation Plan, Target Date, Risk Owner, and more.",
        "results": [
            "6 powerful custom fields per risk issue",
            "Automated risk score calculation",
            "Risks now fully reportable in dashboards",
            "Integrated into Leadership Delivery Overview"
        ],
        "image": "Custome filedes & grouping.png",
        "tags": ["Custom Fields", "Risk Management", "Governance"]
    },
    {
        "id": 5,
        "client": "DevTech Solutions",
        "industry": "IT Services",
        "platform": "Jira Software",
        "title": "Sprint Overview & Burndown Dashboard",
        "challenge": "Scrum Master had to juggle 4 different tools to track sprint health, workload, burndown, and impediments.",
        "solution": "Built a single comprehensive Sprint Overview dashboard with sprint health, burndown chart, team workload heatmap, impediments tracker, and blockers list.",
        "results": [
            "Sprint closed cleanly with 0 days left",
            "Balanced 4-person team workload visible at a glance",
            "All impediments tracked and resolved",
            "Burndown stayed within guidelines throughout"
        ],
        "image": "SprintDashbaord.png",
        "tags": ["Sprint", "Scrum", "Burndown"]
    },
    {
        "id": 6,
        "client": "Glasscolab",
        "industry": "SaaS / Technology",
        "platform": "Jira Software",
        "title": "End-to-End Project Overview Dashboard",
        "challenge": "126 implementation tasks across 8 epics were tracked in spreadsheets with zero sprint visibility and frequent missed deadlines.",
        "solution": "Built a complete Project Overview dashboard with execution summary, epic progress, active risks, dependencies, blockers, and two-dimensional workload statistics.",
        "results": [
            "126 issues fully tracked across 8 epics",
            "Real-time leadership visibility into risks and blockers",
            "Zero missed sprint goals in final 3 sprints",
            "Full team workload and capacity heatmap"
        ],
        "image": "Project dashboard.png",
        "tags": ["Dashboards", "Project Overview", "Scrum"]
    }
]
PROCESS = [
    {"step": "01", "icon": "💬", "title": "Discovery Call",     "desc": "Free 30-min call to understand your team's structure, tools, pain points, and Jira goals."},
    {"step": "02", "icon": "📋", "title": "Proposal & Scope",   "desc": "Detailed scope, timeline, deliverables, and fixed price — no surprises, no scope creep."},
    {"step": "03", "icon": "🔨", "title": "Build & Configure",  "desc": "I build your Jira setup iteratively with regular check-ins, sharing progress at every milestone."},
    {"step": "04", "icon": "✅", "title": "UAT & Handover",     "desc": "You test everything. I document everything. Training sessions + recordings included in every engagement."},
    {"step": "05", "icon": "🛡️", "title": "Post-Launch Support","desc": "30 days of free support after go-live on all implementation projects. Ongoing AMC plans available."},
]

TESTIMONIALS = [
    {
        "name":    "Priya R.",
        "role":    "CTO, SaaS Startup — Bengaluru",
        "text":    "Devendrappa set up our entire Jira in 5 days — workflows, automations, dashboards, everything. Our sprint velocity improved 30% in the first month because the team finally had proper structure.",
        "rating":  5,
    },
    {
        "name":    "Arjun M.",
        "role":    "Engineering Manager, IT Services",
        "text":    "The automation rules he built saved my team 3+ hours every week. The Subtask → Story auto-transition alone eliminated our biggest source of board noise. Worth every rupee.",
        "rating":  5,
    },
    {
        "name":    "Sneha K.",
        "role":    "Product Manager, E-commerce",
        "text":    "We went from zero Jira knowledge to running smooth Scrum sprints in 3 weeks. Devendrappa trained the entire team and even stayed on for a month to keep us on track. Highly recommend.",
        "rating":  5,
    },
]

FAQS = [
    {"q": "Do you work with Jira Cloud or Jira Server/Data Center?",
     "a": "Primarily Jira Cloud (which most teams use). I also have experience with Jira Server and Data Center configurations. Please mention your version when you reach out."},
    {"q": "How long does a typical Jira setup take?",
     "a": "A basic project setup is 3–7 days. Full end-to-end implementations range from 2–6 weeks depending on team size, number of projects, integrations, and data migration needs."},
    {"q": "Do you offer training for the team?",
     "a": "Yes — every implementation includes team training sessions and recorded walkthroughs so your team is self-sufficient from day one. Admin training is also available separately."},
    {"q": "Can you migrate from Trello / Asana / spreadsheets to Jira?",
     "a": "Yes. I handle data migration from Trello, Asana, Monday, and Excel/Google Sheets. I'll clean up your data and map it to the correct Jira structure before import."},
    {"q": "Do you work with non-technical teams?",
     "a": "Absolutely. Many of my clients are marketing, operations, HR, and finance teams. I tailor the Jira setup and training to match your team's technical comfort level."},
    {"q": "What's included in the monthly support retainer?",
     "a": "Unlimited user management, new project setups (up to 3/month), automation fixes, health checks, and a monthly strategy call — all with a 24-hour response SLA."},
]

# ═══════════════════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return render_template("index.html",
        profile=PROFILE, services=SERVICES[:3],
        portfolio=PORTFOLIO[:3], testimonials=TESTIMONIALS,
        process=PROCESS)

@app.route("/services")
def services():
    return render_template("services.html", profile=PROFILE, services=SERVICES, process=PROCESS)

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html", profile=PROFILE, portfolio=PORTFOLIO)

@app.route("/about")
def about():
    return render_template("about.html", profile=PROFILE, testimonials=TESTIMONIALS, faqs=FAQS)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name    = request.form.get("name", "").strip()
        email   = request.form.get("email", "").strip()
        phone   = request.form.get("phone", "").strip()
        service = request.form.get("service", "General Inquiry")
        budget  = request.form.get("budget", "")
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please fill all required fields.", "error")
            return redirect(url_for("contact"))

        try:
            msg = Message(
                subject=f"[JiraFreelancer] New enquiry from {name} — {service}",
                recipients=[CONTACT_EMAIL],
                body=f"""New project enquiry received:

Name    : {name}
Email   : {email}
Phone   : {phone or 'Not provided'}
Service : {service}
Budget  : {budget or 'Not specified'}

Message:
{message}

---
Sent via devendrappa.in contact form
""")
            mail.send(msg)

            # Auto-reply
            auto = Message(
                subject="Got your message — Devendrappa | Jira Expert",
                recipients=[email],
                body=f"""Hi {name},

Thanks for reaching out! I've received your enquiry about "{service}" and will reply within 4 hours (usually faster during business hours).

What happens next:
→ I'll review your requirements
→ We'll schedule a free 30-min discovery call
→ You'll get a detailed proposal within 24 hours

Feel free to connect on LinkedIn: https://www.linkedin.com/in/Devendrappa

Best,
Devendrappa
Certified ScrumMaster | Jira Implementation Expert
📧 Devendrappa@outlook.com
📞 +91 9483017604
""")
            mail.send(auto)
            flash("Message sent! I'll reply within 4 hours.", "success")

        except Exception as e:
            app.logger.error(f"Mail error: {e}")
            flash("Message received! I'll be in touch soon.", "success")

        return redirect(url_for("contact"))

    return render_template("contact.html", profile=PROFILE, services=SERVICES)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", profile=PROFILE), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("404.html", profile=PROFILE), 500

if __name__ == "__main__":
    debug = os.environ.get("FLASK_ENV") != "production"
    app.run(debug=debug, port=5000)
