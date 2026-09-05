import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, date
import time

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

SHEET_URL = "https://docs.google.com/spreadsheets/d/1-2HTr0mOkl_Tis-ehO4apu8kqw4KSKPte_nq_ngTm5E/edit?gid=0#gid=0"

# ============================================================
# HELPER FUNCTIONS
# ============================================================

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def read_sheet(worksheet, columns=None):
    """Read a worksheet safely with instant sync capability."""
    try:
        # We keep ttl=600 for performance, but if data was deleted in the sheet,
        # clearing the cache or reloading the page pulls the fresh state instantly.
        df = conn.read(
            spreadsheet=SHEET_URL,
            worksheet=worksheet,
            ttl=600
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
        error_str = str(e)
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "Quota exceeded" in error_str:
            st.error(
                "🚨 **Google Sheets API Rate Limit Reached (Error 429)**\n\n"
                "You are clicking too fast or refreshing too many tabs simultaneously. "
                "Google allows a maximum of 60 read requests per minute.\n\n"
                "⏳ *Please wait 60 seconds before trying again.*"
            )
            if st.button("🧹 Clear App Cache & Reset", key=f"cache_reset_{worksheet}"):
                st.cache_data.clear()
                st.rerun()
        else:
            st.error(
                f"Could not load worksheet '{worksheet}'. "
                f"Please make sure the tab exists in Google Sheets. "
                f"Error: {e}"
            )
        return pd.DataFrame(columns=columns or [])


def append_to_sheet(worksheet, new_row, columns):
    """Append one row to a Google Sheet worksheet with error handling."""
    try:
        existing = read_sheet(worksheet, columns)
        new_df = pd.DataFrame([new_row], columns=columns)
        updated = pd.concat([existing, new_df], ignore_index=True)

        conn.update(
            spreadsheet=SHEET_URL,
            worksheet=worksheet,
            data=updated
        )
        
        st.cache_data.clear()
        return True

    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "Quota exceeded" in error_str:
            st.error(
                "🚨 **Google Sheets API Rate Limit Reached (Error 429)**\n\n"
                "Your save request was blocked because Google's write quota was temporarily exceeded. Please wait a minute and try saving again."
            )
        else:
            st.error(f"Could not save data: {e}")
        return False


def update_sheet(worksheet, df):
    """Replace worksheet contents with error handling."""
    try:
        conn.update(
            spreadsheet=SHEET_URL,
            worksheet=worksheet,
            data=df
        )
        
        st.cache_data.clear()
        return True

    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "Quota exceeded" in error_str:
            st.error(
                "🚨 **Google Sheets API Rate Limit Reached (Error 429)**\n\n"
                "Your update request was blocked because Google's write quota was temporarily exceeded. Please wait a minute and try again."
            )
        else:
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
st.divider()
    
    # Global Sync / Refresh Button for Real-Time Google Sheets Deletions
    if st.button("🔄 Sync with Google Sheets"):
        st.cache_data.clear()
        st.success("Cache cleared! Pulling latest data...")
        time.sleep(0.8)
        st.rerun()
    st.title("🏢 Thornbury")
    st.caption("Growth Command Centre")
    st.divider()

    st.markdown("### Project Focus")
    st.success("🍽️ Weekday Restaurant Growth")
    st.info("💼 Corporate Theatre Sales")
    st.warning("🌐 Website Conversion")
    st.success("📧 CRM & Repeat Business")

    st.divider()
    st.caption("Thornbury Taphouse + Thornbury Theatre")
    
    st.divider()

    # --------------------------------------------------------
    # HIDDEN ADMIN ACCESS
    # --------------------------------------------------------
    # We hide the password field inside an expander so it doesn't distract the client
    with st.expander("⚙️ Settings"):
        admin_password = st.text_input("Agency Access", type="password")

    # If the password matches, unlock the manager view. 
    # Otherwise, force it into Client View.
    if admin_password == "growth2026":  # Change "growth2026" to your preferred password
        view_mode = "Marketing Manager"
        st.success("🔓 Marketing Manager View Unlocked")
    else:
        view_mode = "Client View"

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

    st.header("🏠 Executive Dashboard")

    # --------------------------------------------------------
    # WEEKLY WINS & ACTION BOARD (SEPARATE STREAMS)
    # --------------------------------------------------------
    st.subheader("📣 Weekly Status & Action Items")

    col_wins, col_needs = st.columns(2)

    # --------------------------------------------------------
    # STREAM A: WEEKLY STATUS UPDATES (Read-Only for Client)
    # --------------------------------------------------------
    wins_cols = ["Timestamp", "Weekly Update"]
    wins_df = read_sheet("Weekly_Wins_Data", wins_cols)
    
    latest_win_text = "No updates posted yet."
    if not wins_df.empty:
        latest_win_text = wins_df.iloc[-1]["Weekly Update"]

    with col_wins:
        st.success(f"**🏆 Latest Weekly Update:**\n\n{latest_win_text}")

  # --------------------------------------------------------
    # STREAM B: CLIENT ACTION ITEMS & QUESTIONS
    # --------------------------------------------------------
    action_cols = ["Timestamp", "Task / Question", "Status", "Client Response"]
    action_df = read_sheet("Client_Action_Items", action_cols)

    # Force string types to prevent Pandas dtype errors when updating cells
    if not action_df.empty:
        for col in action_df.columns:
            action_df[col] = action_df[col].astype(str)

    with col_needs:
        st.warning("**⏳ Action Items & Questions for You:**")
        
        has_open = False
        if not action_df.empty:
            open_items = action_df[action_df["Status"].str.lower() == "open"]
            
            if not open_items.empty:
                has_open = True
                for idx, row in open_items.iterrows():
                    with st.container(border=True):
                        st.markdown(f"**📌 {row['Task / Question']}**")
                        if row['Client Response'] and row['Client Response'] != "nan" and row['Client Response'] != "":
                            st.caption(f"Your last reply: {row['Client Response']}")
                        
                        # Client Reply Form
                        with st.form(key=f"reply_form_{idx}"):
                            client_reply = st.text_input("Type your response:", key=f"input_{idx}")
                            
                            c_btn1, c_btn2 = st.columns(2)
                            with c_btn1:
                                submit_reply = st.form_submit_button("💬 Send Answer")
                            with c_btn2:
                                mark_resolved = st.form_submit_button("✅ Resolve Task")
                                
                            if submit_reply:
                                if not client_reply.strip():
                                    st.error("⚠️ Reply cannot be blank.")
                                else:
                                    action_df.at[idx, "Client Response"] = str(client_reply)
                                    if update_sheet("Client_Action_Items", action_df):
                                        st.success("✅ Response sent!")
                                        time.sleep(1)
                                        st.rerun()
                                        
                            elif mark_resolved:
                                action_df.at[idx, "Status"] = "Resolved"
                                if client_reply.strip():
                                    action_df.at[idx, "Client Response"] = str(client_reply)
                                if update_sheet("Client_Action_Items", action_df):
                                    st.success("✅ Task resolved!")
                                    time.sleep(1)
                                    st.rerun()

        if not has_open:
            st.info("🎉 All caught up! No pending questions right now.")

    # ========================================================
    # MARKETING MANAGER ADMIN CONTROLS (With Status Reversal)
    # ========================================================
    if view_mode == "Marketing Manager":
        st.divider()
        st.markdown("### ⚙️ Manager Update Controls")
        
        m_col1, m_col2 = st.columns(2)
        
        # 1. Post a Weekly Status Update
        with m_col1:
            with st.expander("📝 Post New Weekly Status", expanded=False):
                with st.form("weekly_status_form"):
                    new_win_input = st.text_area("Write weekly update / milestone:", value="", height=120)
                    win_submit = st.form_submit_button("🚀 Publish Status Update")
                    
                    if win_submit:
                        if not new_win_input.strip():
                            st.error("⚠️ Status update cannot be blank.")
                        else:
                            row = {
                                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "Weekly Update": new_win_input.strip()
                            }
                            if append_to_sheet("Weekly_Wins_Data", row, wins_cols):
                                st.success("✅ Weekly update published!")
                                time.sleep(1)
                                st.rerun()

        # 2. Ask a New Question / Create Action Item
        with m_col2:
            with st.expander("❓ Ask a New Question to Client", expanded=False):
                with st.form("new_action_form"):
                    new_question_input = st.text_area("What do you need from the client?", value="", height=120)
                    question_submit = st.form_submit_button("📤 Send Question to Client")
                    
                    if question_submit:
                        if not new_question_input.strip():
                            st.error("⚠️ Question cannot be blank.")
                        else:
                            new_row = {
                                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "Task / Question": new_question_input.strip(),
                                "Status": "Open",
                                "Client Response": ""
                            }
                            if append_to_sheet("Client_Action_Items", new_row, action_cols):
                                st.success("✅ Question sent to client!")
                                time.sleep(1)
                                st.rerun()

        # 3. Manage & Reopen Resolved Tasks (Reverse Function)
        st.markdown("#### 🔄 Manage & Reopen Past Questions")
        with st.expander("View Resolved / History Log & Reopen Tasks", expanded=False):
            if not action_df.empty:
                resolved_items = action_df[action_df["Status"].str.lower() == "resolved"]
                
                if resolved_items.empty:
                    st.info("No resolved tasks in history.")
                else:
                    for r_idx, r_row in resolved_items.iterrows():
                        with st.container(border=True):
                            st.markdown(f"**📌 {r_row['Task / Question']}**")
                            st.caption(f"Last Client Response: {r_row['Client Response'] or 'None'}")
                            
                            if st.button("↩️ Reopen Task (Set to Open)", key=f"reopen_{r_idx}"):
                                action_df.at[r_idx, "Status"] = "Open"
                                if update_sheet("Client_Action_Items", action_df):
                                    st.success("✅ Task reopened and moved back to client queue!")
                                    time.sleep(1)
                                    st.rerun()
            else:
                st.info("No action items recorded yet.")

   # --------------------------------------------------------
    # CONSOLIDATED ROI SNAPSHOT
    # --------------------------------------------------------
    st.divider()
    
    roi_cols = ["Timestamp", "Ad Spend", "Tracked Leads", "Estimated Revenue"]
    roi_df = read_sheet("ROI_Data", roi_cols)

    # Default values if the sheet is empty
    current_spend = 0
    current_leads = 0
    current_revenue = 0

    if not roi_df.empty:
        latest_roi = roi_df.iloc[-1]
        current_spend = latest_roi["Ad Spend"]
        current_leads = latest_roi["Tracked Leads"]
        current_revenue = latest_roi["Estimated Revenue"]

    st.subheader("💰 Campaign ROI Snapshot")
    
    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        metric_card("Total Ad Spend", f"${current_spend:,}")
    with rc2:
        metric_card("Total Tracked Leads", str(current_leads))
    with rc3:
        metric_card("Estimated Revenue Generated", f"${current_revenue:,}")

    # ========================================================
    # MARKETING MANAGER SPECIFIC VIEW
    # ========================================================
    if view_mode == "Marketing Manager":
        
        # Hidden form to update the big ROI numbers
        with st.expander("⚙️ Update ROI Numbers", expanded=False):
            with st.form("roi_update_form"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_spend = st.number_input("Total Ad Spend ($)", min_value=0, value=int(current_spend), step=50)
                with col2:
                    new_leads = st.number_input("Total Tracked Leads", min_value=0, value=int(current_leads), step=1)
                with col3:
                    new_revenue = st.number_input("Estimated Revenue ($)", min_value=0, value=int(current_revenue), step=100)
                
                roi_submit = st.form_submit_button("💾 Save ROI Data")
                
                if roi_submit:
                    row = {
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Ad Spend": new_spend,
                        "Tracked Leads": new_leads,
                        "Estimated Revenue": new_revenue
                    }
                    if append_to_sheet("ROI_Data", row, roi_cols):
                        st.success("✅ ROI Snapshot updated!")
                        time.sleep(1.5)
                        st.rerun()

        st.divider()
        
        # Granular metrics are now hidden from the client, visible only to the manager
        st.subheader("📈 Granular Performance Indicators")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("Monday–Thursday Revenue", "$8,420", "+12%")
        with c2:
            metric_card("Weekday Covers", "126", "+18%")
        with c3:
            metric_card("Corporate Leads", "18", "+6")
        with c4:
            metric_card("Corporate Bookings", "3", "+1")

    st.divider()

  # --------------------------------------------------------
    # CURRENT PROJECT STATUS (Visible to both)
    # --------------------------------------------------------
    st.subheader("🚀 Current Project Status")

    # Fetch live website progress for the dashboard card
    web_df_dash = read_sheet("Website_Data", ["Task", "Completed"])
    total_web_tasks = 12
    completed_web_count = 0
    
    if not web_df_dash.empty:
        completed_web_count = len(web_df_dash[web_df_dash['Completed'].astype(str) == 'True'])
    
    web_progress_val = (completed_web_count / total_web_tasks) if total_web_tasks > 0 else 0

    p1, p2 = st.columns(2)

    with p1:
        st.markdown("### Website Revamp")
        st.progress(
            web_progress_val, 
            text=f"{completed_web_count}/{total_web_tasks} completed — {web_progress_val:.0%}"
        )
        st.markdown(
            "Track the live transformation from discovery and UX audits through to final QA and launch."
        )

    with p2:
        st.markdown("### Marketing Setup")
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
# --------------------------------------------------------
    # SUBMISSION HISTORY (CLIENT TRANSPARENCY)
    # --------------------------------------------------------
    st.divider()
    st.subheader("🗄️ Discovery History")

    # 1. Fetch the data
    discovery_df = read_sheet("Discovery", discovery_columns)

    if not discovery_df.empty:
        # 2. Reverse the data so newest is at the top
        discovery_reversed = discovery_df.iloc[::-1]

        # 3. Display it as a clean, interactive table
        st.dataframe(
            discovery_reversed,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No discovery sessions have been recorded yet.")
# ============================================================
# 3. WEBSITE
# ============================================================

with tabs[2]:

    st.header("🌐 Website Revamp Tracker")
    st.markdown("Monitor and manage the website transformation stages from discovery to launch.")

    web_columns = ["Task", "Completed"]
    web_df = read_sheet("Website_Data", web_columns)
    
    saved_web_status = {}
    if not web_df.empty:
        saved_web_status = dict(zip(web_df['Task'], web_df['Completed'].astype(str) == 'True'))

    website_tasks = [
        "Discovery & Requirements",
        "Website UX Audit",
        "Competitor Research",
        "Information Architecture",
        "Restaurant Wireframes",
        "Corporate Events Landing Page",
        "Mobile-First Design",
        "SEO Structure",
        "OpenTable Integration",
        "Analytics & Conversion Tracking",
        "Final QA",
        "Website Launch"
    ]

    # ========================================================
    # MARKETING MANAGER VIEW (Interactive Checklist Form)
    # ========================================================
    if view_mode == "Marketing Manager":
        st.info("🔒 **Admin Mode:** Update checklist states below and click save.")
        
        with st.form("website_form"):
            completed = 0
            current_web_states = {}

            for task in website_tasks:
                default_val = saved_web_status.get(task, False)
                value = st.checkbox(task, value=default_val, key=f"website_{task}")
                current_web_states[task] = value
                
                if value:
                    completed += 1

            progress = completed / len(website_tasks)
            st.progress(progress, text=f"{completed}/{len(website_tasks)} completed")
            
            web_submit = st.form_submit_button("💾 Save Website Progress")
            
            if web_submit:
                new_web_data = [{"Task": k, "Completed": v} for k, v in current_web_states.items()]
                if update_sheet("Website_Data", pd.DataFrame(new_web_data)):
                    st.success("✅ Website progress saved.")
                    time.sleep(1)
                    st.rerun()

    # ========================================================
    # CLIENT VIEW (Read-Only Status Overview)
    # ========================================================
    elif view_mode == "Client View":
        st.markdown("Here is the current completion status of your website overhaul:")
        
        for task in website_tasks:
            is_done = saved_web_status.get(task, False)
            if is_done:
                st.markdown(f"✅ **{task}** — Completed")
            else:
                st.markdown(f"⏳ **{task}** — In Progress / Pending")

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
    st.markdown("Build repeatable reasons for customers to visit Monday–Thursday.")

    # Wrap all inputs in a form so they save together
    with st.form("restaurant_growth_form"):
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
        day_inputs = {}

        # Generate the daily input cards
        for day in days:
            with st.expander(f"{day} Metrics", expanded=(day == "Tuesday")):
                col1, col2, col3 = st.columns(3)

                with col1:
                    c = st.number_input(f"{day} covers", min_value=0, step=1, key=f"{day}_covers")
                with col2:
                    r = st.number_input(f"{day} revenue ($)", min_value=0, step=100, key=f"{day}_revenue")
                with col3:
                    t = st.number_input(f"{day} target covers", min_value=0, step=5, key=f"{day}_target")
                
                # Store inputs in a dictionary to process upon save
                day_inputs[day] = {"Covers": c, "Revenue": r, "Target": t}
                
                if t > 0:
                    achievement = min(c / t, 1)
                    st.progress(achievement, text=f"{c}/{t} covers")

        st.divider()

        st.subheader("🔥 Super Tuesday Activation")

        activation = st.selectbox(
            "Current Tuesday activation",
            ["Tap Tuesday", "Local Hospo Night", "Secret Menu", "Trivia Night", "Live Music", "Other"]
        )

        description = st.text_area(
            "Tuesday offer / campaign description",
            placeholder="Example: rotating taps + Tuesday-only food special."
        )

        # The Save Button
        restaurant_submit = st.form_submit_button("💾 Save Restaurant Data")

        if restaurant_submit:
            # 1. Update the Monday-Thursday metrics in Restaurant_Data tab
            rest_data = []
            for day in days:
                rest_data.append({
                    "Day": day,
                    "Covers": day_inputs[day]["Covers"],
                    "Target": day_inputs[day]["Target"],
                    "Revenue": day_inputs[day]["Revenue"]
                })
            
            df_rest = pd.DataFrame(rest_data)
            
            # Note: This uses update_sheet to OVERWRITE the current week's data 
            # so your Analytics charts stay clean.
            update_success = update_sheet("Restaurant_Data", df_rest)

            # 2. Append the Tuesday Activation record
            activation_row = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Activation": activation,
                "Description": description
            }
            
            activation_success = append_to_sheet(
                "Tuesday_Activation", 
                activation_row, 
                ["Timestamp", "Activation", "Description"]
            )

            if update_success and activation_success:
                st.success("✅ Restaurant metrics and Super Tuesday data saved successfully.")

    # --------------------------------------------------------
    # DISPLAY CURRENT METRICS OUTSIDE THE FORM
    # --------------------------------------------------------
    st.divider()
    
    st.info(
        "Recommendation: test one strong Tuesday proposition for 4–6 weeks and compare "
        "incremental covers, revenue, average spend and repeat visits."
    )
# --------------------------------------------------------
    # TUESDAY ACTIVATION HISTORY (CLIENT TRANSPARENCY)
    # --------------------------------------------------------
    st.divider()
    st.subheader("🗄️ Super Tuesday Activation History")
    
    tuesday_cols = ["Timestamp", "Activation", "Description"]
    tuesday_df = read_sheet("Tuesday_Activation", tuesday_cols)
    
    if not tuesday_df.empty:
        st.dataframe(
            tuesday_df.iloc[::-1],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No Tuesday campaigns have been recorded yet.")
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
# --------------------------------------------------------
    # CORPORATE LEADS HISTORY (CLIENT TRANSPARENCY)
    # --------------------------------------------------------
    st.divider()
    st.subheader("🗄️ Corporate Leads History")
    
    leads_df = read_sheet("Corporate_Leads", lead_columns)
    
    if not leads_df.empty:
        # Reverse the dataframe to show newest first
        st.dataframe(
            leads_df.iloc[::-1],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No corporate leads have been recorded yet.")
# ============================================================
# 6. CONTENT STUDIO
# ============================================================

with tabs[5]:

    st.header("🎬 Content Studio")

    content_columns = [
        "Timestamp", "Brand", "Content Type", "Title", 
        "Hook", "Platform", "Status", "Publish Date", "Client Notes"
    ]
    
    # Fetch data first so both views can use it
    content_df = read_sheet("Content", content_columns)

    # ========================================================
    # 1. MARKETING MANAGER VIEW (Creation & Revisions)
    # ========================================================
    if view_mode == "Marketing Manager":
        
        # A. Draft New Content Form
        with st.form("content_form"):
            st.subheader("➕ Draft New Content")
            
            col1, col2 = st.columns(2)
            with col1:
                brand = st.selectbox("Brand", ["Thornbury Taphouse", "Thornbury Theatre", "Both"])
                content_type = st.selectbox("Content Type", ["Reel", "Carousel", "Photo", "Story", "Corporate", "UGC"])
                title = st.text_input("Content Title")
            with col2:
                platform = st.multiselect("Platform", ["Instagram", "Facebook", "TikTok", "LinkedIn"])
                publish_date = st.date_input("Publish Date", value=date.today())
                # Default new items to "In Review" so they go straight to the client
                status = st.selectbox("Status", ["In Review", "Draft", "Scheduled", "Published"])
                
            hook = st.text_area("Post Copy / First 3 Seconds")
            client_notes = st.text_area("Internal Notes (Optional)")

            content_submit = st.form_submit_button("💾 Save & Send to Client")

            if content_submit and title:
                row = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Brand": brand,
                    "Content Type": content_type,
                    "Title": title,
                    "Hook": hook,
                    "Platform": ", ".join(platform),
                    "Status": status,
                    "Publish Date": str(publish_date),
                    "Client Notes": client_notes
                }

                if append_to_sheet("Content", row, content_columns):
                    st.success("✅ Content sent to client for approval.")
                    st.rerun()

        st.divider()

        # B. Revisions Queue (Only visible to the Manager)
        st.subheader("⚠️ Revisions Needed")
        
        if not content_df.empty:
            revisions_df = content_df[content_df["Status"] == "Changes Requested"]
            
            if revisions_df.empty:
                st.info("No content currently requires your revision.")
            else:
                for idx, row in revisions_df.iterrows():
                    with st.expander(f"Fix: {row['Title']} (Feedback from Client)", expanded=True):
                        st.error(f"**Client Feedback:** {row['Client Notes']}")
                        
                        # Let the manager edit the actual content
                        new_hook = st.text_area("Update the copy/hook:", value=row['Hook'], key=f"edit_hook_{idx}")
                        manager_reply = st.text_input("Reply to client (optional):", key=f"reply_{idx}")
                        
                        if st.button("📤 Send Back for Approval", key=f"resend_{idx}", type="primary"):
                            content_df.at[idx, "Hook"] = new_hook
                            content_df.at[idx, "Status"] = "In Review"
                            
                            # Combine the chat history in the notes column
                            if manager_reply:
                                content_df.at[idx, "Client Notes"] = f"Agency Reply: {manager_reply} | Prior Feedback: {row['Client Notes']}"
                            
                            if update_sheet("Content", content_df):
                                st.rerun()
        st.divider()


    # ========================================================
    # 2. APPROVAL QUEUE (Visible to Everyone)
    # ========================================================
    st.subheader("✅ Needs Client Approval")
    
    if not content_df.empty:
        pending_df = content_df[content_df["Status"] == "In Review"]
        
        if pending_df.empty:
            st.success("🎉 All caught up! No content is currently waiting for approval.")
        else:
            for idx, row in pending_df.iterrows():
                with st.expander(f"📝 {row['Title']} (Scheduled: {row['Publish Date']})", expanded=True):
                    st.markdown(f"**Brand:** {row['Brand']} | **Platform:** {row['Platform']}")
                    st.markdown(f"**Copy/Concept:** {row['Hook']}")
                    
                    if row['Client Notes']:
                        st.info(f"**Notes:** {row['Client Notes']}")
                    
                    # Blank input for fresh client feedback
                    client_feedback = st.text_input(
                        "Add feedback or request changes:", 
                        key=f"client_fb_{idx}"
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Approve Content", key=f"approve_{idx}", type="primary"):
                            content_df.at[idx, "Status"] = "Approved"
                            if client_feedback:
                                content_df.at[idx, "Client Notes"] = client_feedback
                            if update_sheet("Content", content_df):
                                st.rerun()
                    
                    with col2:
                        if st.button("🔄 Request Changes", key=f"reject_{idx}"):
                            # Prevent sending back without actual feedback
                            if not client_feedback:
                                st.warning("Please type your feedback in the box before requesting changes.")
                            else:
                                content_df.at[idx, "Status"] = "Changes Requested"
                                content_df.at[idx, "Client Notes"] = client_feedback
                                if update_sheet("Content", content_df):
                                    st.rerun()
    else:
        st.info("No content pipeline has been established yet.")

    # ========================================================
    # 3. HISTORY TABLE (Visible to Everyone)
    # ========================================================
    st.divider()
    st.subheader("🗄️ Content Pipeline History")
    
    if not content_df.empty:
        st.dataframe(
            content_df.iloc[::-1],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No content has been added yet.")
# ============================================================
# 7. CRM & LOYALTY
# ============================================================

with tabs[6]:

    st.header("📧 CRM & Loyalty")
    st.markdown("Build a first-party customer database and increase repeat visits.")

    # Fetch existing data to show the latest metrics
    crm_columns = [
        "Timestamp", "Database Size", "New Subscribers", 
        "Open Rate", "Email Bookings", "Active Segments"
    ]
    crm_df = read_sheet("CRM_Data", crm_columns)

    if not crm_df.empty:
        latest_crm = crm_df.iloc[-1]
        
        st.subheader("Current Performance")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("Customer Database", str(latest_crm["Database Size"]))
        with c2:
            metric_card("New Subscribers", str(latest_crm["New Subscribers"]))
        with c3:
            metric_card("Email Open Rate", str(latest_crm["Open Rate"]))
        with c4:
            metric_card("Bookings from Email", str(latest_crm["Email Bookings"]))
            
    st.divider()

    # Form to input and save new data
    with st.form("crm_form"):
        st.subheader("Update CRM Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            db_size = st.number_input("Customer Database Size", min_value=0, step=10)
        with col2:
            new_subs = st.number_input("New Subscribers", min_value=0, step=1)
        with col3:
            open_rate = st.number_input("Email Open Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
        with col4:
            email_bookings = st.number_input("Bookings from Email", min_value=0, step=1)

        st.divider()

        st.subheader("Thornbury Insider & Segments")

        st.markdown("""
        **Potential member benefits**
        - Early access to shows
        - Special weekday offers
        - Birthday reward
        - Exclusive events
        - Member-only experiences
        - Ticket presales
        """)

        segments = st.multiselect(
            "Active CRM segments",
            [
                "Restaurant Customers",
                "Theatre Customers",
                "Restaurant + Theatre Customers",
                "Corporate Leads",
                "VIP / Repeat Customers"
            ],
            default=["Restaurant Customers", "Theatre Customers"]
        )

        crm_submit = st.form_submit_button("💾 Save CRM Data")

        if crm_submit:
            row = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Database Size": db_size,
                "New Subscribers": new_subs,
                "Open Rate": f"{open_rate}%",
                "Email Bookings": email_bookings,
                "Active Segments": ", ".join(segments)
            }

            if append_to_sheet("CRM_Data", row, crm_columns):
                st.success("✅ CRM & Loyalty data saved successfully. Refresh to see updated metrics.")

    st.info(
        "Use the existing customer database where legally permitted "
        "and ensure marketing communications have appropriate consent."
    )
# --------------------------------------------------------
    # CRM HISTORY (CLIENT TRANSPARENCY)
    # --------------------------------------------------------
    st.divider()
    st.subheader("🗄️ CRM Growth History")
    
    # We fetch it again here or use the crm_df already loaded at the top
    if not crm_df.empty:
        st.dataframe(
            crm_df.iloc[::-1],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No CRM data has been recorded yet.")
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
    
    restaurant_data = read_sheet("Restaurant_Data", ["Day", "Covers", "Target", "Revenue"])

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
# ========================================================
    # UTM LINK GENERATOR & REPOSITORY (Marketing Manager Only)
    # ========================================================
    if view_mode == "Marketing Manager":
        
        st.divider()
        st.subheader("🔗 UTM Tracking Link Generator & History")
        st.markdown("Create clean, trackable URLs and save them to prevent campaign duplication.")

        utm_columns = ["Timestamp", "Campaign Name", "Destination URL", "Source", "Medium", "Final UTM URL"]

        with st.form("utm_builder_form"):
            base_url = st.text_input(
                "Destination URL (Required)", 
                placeholder="https://www.thornbury.com/corporate-events"
            )
            
            c1, c2, c3 = st.columns(3)
            with c1:
                utm_source = st.text_input("Source (Required)", placeholder="e.g., meta, google, newsletter")
            with c2:
                utm_medium = st.text_input("Medium (Required)", placeholder="e.g., cpc, social, email")
            with c3:
                utm_campaign = st.text_input("Campaign Name (Required)", placeholder="e.g., xmas_party_2026")
                
            c4, c5 = st.columns(2)
            with c4:
                utm_term = st.text_input("Term (Optional)", placeholder="e.g., corporate+venues")
            with c5:
                utm_content = st.text_input("Content (Optional)", placeholder="e.g., video_v1, image_v2")

            generate_utm = st.form_submit_button("🔨 Generate & Save Tracking Link")

            if generate_utm:
                if base_url and utm_source and utm_medium and utm_campaign:
                    import urllib.parse
                    
                    base_url = base_url.strip()
                    if not base_url.startswith('http'):
                        base_url = 'https://' + base_url
                        
                    clean_campaign = utm_campaign.strip().replace(" ", "_").lower()
                    
                    params = {
                        'utm_source': utm_source.strip().lower(),
                        'utm_medium': utm_medium.strip().lower(),
                        'utm_campaign': clean_campaign
                    }
                    if utm_term:
                        params['utm_term'] = utm_term.strip().replace(" ", "_").lower()
                    if utm_content:
                        params['utm_content'] = utm_content.strip().replace(" ", "_").lower()
                        
                    query_string = urllib.parse.urlencode(params)
                    separator = '&' if '?' in base_url else '?'
                    final_url = f"{base_url}{separator}{query_string}"
                    
                    # Package data to save to Google Sheets
                    row = {
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Campaign Name": clean_campaign,
                        "Destination URL": base_url,
                        "Source": utm_source.strip().lower(),
                        "Medium": utm_medium.strip().lower(),
                        "Final UTM URL": final_url
                    }
                    
                    if append_to_sheet("UTM_Links", row, utm_columns):
                        st.success("✅ Tracking link generated and saved to history!")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.error("⚠️ Please fill in all required fields: Destination URL, Source, Medium, and Campaign.")

        # Display history so you can check existing links before creating new ones
        st.markdown("### 🗄️ Previously Generated Links")
        utm_df = read_sheet("UTM_Links", utm_columns)
        
        if not utm_df.empty:
            st.dataframe(
                utm_df.iloc[::-1],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No tracking links have been generated yet.")
# ============================================================
# 9. 90-DAY ROADMAP
# ============================================================

with tabs[8]:

    st.header("🗓️ 90-Day Growth Sprint")
    st.markdown("Track the project week by week.")

    # 1. Fetch existing saved progress from Google Sheets
    roadmap_columns = ["Task", "Completed"]
    roadmap_df = read_sheet("Roadmap_Data", roadmap_columns)
    
    # Convert the saved data into a dictionary for easy lookup
    # 'Completed' comes back as a string ('True' or 'False') from Google Sheets
    saved_status = {}
    if not roadmap_df.empty:
        saved_status = dict(zip(roadmap_df['Task'], roadmap_df['Completed'].astype(str) == 'True'))

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

    total_tasks = sum(len(tasks) for tasks in phases.values())

    # 2. Build the Form
    with st.form("roadmap_form"):
        
        completed_tasks = 0
        current_states = {}

        for phase, tasks in phases.items():
            st.subheader(phase)

            for task in tasks:
                # Look up if this task was previously saved as True
                default_val = saved_status.get(task, False)
                
                done = st.checkbox(task, value=default_val, key=f"roadmap_{task}")
                current_states[task] = done
                
                if done:
                    completed_tasks += 1

        st.divider()

        progress = (completed_tasks / total_tasks) if total_tasks > 0 else 0

        st.progress(
            progress,
            text=f"{completed_tasks}/{total_tasks} milestones completed — {progress:.0%}"
        )

        roadmap_submit = st.form_submit_button("💾 Save Roadmap Progress")

        # 3. Save logic
        if roadmap_submit:
            # Convert the current checkbox states into a DataFrame
            new_roadmap_data = []
            for task_name, is_done in current_states.items():
                new_roadmap_data.append({
                    "Task": task_name,
                    "Completed": is_done
                })
            
            df_roadmap = pd.DataFrame(new_roadmap_data)
            
            # Overwrite the sheet so it acts as a permanent state tracker
            if update_sheet("Roadmap_Data", df_roadmap):
                st.success("✅ Roadmap progress saved successfully!")

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Thornbury Growth Command Centre • "
    "Restaurant + Theatre + Corporate Growth"
)
# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Thornbury Growth Command Centre • "
    "Restaurant + Theatre + Corporate Growth"
)
