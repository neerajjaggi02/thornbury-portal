import streamlit as st

def render_scope_pricing():
    st.header("📑 Marketing Plan & Costing")

    # ========================================================
    # 1. DOWNLOAD LINK
    # ========================================================
    try:
        with open("marketing-plan_2.docx", "rb") as file:
            st.download_button(
                label="📄 Download Full Proposal (Word Doc)",
                data=file,
                file_name="marketing-plan_2.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    except FileNotFoundError:
        st.warning("⚠️ 'marketing-plan_2.docx' not found in the repository. Upload it to enable the download button.")

    st.divider()

    # ========================================================
    # 2. FULL DOCUMENT TEXT 
    # ========================================================
    st.markdown("""
    ### HOSPITALITY MARKETING & CREATIVE SERVICES
    **Client Pricing & Scope**  
    Hospitality Marketing Partner | Mumbai-based execution | 

    #### How We Work Together
    This proposal is structured in two phases, based on current priorities:

    **PHASE 1 — Cloud Kitchen Brand Launch (One-Time Project)**
    We begin with the brand launch as the priority project. This covers everything needed to take the cloud kitchen brand from concept to market — identity, packaging, digital presence, and launch collateral. A flat project management fee covers my oversight for the full duration.

    **PHASE 2 — Ongoing Monthly Retainer (When Ready to Scale)**
    Once the brand is live and operational, we move into a recurring monthly engagement covering creative, social media, website maintenance, and marketing leadership across all properties.

    ---

    ### PHASE 1
    **Cloud Kitchen Brand Launch — One-Time Project**

    #### Brand Launch Deliverables
    | Deliverable | Fee | What's Included |
    | :--- | :--- | :--- |
    | **Brand Concept & Creative Direction** | ₹10,000–₹15,000 | Concept development, moodboard, visual language & tone |
    | **Logo & Brand Identity** | ₹8,000–₹15,000 | 2–3 logo directions, refinement, colour palette, typography, final files |
    | **Primary Packaging Design** | ₹5,000–₹8,000 | One primary takeaway box/packaging, print-ready artwork |
    | **Website UI/UX Design (4–5 pages)** | ₹15,000–₹20,000 | Desktop & mobile design, developer-ready files |
    | **Standees, Banners & Menu Collateral** | ₹6,000–₹10,000 | Core launch collateral for the outlet |
    | **Animated Logo** | ₹3,000–₹5,000 | Social-ready animated version of the logo |
    | **Social Media Launch Kit** | ₹3,000–₹5,000 | Profile assets, cover images, launch visual direction |
    | **Project Management & QA** | ₹8,000–₹12,000 | Coordination across design vendors, approvals & final QA |

    #### Website Development (New Brand)
    Built on the approved UI/UX design. Quoted separately from design.

    | Component | Fee |
    | :--- | :--- |
    | **Full website development (4–5 pages, responsive)** | ₹30,000–₹50,000 |
    | **CMS setup, content implementation & standard forms** | Included |
    | **Basic QA and launch support** | Included |
    
    *Excludes: hosting/domain, paid plugins, ordering/payment systems, third-party integrations, copywriting.*

    #### Marketing Lead — Project Oversight Fee
    A flat fee covering end-to-end project management of the brand launch from briefing through to go-live. Includes vendor coordination, creative direction, timeline management, stakeholder approvals and quality control across all deliverables (~6–8 weeks).

    | Role | Fee |
    | :--- | :--- |
    | **Marketing Lead / Project Oversight** (flat fee, full project duration) | ₹75,000 |

    *Separate from and in addition to the brand launch deliverables and website development costs above.*

    #### Phase 1 — Total Estimated Investment
    | Component | Estimated Cost | Nature |
    | :--- | :--- | :--- |
    | **Brand Launch Deliverables** | ₹58,000–₹90,000 | One-time |
    | **Website Development** | ₹30,000–₹50,000 | One-time |
    | **Marketing Lead / PM Oversight** | ₹75,000 | One-time (flat fee) |
    | **TOTAL PHASE 1** | **₹1,63,000–₹2,15,000** | **One-time** |

    *Final figures subject to confirmed scope. Each deliverable will have a written brief, timeline and revision allowance before commencement.*

    ---

    ### PHASE 2
    **Ongoing Monthly Retainer — When Ready to Scale**

    #### Monthly Investment at a Glance
    | Service | Monthly Fee | Billing |
    | :--- | :--- | :--- |
    | **Marketing Lead / Account & Project Management** | ₹1,00,000 | Monthly |
    | **Creative Design — 12–15 social posts** | ₹20,000 | Monthly |
    | **Social Media Management & Posting** | ₹12,000 | Monthly |
    | **Website Maintenance — 3 websites** | ₹15,000 | Monthly |
    | **TOTAL CORE MONTHLY COST** | **₹1,47,000** | **Monthly** |

    *Reels, influencer management, paid media and ad-hoc projects are charged only when required.*

    #### 1. Marketing Lead / Account & Project Management — ₹1,00,000/month
    * Overall marketing strategy and campaign planning
    * End-to-end project management across restaurant, theatre, digital and social
    * Coordination with Melbourne stakeholders and Mumbai execution team
    * Creative briefing and creative direction
    * Review and quality control of all major deliverables
    * Feedback consolidation, revision management and stakeholder approvals
    * Website, brand and ongoing project oversight
    * Influencer and campaign coordination
    * Timeline, dependency and delivery management
    * Up to approximately 2 hours/day, Monday–Sunday (~60 hours/month)
    
    *Excludes: specialist execution, media spend, influencer fees, production, printing, travel and third-party software.*

    #### 2. Creative Design Retainer — ₹20,000/month
    * Covers 12–15 brand-consistent social media creatives per month across Instagram and Facebook.
    * Static posts, promotional creatives, event/offer creatives and carousels
    * Basic format adaptations across platforms
    * Up to two revision rounds per creative
    * Coordination with Marketing Lead and Social Media Manager
    * Source/editable files where appropriate
    
    *Individual rates apply for work outside the retainer — see Creative Rate Card at the end of this document.*

    #### 3. Social Media Management & Posting — ₹12,000/month
    * Instagram + Facebook management
    * Content calendar and caption/hashtag coordination
    * Scheduling and publishing approved content
    * Basic profile/content optimisation
    * Basic monitoring, escalation and monthly reporting coordination
    
    *Excludes: paid advertising, high-volume customer service and original content production.*

    #### 4. Website Maintenance — 3 Websites — ₹15,000/month
    | Website | Monthly Fee |
    | :--- | :--- |
    | **Website 1** | ₹5,000 |
    | **Website 2** | ₹5,000 |
    | **Website 3** | ₹5,000 |
    | **Total** | **₹15,000** |

    * Menu/price changes and text & image updates
    * Minor layout edits and promotional banners
    * Routine CMS/plugin updates where applicable
    * Basic bug fixes, troubleshooting and backup coordination
    * Minor campaign or landing-page changes
    
    *Major redesigns, new pages, new functionality and development projects are quoted separately.*

    #### 5. Website Revamp — Existing Websites
    **₹25,000–₹35,000* per website**

    | Component | Status | Scope |
    | :--- | :--- | :--- |
    | **Audit & UX review** | Included | Existing-site review and improvement recommendations |
    | **Visual/UI refresh** | Included | Homepage + agreed key pages/templates |
    | **Desktop & mobile updates** | Included | Responsive design for agreed scope |
    | **Content/menu/image updates** | Included | Using client-supplied assets |
    | **Development implementation** | Included | Approved design changes |
    | **Standard forms/functionality** | Included | Existing standard functionality retained/updated |
    | **QA & launch support** | Included | Basic device/browser testing and go-live coordination |

    *Based on 4–6 key pages/templates per site. Excludes rebuild/migration, custom applications, ordering/payment systems, major SEO, copywriting, hosting/domain and paid plugins.*
    *\*If the website layout or UI/UX undergoes significant changes, the final pricing may differ from the original package.*

    #### 6. Optional Specialist Services
    *Charged only when required, on top of the monthly retainer.*

    | Service | Rate |
    | :--- | :--- |
    | **Additional social post** | ₹800 |
    | **Story creative** | ₹600 |
    | **Carousel (up to 5 slides)** | ₹2,000 |
    | **Simple animated creative** | ₹2,000 |
    | **Reel editing (supplied footage)** | ₹3,000/reel |
    | **Complex motion graphic** | ₹5,000–₹7,500 |
    | **Influencer campaign management** | ₹8,000–₹12,000/campaign |
    | **Paid media management** | ₹10,000–₹15,000/month |
    | **Additional packaging SKU** | ₹5,000–₹10,000 |
    | **Professional photography/videography** | Separately quoted |

    #### 7. Exclusions & Commercial Conditions
    * Paid advertising/media spend
    * Influencer/talent fees, gifting and collaboration costs
    * Photography, videography and on-site content production
    * Travel, accommodation and local production expenses
    * Printing, fabrication, signage production and installation
    * Website hosting and domain charges
    * Paid plugins, apps, software and third-party subscriptions
    * Major website functionality, integrations or platform migration
    * Professional copywriting unless specifically included
    * Work materially outside agreed monthly hours or project scope
    * Taxes, if applicable, are additional

    #### 8. Scope Protection
    * Monthly creative is capped at 12–15 social assets.
    * Each major creative/project deliverable includes up to two revision rounds unless otherwise agreed.
    * Website revamps are based on the existing platform and agreed page scope.
    * Website maintenance covers minor ongoing changes; major work is separately quoted.
    * Client/local Melbourne team supplies timely photographs, videos, reels/raw footage, menu information and approvals.
    * Timelines are dependent on timely content, access, feedback and stakeholder approvals.
    * Each one-time project will have a written scope, timeline and revision allowance before commencement.

    #### Recommended Positioning
    This proposal positions the team as a boutique hospitality marketing partner. Phase 1 delivers a complete, market-ready cloud kitchen brand. Phase 2 brings in one accountable Marketing Lead supported by specialist creative, social and development resources on a predictable monthly commitment. The structure allows each phase to be approved independently, with larger brand and website projects commissioned separately as the business grows.

    ---
    
    ### Detailed Creative Rate Card
    """)

    # ========================================================
    # 3. RATE CARD IMAGE
    # ========================================================
    try:
        st.image("rate_card.jpg", use_container_width=True)
    except FileNotFoundError:
        st.info("🖼️ To display the visual rate card, save the image as 'rate_card.jpg' in your main GitHub project folder.")
