import streamlit as st
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Thornbury Marketing Portal", layout="wide", page_icon="🏢")

# --- INITIALIZE SESSION STATE (To save data between clicks) ---
if 'questionnaire_saved' not in st.session_state:
    st.session_state['questionnaire_saved'] = False
if 'reel_ideas' not in st.session_state:
    st.session_state['reel_ideas'] = []

# --- HEADER ---
st.title("Thornbury Theatre & Taphouse")
st.subheader("Interactive Growth & Marketing Portal")
st.markdown("Welcome to your centralized hub. Use the tabs below to provide business details, track website progress, and review our social media strategy.")
st.divider()

# --- TABS SETUP ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 1. Discovery Questionnaire", 
    "🌐 2. Website Revamp", 
    "🎬 3. Reels Studio",
    "💼 4. Corporate B2B Launch"
])

# --- TAB 1: DISCOVERY QUESTIONNAIRE ---
with tab1:
    st.header("Brand & Operations Discovery")
    st.markdown("Help us understand the mechanics of your busy days so we can replicate them Monday to Thursday.")
    
    with st.form("discovery_form"):
        st.subheader("Brand Identity")
        st.text_input("What 3 words define Thornbury Taphouse?", placeholder="e.g., Local, Vibrant, Comforting")
        st.text_input("What 3 words define Thornbury Theatre?", placeholder="e.g., Historic, Energetic, Premium")
        
        st.subheader("Target Audience")
        st.multiselect("Who is your primary target for Monday–Wednesday dinners?", 
                       ["Locals/Neighbors", "Office Workers", "Students", "Hospo/Industry Staff"])
        
        st.subheader("Cloud Kitchen & Venue Capabilities")
        st.text_area("Which delivery-only cloud kitchen items have the highest margins and re-order rates?", 
                     placeholder="List 2-3 items we can feature as 'Secret Menu' dine-in exclusives.")
        st.radio("Does the Theatre have a dedicated A/V technician available for Mon–Wed corporate events?",
                 ["Yes, in-house", "Yes, on request", "No, client must provide"])
        
        st.subheader("Digital Assets")
        st.text_input("Link to your high-res photos/logos (Google Drive, Dropbox, etc.)")
        
        submitted = st.form_submit_button("Save Responses")
        if submitted:
            st.session_state['questionnaire_saved'] = True
            st.success("Your responses have been securely saved to the project board!")

# --- TAB 2: WEBSITE REVAMP ROADMAP ---
with tab2:
    st.header("Website Redesign Tracker")
    st.markdown("Track our phase-by-phase progress. Check off the boxes below as you approve each milestone.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Phase 1: Wireframes & Architecture")
        st.checkbox("Approve Thornbury Theatre Event Calendar Structure", value=False)
        st.checkbox("Approve 'Dine Before the Show' Cross-links", value=False)
        st.checkbox("Approve OpenTable Widget Placement for Taphouse", value=False)
        
    with col2:
        st.subheader("Phase 2: Design & Copy")
        st.checkbox("Approve High-Converting Corporate B2B Copy", value=False)
        st.checkbox("Approve Mobile-First UI Design", value=False)
        
    st.divider()
    st.subheader("Phase 3: Integration & Launch (Pending)")
    st.progress(0, text="Awaiting Phase 1 & 2 approvals before launch sequence begins.")

# --- TAB 3: REELS STUDIO ---
with tab3:
    st.header("Instagram Reels Pipeline")
    
    col_ideas, col_submit = st.columns([2, 1])
    
    with col_ideas:
        st.subheader("Current Scripts for Review")
        
        with st.expander("Reel 1: The 'Secret Menu' Reveal (Tue/Wed Target)", expanded=True):
            st.markdown("**Hook:** Fast-paced close-up of a kitchen ticket printing, chef drops an outrageous cloud kitchen dish on the pass.")
            st.markdown("**On-Screen Text:** *The Thornbury secret you aren't supposed to know 🤫*")
            st.selectbox("Status:", ["In Review", "Approved for Production", "Changes Requested"], key="status1")
            st.text_area("Client Notes (Reel 1):", placeholder="Looks good, but make sure to feature the spicy loaded fries.")
            
        with st.expander("Reel 2: The Hospo Escape (Mon Target)"):
            st.markdown("**Hook:** POV shot walking into the Taphouse, slow-mo beer sliding across the bar.")
            st.markdown("**On-Screen Text:** *When your weekend starts on a Monday... 🍻*")
            st.selectbox("Status:", ["In Review", "Approved for Production", "Changes Requested"], key="status2")

    with col_submit:
        st.subheader("Drop a New Idea")
        st.markdown("Have an idea while walking around the venue? Drop it here.")
        with st.form("new_idea_form", clear_on_submit=True):
            idea_title = st.text_input("Idea / Topic Title")
            idea_notes = st.text_area("Details or Reference Links")
            idea_submitted = st.form_submit_button("Send to Production Team")
            
            if idea_submitted and idea_title:
                st.session_state['reel_ideas'].append({"title": idea_title, "date": datetime.date.today()})
                st.success(f"Idea '{idea_title}' added to the board!")
                
        if st.session_state['reel_ideas']:
            st.markdown("**Your Submitted Ideas:**")
            for idea in st.session_state['reel_ideas']:
                st.caption(f"✅ {idea['title']} ({idea['date']})")

# --- TAB 4: CORPORATE B2B LAUNCH ---
with tab4:
    st.header("Corporate Event Packages (Mon-Thu)")
    st.markdown("We will use this section to refine the 3 B2B packages we will pitch on LinkedIn.")
    
    st.info("**Strategy:** We are pitching 'Frictionless Planning' to HR Managers and Event Coordinators.")
    
    st.markdown("### Draft Packages for Approval")
    st.text_input("Package 1 Name:", value="The Townhall (Presentation + Drinks)")
    st.text_input("Package 2 Name:", value="The Offsite (Full Day + Lunch/Dinner)")
    st.text_input("Package 3 Name:", value="The End-of-Year Gala (Banquet + DJ)")
    
    st.markdown("---")
    st.button("Request LinkedIn Outreach Scripts for these packages")