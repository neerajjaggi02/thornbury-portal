import streamlit as st

def render_scope_pricing():
    st.header("📑 Marketing Plan & Costing")
    st.markdown("Overview of execution phases, deliverables, and estimated investments based on the current scope[cite: 1].")

    # --------------------------------------------------------
    # TOP-LEVEL SUMMARY
    # --------------------------------------------------------
    c1, c2 = st.columns(2)
    with c1:
        st.info(
            "**PHASE 1: Brand Launch (One-Time)**\n\n"
            "**Est. ₹1,63,000 – ₹2,15,000**[cite: 1]\n\n"
            "Takes the cloud kitchen brand from concept to market[cite: 1]."
        )
    with c2:
        st.success(
            "**PHASE 2: Monthly Retainer**\n\n"
            "**₹1,47,000 / month**[cite: 1]\n\n"
            "Ongoing marketing leadership, creative, and maintenance[cite: 1]."
        )

    st.divider()

    # --------------------------------------------------------
    # PHASE 1 BREAKDOWN
    # --------------------------------------------------------
    st.subheader("Phase 1: Cloud Kitchen Brand Launch")

    st.markdown("""
    | Deliverable | Estimated Fee | What's Included |
    | :--- | :--- | :--- |
    | **Brand Concept & Direction** | ₹10,000–₹15,000 | Concept development, moodboard, visual language & tone[cite: 1] |
    | **Logo & Brand Identity** | ₹8,000–₹15,000 | 2–3 logo directions, refinement, colour palette, typography, final files[cite: 1] |
    | **Primary Packaging Design** | ₹5,000–₹8,000 | One primary takeaway box/packaging, print-ready artwork[cite: 1] |
    | **Website UI/UX Design** | ₹15,000–₹20,000 | 4–5 pages desktop & mobile design, developer-ready files[cite: 1] |
    | **Launch Collateral** | ₹6,000–₹10,000 | Standees, banners, and core menu collateral for the outlet[cite: 1] |
    | **Social Media Assets** | ₹6,000–₹10,000 | Animated logo + Social Media Launch Kit (profile & cover assets)[cite: 1] |
    | **Project Management & QA** | ₹8,000–₹12,000 | Coordination across design vendors, approvals & final QA[cite: 1] |
    """)

    with st.expander("💻 Website Development & Marketing Oversight (Phase 1)"):
        st.markdown("""
        * **Full Website Development:** ₹30,000–₹50,000 (Responsive 4-5 pages, CMS setup, content implementation, standard forms)[cite: 1].
        * **Marketing Lead / Project Oversight:** ₹75,000 flat fee covering end-to-end project management for the ~6-8 week duration[cite: 1].
        """)

    st.divider()

    # --------------------------------------------------------
    # PHASE 2 BREAKDOWN
    # --------------------------------------------------------
    st.subheader("Phase 2: Core Monthly Retainer")

    st.markdown("""
    | Service | Monthly Fee | Description |
    | :--- | :--- | :--- |
    | **Marketing Lead / PM** | ₹1,00,000 | Overall strategy, campaign planning, and oversight (~60 hours/month)[cite: 1] |
    | **Creative Design** | ₹20,000 | 12–15 brand-consistent social media creatives per month[cite: 1] |
    | **Social Media Management** | ₹12,000 | Instagram + Facebook management, scheduling, and basic optimisation[cite: 1] |
    | **Website Maintenance** | ₹15,000 | Minor updates, bug fixes, and routine CMS management across 3 websites[cite: 1] |
    """)

    with st.expander("➕ Optional Specialist Services (Rate Card)"):
        st.markdown("""
        *Charged only when required, on top of the monthly retainer[cite: 1].*
        
        * **Additional Social Post:** ₹800[cite: 1]
        * **Story Creative:** ₹600[cite: 1]
        * **Carousel (up to 5 slides):** ₹2,000[cite: 1]
        * **Reel Editing (supplied footage):** ₹3,000/reel[cite: 1]
        * **Complex Motion Graphic:** ₹5,000–₹7,500[cite: 1]
        * **Paid Media Management:** ₹10,000–₹15,000/month[cite: 1]
        * **Influencer Campaign Management:** ₹8,000–₹12,000/campaign[cite: 1]
        * **Website Revamp (Existing):** ₹25,000–₹35,000 per website (audit, UI refresh, dev implementation)[cite: 1]
        """)
