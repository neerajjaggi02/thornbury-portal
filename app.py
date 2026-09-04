import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, date

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Thornbury Growth Command Centre",
    layout="wide",
    page_icon="🏢",
    initial_sidebar_state="expanded"
)

# ============================================================
# GOOGLE SHEETS CONNECTION
# ============================================================

conn = st.connection("gsheets", type=GSheetsConnection)

# ============================================================
# CONFIGURATION
# ============================================================

SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_GOOGLE_SHEET_ID/edit"

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def read_sheet(worksheet, columns=None):
    """Read a worksheet safely."""
    try:
        df = conn.read(
            spreadsheet=SHEET_URL,
            worksheet=worksheet,
            ttl=0
        )

        if df is None:
            df = pd.DataFrame()

        df = df.dropna(how="all")

        if columns:
            for col in columns:
                if col not in df.columns:
                    df[col] = ""

            df = df[columns]

        return df

    except Exception as e:
        st.warning(f"Could not load '{worksheet}': {e}")
        return pd.DataFrame(columns=columns or [])


def append_to_sheet(worksheet, new_row, columns):
    """Append one row to a Google Sheet worksheet."""
    try:
        existing = read_sheet(worksheet, columns)

        new_df = pd.DataFrame([new_row], columns=columns)

        updated = pd.concat(
            [existing, new_df],
            ignore_index=True
        )

        conn.update(
            spreadsheet=SHEET_URL,
            worksheet=worksheet,
            data=updated
        )

        return True

    except Exception as e:
        st.error(f"Could not save data: {e}")
        return False


def update_sheet(worksheet, df):
    """Replace worksheet contents."""
    try:
        conn.update(
            spreadsheet=SHEET_URL,
            worksheet=worksheet,
            data=df
        )
        return True

    except Exception as e:
        st.error(f"Could not update sheet: {e}")
        return False


def metric_card(label, value, delta=None):
    st.metric(
        label=label,
        value=value,
        delta=delta
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🏢 Thornbury")

    st.caption("Growth Command Centre")

    st.divider()

    st.markdown("### Navigation")

    view_mode = st.radio(
        "View",
        ["Client View", "Marketing Manager"],
        index=0
    )

    st.divider()

    st.markdown("### Project Focus")

    st.success("🍽️ Weekday Restaurant Growth")
    st.info("💼 Corporate Theatre Sales")
    st.warning("🌐 Website Conversion")
    st.success("📧 CRM & Repeat Business")

    st.divider()

    st.caption(
        "Thornbury Taphouse + Thornbury Theatre"
    )

# ============================================================
# HEADER
# ============================================================

st.title("THORNBURY GROWTH COMMAND CENTRE")

st.markdown(
    """
    **Digital marketing, website, restaurant growth, theatre sales,
    content and KPI management in one place.**
    """
)

st.divider()

# ============================================================
# TABS
# ============================================================

tabs = st.tabs([
    "🏠 Dashboard",
    "📋 Discovery",
    "🌐 Website",
    "🍽️ Restaurant Growth",
    "💼 Corporate B2B",
    "🎬 Content Studio",
    "📧 CRM & Loyalty",
    "📊 Analytics",
    "🗓️ 90-Day Roadmap"
])

# ============================================================
# 1. DASHBOARD
# ============================================================

with tabs[0]:

    st.header("Business Performance")

    # Demo / baseline values
    # Replace with Google Sheets data when historical data is available.

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Monday–Thursday Revenue",
            "$8,420",
            "+12%"
        )

    with c2:
        metric_card(
            "Weekday Covers",
            "126",
            "+18%"
        )

    with c3:
        metric_card(
            "Corporate Leads",
            "18",
            "+6"
        )

    with c4:
        metric_card(
            "Corporate Bookings",
            "3",
            "+1"
        )

    st.divider()

    # --------------------------------------------------------
    # RESTAURANT
    # --------------------------------------------------------

    st.subheader("🍽️ Restaurant — Monday to Thursday")

    r1, r2, r3, r4 = st.columns(4)

    with r1:
        metric_card("Monday Covers", "34")

    with r2:
        metric_card("Tuesday Covers", "22")

    with r3:
        metric_card("Wednesday Covers", "31")

    with r4:
        metric_card("Thursday Covers", "55")

    st.info(
        "🎯 Primary restaurant objective: increase Monday–Thursday "
        "covers without relying on heavy discounting."
    )

    # --------------------------------------------------------
    # THEATRE
    # --------------------------------------------------------

    st.subheader("💼 Theatre — Corporate Pipeline")

    t1, t2, t3, t4, t5 = st.columns(5)

    with t1:
        metric_card("Prospects", "47")

    with t2:
        metric_card("Contacted", "31")

    with t3:
        metric_card("Replies", "9")

    with t4:
        metric_card("Qualified", "6")

    with t5:
        metric_card("Booked", "2")

    st.divider()

    # --------------------------------------------------------
    # CURRENT PROJECT STATUS
    # --------------------------------------------------------

    st.subheader("🚀 Current Project Status")

    p1, p2 = st.columns(2)

    with p1:

        st.markdown("### Website")

        st.progress(
            0.78,
            text="78% — Conversion architecture"
        )

        st.markdown("""
        - ✅ Discovery
        - ✅ Website audit
        - ✅ Wireframes
        - 🔄 Corporate landing page
        - ⬜ Final design
        - ⬜ Launch
        """)

    with p2:

        st.markdown("### Marketing")

        st.progress(
            0.55,
            text="55% — Acquisition setup"
        )

        st.markdown("""
        - ✅ Content strategy
        - ✅ Weekday campaign concept
        - 🔄 Corporate outreach
        - 🔄 Google/Meta setup
        - ⬜ CRM automation
        """)

# ============================================================
# 2. DISCOVERY
# ============================================================

with tabs[1]:

    st.header("📋 Client Discovery Questionnaire")

    st.markdown(
        "Complete this with the business owner. "
        "Marketing research should be completed separately by you."
    )

    discovery_columns = [
        "Timestamp",
        "Taphouse 3 Words",
        "Theatre 3 Words",
        "Target Audience",
        "Cloud Kitchen Items",
        "A/V Tech",
        "Assets Link",
        "Monthly Revenue Target",
        "Weekday Cover Target",
        "Corporate Priority",
        "Notes"
    ]

    with st.form("discovery_form"):

        st.subheader("Brand Identity")

        taphouse_words = st.text_input(
            "What 3 words define Thornbury Taphouse?"
        )

        theatre_words = st.text_input(
            "What 3 words define Thornbury Theatre?"
        )

        st.subheader("Restaurant Growth")

        target_audience = st.multiselect(
            "Primary target for Monday–Wednesday dinners?",
            [
                "Locals / Neighbours",
                "Office Workers",
                "Students",
                "Couples",
                "Families",
                "Groups",
                "Hospo / Industry Staff"
            ]
        )

        weekday_target = st.number_input(
            "Ideal average weekday covers",
            min_value=0,
            step=5
        )

        monthly_target = st.number_input(
            "Desired monthly revenue target ($AUD)",
            min_value=0,
            step=1000
        )

        st.subheader("Theatre / Corporate")

        corporate_priority = st.multiselect(
            "Which corporate events are priorities?",
            [
                "Product Launch",
                "Conference",
                "Awards Night",
                "EOFY Event",
                "Christmas Party",
                "Team Event",
                "Networking",
                "Client Entertainment",
                "Brand Activation",
                "Private Performance"
            ]
        )

        av_tech = st.radio(
            "A/V technician available?",
            [
                "Yes — in-house",
                "Yes — on request",
                "No"
            ]
        )

        st.subheader("Cloud Kitchen")

        kitchen_items = st.text_area(
            "Potential high-margin cloud kitchen / takeaway items"
        )

        assets_link = st.text_input(
            "Link to high-resolution photos, logos and videos"
        )

        notes = st.text_area(
            "Additional notes"
        )

        submitted = st.form_submit_button(
            "💾 Save Discovery"
        )

        if submitted:

            row = {
                "Timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "Taphouse 3 Words": taphouse_words,
                "Theatre 3 Words": theatre_words,
                "Target Audience": ", ".join(target_audience),
                "Cloud Kitchen Items": kitchen_items,
                "A/V Tech": av_tech,
                "Assets Link": assets_link,
                "Monthly Revenue Target": monthly_target,
                "Weekday Cover Target": weekday_target,
                "Corporate Priority": ", ".join(corporate_priority),
                "Notes": notes
            }

            if append_to_sheet(
                "Discovery",
                row,
                discovery_columns
            ):
                st.success(
                    "✅ Discovery responses saved."
                )

# ============================================================
# 3. WEBSITE
# ============================================================

with tabs[2]:

    st.header("🌐 Website Revamp Tracker")

    st.markdown(
        "Track the website transformation from discovery to launch."
    )

    website_tasks = [
        ("Discovery & Requirements", True),
        ("Website UX Audit", True),
        ("Competitor Research", False),
        ("Information Architecture", True),
        ("Restaurant Wireframes", False),
        ("Corporate Events Landing Page", False),
        ("Mobile-First Design", False),
        ("SEO Structure", False),
        ("OpenTable Integration", False),
        ("Analytics & Conversion Tracking", False),
        ("Final QA", False),
        ("Website Launch", False),
    ]

    completed = 0

    for task, default in website_tasks:

        value = st.checkbox(
            task,
            value=default,
            key=f"website_{task}"
        )

        if value:
            completed += 1

    progress = completed / len(website_tasks)

    st.progress(
        progress,
        text=f"{completed}/{len(website_tasks)} completed"
    )

    st.divider()

    st.subheader("Recommended Theatre Website Structure")

    st.code("""
HOME
├── What's On
├── Corporate Events
├── Private Events
├── Venue Hire
├── Food & Dining
├── Gallery
├── About
└── Contact
""")

    st.subheader("Recommended Taphouse Website Structure")

    st.code("""
HOME
├── Menu
├── Book a Table
├── What's On
├── Group Bookings
├── Corporate Dining
├── Dinner + Show
├── Gallery
└── Contact
""")

# ============================================================
# 4. RESTAURANT GROWTH
# ============================================================

with tabs[3]:

    st.header("🍽️ Restaurant Weekday Growth")

    st.markdown(
        "Build repeatable reasons for customers to visit Monday–Thursday."
    )

    # --------------------------------------------------------
    # DAY CARDS
    # --------------------------------------------------------

    days = [
        ("Monday", "Smokehouse Monday"),
        ("Tuesday", "Tap Tuesday / Super Tuesday"),
        ("Wednesday", "Taphouse Social"),
        ("Thursday", "Dinner + Show")
    ]

    for day, campaign in days:

        with st.expander(
            f"{day} — {campaign}",
            expanded=(day == "Tuesday")
        ):

            col1, col2, col3 = st.columns(3)

            with col1:

                covers = st.number_input(
                    f"{day} covers",
                    min_value=0,
                    step=1,
                    key=f"{day}_covers"
                )

            with col2:

                revenue = st.number_input(
                    f"{day} revenue ($)",
                    min_value=0,
                    step=100,
                    key=f"{day}_revenue"
                )

            with col3:

                target = st.number_input(
                    f"{day} target covers",
                    min_value=0,
                    step=5,
                    key=f"{day}_target"
                )

            if target > 0:

                achievement = min(
                    covers / target,
                    1
                )

                st.progress(
                    achievement,
                    text=f"{covers}/{target} covers"
                )

    st.divider()

    # --------------------------------------------------------
    # SUPER TUESDAY
    # --------------------------------------------------------

    st.subheader("🔥 Super Tuesday Activation")

    activation = st.selectbox(
        "Current Tuesday activation",
        [
            "Tap Tuesday",
            "Local Hospo Night",
            "Secret Menu",
            "Trivia Night",
            "Live Music",
            "Other"
        ]
    )

    st.text_area(
        "Tuesday offer / campaign description",
        placeholder=(
            "Example: rotating taps + Tuesday-only "
            "food special."
        )
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Tuesday Covers", "22")

    with c2:
        metric_card("Target", "50")

    with c3:
        metric_card("Average Spend", "$54")

    with c4:
        metric_card("Repeat Tuesday Customers", "—")

    st.info(
        "Recommendation: test one strong Tuesday proposition "
        "for 4–6 weeks and compare incremental covers, revenue, "
        "average spend and repeat visits."
    )

# ============================================================
# 5. CORPORATE B2B
# ============================================================

with tabs[4]:

    st.header("💼 Corporate Theatre B2B")

    st.markdown(
        "Generate Monday–Thursday corporate and private-event demand."
    )

    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    st.subheader("Corporate Pipeline")

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    pipeline_metrics = [
        ("Prospects", "47"),
        ("Contacted", "31"),
        ("Replies", "9"),
        ("Qualified", "6"),
        ("Quotes", "4"),
        ("Booked", "2")
    ]

    for col, (label, value) in zip(
        [c1, c2, c3, c4, c5, c6],
        pipeline_metrics
    ):
        with col:
            metric_card(label, value)

    st.divider()

    # --------------------------------------------------------
    # ADD LEAD
    # --------------------------------------------------------

    st.subheader("➕ Add Corporate Lead")

    lead_columns = [
        "Timestamp",
        "Company",
        "Contact",
        "Job Title",
        "LinkedIn",
        "Email",
        "Event Type",
        "Guests",
        "Budget",
        "Status",
        "Last Contact",
        "Next Follow-up",
        "Notes"
    ]

    with st.form("corporate_lead_form"):

        col1, col2 = st.columns(2)

        with col1:

            company = st.text_input("Company")

            contact = st.text_input("Contact Person")

            job_title = st.text_input("Job Title")

            linkedin = st.text_input(
                "LinkedIn Profile"
            )

            email = st.text_input("Email")

        with col2:

            event_type = st.selectbox(
                "Event Type",
                [
                    "Product Launch",
                    "Conference",
                    "Awards Night",
                    "EOFY",
                    "Christmas Party",
                    "Team Event",
                    "Networking",
                    "Client Entertainment",
                    "Brand Activation",
                    "Private Event",
                    "Other"
                ]
            )

            guests = st.number_input(
                "Estimated Guests",
                min_value=0,
                step=10
            )

            budget = st.number_input(
                "Estimated Budget ($AUD)",
                min_value=0,
                step=500
            )

            status = st.selectbox(
                "Pipeline Status",
                [
                    "Prospect",
                    "Contacted",
                    "Replied",
                    "Qualified",
                    "Quote Sent",
                    "Negotiation",
                    "Booked",
                    "Lost"
                ]
            )

        notes = st.text_area("Notes")

        lead_submit = st.form_submit_button(
            "Save Corporate Lead"
        )

        if lead_submit and company:

            row = {
                "Timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "Company": company,
                "Contact": contact,
                "Job Title": job_title,
                "LinkedIn": linkedin,
                "Email": email,
                "Event Type": event_type,
                "Guests": guests,
                "Budget": budget,
                "Status": status,
                "Last Contact": "",
                "Next Follow-up": "",
                "Notes": notes
            }

            if append_to_sheet(
                "Corporate_Leads",
                row,
                lead_columns
            ):
                st.success(
                    "✅ Corporate lead saved."
                )

    st.divider()

    # --------------------------------------------------------
    # LINKEDIN OUTBOUND
    # --------------------------------------------------------

    st.subheader("🔗 Organic LinkedIn Outreach")

    l1, l2, l3, l4, l5 = st.columns(5)

    with l1:
        metric_card("Prospects Researched", "18")

    with l2:
        metric_card("Connections Sent", "15")

    with l3:
        metric_card("Accepted", "8")

    with l4:
        metric_card("Replies", "4")

    with l5:
        metric_card("Qualified", "2")

    st.markdown("""
    **Target profiles**

    - HR Managers
    - People & Culture
    - Executive Assistants
    - Office Managers
    - Marketing Managers
    - Event Managers
    - Event Agencies
    - Conference Organisers
    """)

# ============================================================
# 6. CONTENT STUDIO
# ============================================================

with tabs[5]:

    st.header("🎬 Content Studio")

    st.markdown(
        "Plan, approve and track Instagram/Facebook/TikTok content."
    )

    content_columns = [
        "Timestamp",
        "Brand",
        "Content Type",
        "Title",
        "Hook",
        "Platform",
        "Status",
        "Publish Date",
        "Client Notes"
    ]

    # --------------------------------------------------------
    # ADD CONTENT IDEA
    # --------------------------------------------------------

    with st.form("content_form"):

        brand = st.selectbox(
            "Brand",
            [
                "Thornbury Taphouse",
                "Thornbury Theatre",
                "Both"
            ]
        )

        content_type = st.selectbox(
            "Content Type",
            [
                "Reel",
                "Carousel",
                "Photo",
                "Story",
                "Corporate",
                "UGC",
                "Behind the Scenes"
            ]
        )

        title = st.text_input(
            "Content Title"
        )

        hook = st.text_area(
            "Hook / First 3 Seconds"
        )

        platform = st.multiselect(
            "Platform",
            [
                "Instagram",
                "Facebook",
                "TikTok",
                "LinkedIn"
            ]
        )

        status = st.selectbox(
            "Status",
            [
                "Idea",
                "Draft",
                "In Review",
                "Changes Requested",
                "Approved",
                "Scheduled",
                "Published"
            ]
        )

        publish_date = st.date_input(
            "Publish Date",
            value=date.today()
        )

        client_notes = st.text_area(
            "Client Notes"
        )

        content_submit = st.form_submit_button(
            "💾 Save Content"
        )

        if content_submit and title:

            row = {
                "Timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "Brand": brand,
                "Content Type": content_type,
                "Title": title,
                "Hook": hook,
                "Platform": ", ".join(platform),
                "Status": status,
                "Publish Date": str(publish_date),
                "Client Notes": client_notes
            }

            if append_to_sheet(
                "Content",
                row,
                content_columns
            ):
                st.success(
                    "✅ Content idea saved."
                )

    st.divider()

    # --------------------------------------------------------
    # CURRENT CONTENT
    # --------------------------------------------------------

    content_df = read_sheet(
        "Content",
        content_columns
    )

    if not content_df.empty:

        st.subheader("Current Content Pipeline")

        st.dataframe(
            content_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No content has been added yet."
        )

# ============================================================
# 7. CRM & LOYALTY
# ============================================================

with tabs[6]:

    st.header("📧 CRM & Loyalty")

    st.markdown(
        "Build a first-party customer database and increase repeat visits."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Customer Database", "—")

    with c2:
        metric_card("New Subscribers", "—")

    with c3:
        metric_card("Email Open Rate", "—")

    with c4:
        metric_card("Bookings from Email", "—")

    st.divider()

    st.subheader("Thornbury Insider")

    st.markdown("""
    **Potential member benefits**

    - Early access to shows
    - Special weekday offers
    - Birthday reward
    - Exclusive events
    - Member-only experiences
    - Ticket presales
    """)

    st.info(
        "Use the existing customer database where legally permitted "
        "and ensure marketing communications have appropriate consent."
    )

    st.subheader("Suggested CRM Segments")

    segments = st.multiselect(
        "Active CRM segments",
        [
            "Restaurant Customers",
            "Theatre Customers",
            "Restaurant + Theatre Customers",
            "Corporate Leads",
            "VIP / Repeat Customers"
        ],
        default=[
            "Restaurant Customers",
            "Theatre Customers"
        ]
    )

    st.write(
        f"Selected segments: {', '.join(segments)}"
    )

# ============================================================
# 8. ANALYTICS
# ============================================================

with tabs[7]:

    st.header("📊 Marketing Performance Dashboard")

    st.caption(
        "Use this area for validated business data. "
        "Demo values below should be replaced with connected data."
    )

    # --------------------------------------------------------
    # RESTAURANT
    # --------------------------------------------------------

    st.subheader("🍽️ Restaurant KPIs")

    restaurant_data = pd.DataFrame({
        "Day": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday"
        ],
        "Covers": [
            34,
            22,
            31,
            55
        ],
        "Target": [
            50,
            50,
            50,
            70
        ],
        "Revenue": [
            1800,
            1400,
            1700,
            3520
        ]
    })

    st.dataframe(
        restaurant_data,
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        restaurant_data.set_index("Day")[
            ["Covers", "Target"]
        ]
    )

    st.divider()

    # --------------------------------------------------------
    # THEATRE
    # --------------------------------------------------------

    st.subheader("💼 Theatre KPIs")

    theatre_data = pd.DataFrame({
        "Metric": [
            "Corporate Enquiries",
            "Qualified Leads",
            "Quotes",
            "Bookings"
        ],
        "Current": [
            18,
            6,
            4,
            2
        ]
    })

    st.dataframe(
        theatre_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # MARKETING
    # --------------------------------------------------------

    st.subheader("📈 Marketing KPIs")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        metric_card("Website Visitors", "—")

    with m2:
        metric_card("Booking Conversion", "—")

    with m3:
        metric_card("Cost per Lead", "—")

    with m4:
        metric_card("ROAS", "—")

# ============================================================
# 9. 90-DAY ROADMAP
# ============================================================

with tabs[8]:

    st.header("🗓️ 90-Day Growth Sprint")

    st.markdown(
        "Track the project week by week."
    )

    phases = {

        "Phase 1 — Foundation | Weeks 1–4": [
            "Week 1 — Client discovery + collect brand assets",
            "Week 2 — Website, Google, booking and competitor audit",
            "Week 3 — Website wireframes + corporate landing page",
            "Week 4 — Analytics + conversion tracking + content strategy"
        ],

        "Phase 2 — Launch | Weeks 5–8": [
            "Week 5 — Website launch + Monday–Wednesday campaign",
            "Week 6 — Corporate B2B launch + LinkedIn outreach",
            "Week 7 — Dinner + Show cross-selling",
            "Week 8 — Short-form content + Google/Meta campaigns"
        ],

        "Phase 3 — Optimise | Weeks 9–12": [
            "Week 9 — Review CPL + booking conversion",
            "Week 10 — Evaluate cloud kitchen readiness",
            "Week 11 — Launch Thornbury Insider email programme",
            "Week 12 — 90-day KPI review + next-quarter plan"
        ]
    }

    total_tasks = sum(
        len(tasks)
        for tasks in phases.values()
    )

    completed_tasks = 0

    for phase, tasks in phases.items():

        st.subheader(phase)

        for task in tasks:

            done = st.checkbox(
                task,
                key=f"roadmap_{task}"
            )

            if done:
                completed_tasks += 1

    progress = (
        completed_tasks / total_tasks
        if total_tasks > 0
        else 0
    )

    st.divider()

    st.progress(
        progress,
        text=(
            f"{completed_tasks}/{total_tasks} milestones "
            f"completed — {progress:.0%}"
        )
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Thornbury Growth Command Centre • "
    "Restaurant + Theatre + Corporate Growth"
)
