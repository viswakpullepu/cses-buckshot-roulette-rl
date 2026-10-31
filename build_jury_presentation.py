"""
Jury Presentation Generator for Team CyberCore (CSES Buckshot Roulette).
Generates an executive, academic-grade 16:9 widescreen PPTX with:
- Simple, elegant tone colors (Light slate/white theme with royal navy and subtle accents)
- Team Name: CyberCore
- Participants: Vishwak Naidu & Dhivija
- Diverse visual layouts across every slide (no two slides look identical)
- Embedded charts, loss curves, flowcharts, and benchmarks
"""
import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Simple, Professional Tone Colors (Executive Light Palette)
BG_PAGE       = RGBColor(248, 250, 252)  # #F8FAFC Clean Slate Canvas
CARD_WHITE    = RGBColor(255, 255, 255)  # #FFFFFF Pure White
CARD_BORDER   = RGBColor(226, 232, 240)  # #E2E8F0 Subtle Slate Border
HEADER_TEXT   = RGBColor(15, 23, 42)     # #0F172A Deep Slate Navy
BODY_TEXT     = RGBColor(51, 65, 85)     # #334155 Slate 700
MUTED_TEXT    = RGBColor(100, 116, 139)  # #64748B Slate 500

ACCENT_BLUE   = RGBColor(29, 78, 216)    # #1D4ED8 Deep Royal Blue
ACCENT_TEAL   = RGBColor(13, 148, 136)   # #0D9488 Professional Teal
ACCENT_GREEN  = RGBColor(22, 101, 52)    # #166534 Success Green
ACCENT_AMBER  = RGBColor(180, 83, 9)     # #B45309 Champion Amber Gold
PILL_BG       = RGBColor(238, 242, 255)  # #EEF2FF Soft Indigo Tint
PILL_BORDER   = RGBColor(199, 210, 254)  # #C7D2FE
PILL_TEXT     = RGBColor(67, 56, 202)    # #4338CA


def build_cybercore_deck(filename="CSES_Buckshot_Roulette_Jury_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_page_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_PAGE
        bg.line.color.rgb = BG_PAGE
        return bg

    def add_top_bar(slide, title_text, category_text="TEAM CYBERCORE • CSES ARCADE RL HACKATHON • TECHNOZION '26"):
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), Inches(6.0), Inches(0.32))
        pill.fill.solid()
        pill.fill.fore_color.rgb = PILL_BG
        pill.line.color.rgb = PILL_BORDER
        pill.line.width = Pt(1.0)
        p_pill = pill.text_frame.paragraphs[0]
        p_pill.text = category_text
        p_pill.font.name = "Arial"
        p_pill.font.size = Pt(9.5)
        p_pill.font.bold = True
        p_pill.font.color.rgb = PILL_TEXT
        p_pill.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Arial"
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = HEADER_TEXT

    def add_panel(slide, left, top, width, height, bg=CARD_WHITE, border=CARD_BORDER, border_width=1.0):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = border
        card.line.width = Pt(border_width)
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Clean Hero Layout with Team Card)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_page_bg(slide1)

    add_panel(slide1, Inches(0.8), Inches(0.75), Inches(11.733), Inches(4.35), bg=CARD_WHITE, border=CARD_BORDER)

    tb = slide1.shapes.add_textbox(Inches(1.2), Inches(1.05), Inches(10.9), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.text = "NIT WARANGAL • TECHNOZION '26 • CSES ARCADE RL HACKATHON"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    tb_t = slide1.shapes.add_textbox(Inches(1.2), Inches(1.45), Inches(10.9), Inches(1.6))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p1 = tf_t.paragraphs[0]
    p1.text = "Autonomous Deep Q-Network Agent"
    p1.font.name = "Arial"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = HEADER_TEXT

    p2 = tf_t.add_paragraph()
    p2.text = "Multi-Agent Stochastic Survival in CSES Buckshot Roulette"
    p2.font.name = "Arial"
    p2.font.size = Pt(25)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_BLUE

    # Team Card
    add_panel(slide1, Inches(1.2), Inches(3.25), Inches(10.9), Inches(1.5), bg=RGBColor(241, 245, 249), border=RGBColor(203, 213, 225))
    tb_team = slide1.shapes.add_textbox(Inches(1.4), Inches(3.35), Inches(10.5), Inches(1.3))
    tf_team = tb_team.text_frame
    tf_team.word_wrap = True
    
    p_tm = tf_team.paragraphs[0]
    p_tm.text = "TEAM: CYBERCORE"
    p_tm.font.name = "Arial"
    p_tm.font.size = Pt(15)
    p_tm.font.bold = True
    p_tm.font.color.rgb = HEADER_TEXT

    p_names = tf_team.add_paragraph()
    p_names.text = "Participants: Vishwak Naidu  |  Dhivija"
    p_names.font.name = "Arial"
    p_names.font.size = Pt(13)
    p_names.font.bold = True
    p_names.font.color.rgb = ACCENT_TEAL

    p_sub = tf_team.add_paragraph()
    p_sub.text = "Submission: my_bot (Rank #1 • 42.50% Win Rate • +0.3500 Avg Points • Zero Runtime Dependencies)"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = BODY_TEXT

    # 4 Bottom Metric Chips
    metrics = [
        ("OFFICIAL STANDING", "Rank #1", ACCENT_AMBER),
        ("4-PLAYER BATTLE ROYALE", "42.50% Win Rate", ACCENT_GREEN),
        ("1v1 DUEL EFFICIENCY", "87.00% Win Rate", ACCENT_BLUE),
        ("DECISION LATENCY", "< 0.001s / Turn", ACCENT_TEAL),
    ]
    for i, (lbl, val, col) in enumerate(metrics):
        m_left = Inches(0.8 + i * 2.98)
        add_panel(slide1, m_left, Inches(5.35), Inches(2.83), Inches(1.45), bg=CARD_WHITE, border=CARD_BORDER)
        tb_m = slide1.shapes.add_textbox(m_left + Inches(0.15), Inches(5.48), Inches(2.53), Inches(1.2))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        
        p_l = tf_m.paragraphs[0]
        p_l.text = lbl
        p_l.font.name = "Arial"
        p_l.font.size = Pt(9.5)
        p_l.font.bold = True
        p_l.font.color.rgb = MUTED_TEXT

        p_v = tf_m.add_paragraph()
        p_v.text = val
        p_v.font.name = "Arial"
        p_v.font.size = Pt(17)
        p_v.font.bold = True
        p_v.font.color.rgb = col

    slide1.notes_slide.notes_text_frame.text = (
        "Good afternoon, respected NIT Warangal CSE professors and jury members. We are Team CyberCore, presented by Vishwak Naidu and Dhivija.\n\n"
        "Today we present our Autonomous Deep Q-Network Agent for CSES Buckshot Roulette. Our bot, my_bot, achieved Rank #1 in the official tournament evaluation with a 42.50% win rate across 120 matches, more than double the runner-up's points, all while running in pure Python under 1 millisecond per decision."
    )

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & CONSTRAINTS (2-Column Split)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_page_bg(slide2)
    add_top_bar(slide2, "Problem Domain: Game Dynamics vs Sandbox Constraints")

    # Left Column: Game Dynamics
    add_panel(slide2, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), bg=CARD_WHITE, border=RGBColor(199, 210, 254))
    tb_l = slide2.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(5.2), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "CSES Buckshot Roulette Mechanics"
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    rules = [
        ("Turn-Based Gunplay", "A shotgun is loaded with a secret chamber sequence of live and blank shells. Players take turns choosing to shoot an opponent or shoot themselves."),
        ("Multi-Agent Crossfire (2-4p)", "High stochasticity where turn order and player alliances cause unpredictable eliminations before a player can even act."),
        ("Utility Upgrades & Economy", "Juice (+1 HP heal), Mag Glass (peek chamber shell), Hand Saw (+1 dmg burst), Pool Floatie (skip enemy turn), Coffee (eject shell)."),
        ("Imperfect Information Dilemma", "Shells are hidden. Ejections can be known or unknown. A bot must track probabilities mathematically or risk fatal self-damage."),
    ]
    for h, d in rules:
        p_h = tf_l.add_paragraph()
        p_h.text = f"• {h}"
        p_h.font.name = "Arial"
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = HEADER_TEXT
        p_d = tf_l.add_paragraph()
        p_d.text = d
        p_d.font.name = "Arial"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = BODY_TEXT

    # Right Column: Sandbox Constraints
    add_panel(slide2, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.3), bg=CARD_WHITE, border=RGBColor(254, 215, 170))
    tb_r = slide2.shapes.add_textbox(Inches(7.05), Inches(1.85), Inches(5.2), Inches(4.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p_rh = tf_r.paragraphs[0]
    p_rh.text = "Strict Sandbox Execution Limits"
    p_rh.font.name = "Arial"
    p_rh.font.size = Pt(16)
    p_rh.font.bold = True
    p_rh.font.color.rgb = ACCENT_AMBER

    limits = [
        ("Zero External Dependencies", "The Docker evaluation sandbox is python:3.12-slim. Third-party ML packages (PyTorch, TensorFlow, NumPy) are strictly prohibited at runtime."),
        ("Memory Ceiling (128 MB RAM)", "Heavy neural frameworks fail immediately. The model must have a tiny memory footprint (< 30 MB)."),
        ("Per-Decision Timeout (0.05s)", "Each turn must execute within 50 milliseconds. Long tree searches or Monte Carlo simulations time out."),
        ("Match Time Budget (0.50s)", "Cumulative match compute cannot exceed half a second across all turns combined."),
    ]
    for h, d in limits:
        p_h = tf_r.add_paragraph()
        p_h.text = f"• {h}"
        p_h.font.name = "Arial"
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = HEADER_TEXT
        p_d = tf_r.add_paragraph()
        p_d.text = d
        p_d.font.name = "Arial"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = BODY_TEXT

    slide2.notes_slide.notes_text_frame.text = (
        "Slide 2 outlines the problem space. Buckshot Roulette requires balancing risk and reward under imperfect information.\n\n"
        "On the left, notice the game dynamics: a finite chamber with unknown live and blank shells, multi-agent crossfire, and utility items.\n"
        "On the right, notice the strict engineering bounds set by the organizers: maximum 128 MB RAM, less than 0.05s per decision, and standard library only.\n"
        "Team CyberCore designed our agent specifically to excel within these constraints without any external runtime dependencies."
    )

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE & FLOWCHART
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_page_bg(slide3)
    add_top_bar(slide3, "System Architecture: 5-Stage Zero-Dependency Pipeline")

    # Flowchart image across the top
    if os.path.exists("charts/pipeline_flowchart.png"):
        slide3.shapes.add_picture("charts/pipeline_flowchart.png", Inches(0.8), Inches(1.5), Inches(11.733), Inches(2.3))

    # 3 Summary Cards Below Flowchart
    arch_cards = [
        ("Bayesian Shell Observer", "Computes exact p_live and p_blank by tracking initial counts, shots, and ejected shells. Flags 100% certain live or blank states without guessing.", ACCENT_BLUE),
        ("Pure Python Deep Q-Network", "Evaluates Q(s, a) over 18 features via a compact MLP (18->48->24->7). Exported weights total 65 KB. Multiplications take < 0.001s with zero dependencies.", ACCENT_TEAL),
        ("Action Masking & Targeting", "Enforces non-negotiable game invariants (heal if hurt, zero gamble on blanks) and directs fire with Threat-Weighted Anti-Snowball targeting.", ACCENT_AMBER),
    ]
    for i, (ctitle, cdesc, col) in enumerate(arch_cards):
        c_left = Inches(0.8 + i * 3.98)
        add_panel(slide3, c_left, Inches(4.0), Inches(3.78), Inches(2.9), bg=CARD_WHITE, border=col, border_width=1.2)

        tb = slide3.shapes.add_textbox(c_left + Inches(0.2), Inches(4.15), Inches(3.38), Inches(2.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = ctitle
        p_t.font.name = "Arial"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        p_d = tf.add_paragraph()
        p_d.text = cdesc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = BODY_TEXT

    slide3.notes_slide.notes_text_frame.text = (
        "Slide 3 illustrates our five-stage end-to-end inference pipeline.\n\n"
        "Stage 1 calculates exact Bayesian shell counts: remaining lives, blanks, and uncertain ejections.\n"
        "Stage 2 formats this into a normalized 18-dimensional feature vector.\n"
        "Stage 3 executes the forward pass of our trained Deep Q-Network. Because weights are exported into compact JSON (48x18, 24x48, 7x24), inference requires ~2,280 basic multiplications. This takes less than 0.001 seconds—50x faster than the timeout threshold!\n"
        "Stage 4 combines the Q-values with hierarchical action masks to enforce safety constraints.\n"
        "Stage 5 executes the decision and targets opponents using our threat-weighted anti-snowball heuristic."
    )

    # =========================================================================
    # SLIDE 4: 18-DIMENSIONAL STATE VECTOR (4 Categorized Group Cards)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_page_bg(slide4)
    add_top_bar(slide4, "Feature Engineering: 18-Dimensional State Space (s in R^18)")

    f_groups = [
        ("Health & Combat State (4-D)", [
            ("my_hp / 5.0", "Agent normalized health"),
            ("opp_hp / 5.0", "Target opponent health"),
            ("is_lethal", "Boolean: target HP <= current dmg"),
            ("rounds_rem / 8.0", "Chamber capacity ratio remaining"),
        ], ACCENT_GREEN),
        ("Bayesian Chamber Belief (4-D)", [
            ("p_live", "Calculated probability next round is LIVE"),
            ("p_blank", "Calculated probability next round is BLANK"),
            ("is_live_certain", "1.0 if round is 100% confirmed live"),
            ("is_blank_certain", "1.0 if round is 100% confirmed blank"),
        ], ACCENT_BLUE),
        ("Inventory & Upgrades (6-D)", [
            ("my_juice / 3.0", "Inventory of healing juice"),
            ("my_mag / 2.0", "Inventory of magnifying glasses"),
            ("my_saw / 3.0", "Inventory of hand saws"),
            ("my_floatie / 2.0", "Inventory of pool floaties"),
            ("my_coffee / 2.0", "Inventory of coffee items"),
            ("saw_stacked / 3.0", "Active accumulated damage bonus"),
        ], ACCENT_AMBER),
        ("Opponent & Table Threat (4-D)", [
            ("opp_has_floatie", "Target already pinned with pending skip"),
            ("opp_mag / 2.0", "Opponent vision capability index"),
            ("opp_saw / 2.0", "Opponent burst lethality capability"),
            ("alive_players / 4.0", "Multi-agent vs duel phase indicator"),
        ], ACCENT_TEAL),
    ]

    for i, (gtitle, gitems, col) in enumerate(f_groups):
        g_left = Inches(0.8 + (i % 2) * 5.95)
        g_top = Inches(1.6 + (i // 2) * 2.7)
        add_panel(slide4, g_left, g_top, Inches(5.75), Inches(2.5), bg=CARD_WHITE, border=col, border_width=1.2)

        tb = slide4.shapes.add_textbox(g_left + Inches(0.2), g_top + Inches(0.18), Inches(5.35), Inches(2.15))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = gtitle
        p_t.font.name = "Arial"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        for item_name, item_desc in gitems:
            p_i = tf.add_paragraph()
            p_i.text = f"• {item_name}: "
            p_i.font.name = "Courier New"
            p_i.font.size = Pt(10)
            p_i.font.bold = True
            p_i.font.color.rgb = HEADER_TEXT
            p_i.text += item_desc

    slide4.notes_slide.notes_text_frame.text = (
        "A critical strength of our RL model is the input representation. We designed an 18-dimensional feature vector grouped into 4 distinct quadrants:\n\n"
        "1. HP metrics: Allows the network to recognize kill windows when is_lethal is triggered.\n"
        "2. Bayesian Belief: Derived from shell counting. If 3 lives and 1 blank remain, p_live is 0.75. When Mag Glass is used or a blank is shot, is_live_certain or is_blank_certain becomes 1.0.\n"
        "3. Inventory metrics: Quantifies available resources for healing, burst, and information.\n"
        "4. Opponent Threat & Arena phase: Captures whether the game is a 1v1 duel or a 4-player brawl, dynamically altering the value of turn denial and health conservation."
    )

    # =========================================================================
    # SLIDE 5: RL TRAINING & CONVERGENCE (Includes Loss Curve Image)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_page_bg(slide5)
    add_top_bar(slide5, "Training Methodology & Bellman Loss Convergence")

    # Left: Loss Curve Image + Stats
    add_panel(slide5, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.3), bg=CARD_WHITE, border=ACCENT_BLUE)
    if os.path.exists("charts/loss_curve.png"):
        slide5.shapes.add_picture("charts/loss_curve.png", Inches(0.9), Inches(1.75), Inches(5.5), Inches(3.2))

    tb_ls = slide5.shapes.add_textbox(Inches(1.05), Inches(5.05), Inches(5.2), Inches(1.7))
    tf_ls = tb_ls.text_frame
    tf_ls.word_wrap = True
    p_ls = tf_ls.paragraphs[0]
    p_ls.text = "Convergence Summary: Huber loss fell from 2.98868 to 0.22601 over 30 epochs across 185,706 transition rollouts, proving stable Q-value convergence."
    p_ls.font.name = "Arial"
    p_ls.font.size = Pt(10.5)
    p_ls.font.color.rgb = BODY_TEXT

    # Right: Reward Shaping Matrix Table
    add_panel(slide5, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.3), bg=CARD_WHITE, border=ACCENT_AMBER)
    tb_rw = slide5.shapes.add_textbox(Inches(7.05), Inches(1.8), Inches(5.2), Inches(4.9))
    tf_rw = tb_rw.text_frame
    tf_rw.word_wrap = True

    p_rh = tf_rw.paragraphs[0]
    p_rh.text = "Potential-Based Reward Shaping Matrix"
    p_rh.font.name = "Arial"
    p_rh.font.size = Pt(15)
    p_rh.font.bold = True
    p_rh.font.color.rgb = ACCENT_AMBER

    rewards_list = [
        ("+15.0 pts", "Match Victory / Tournament Win", ACCENT_GREEN),
        ("+ 5.0 pts", "Opponent Elimination Bonus", ACCENT_GREEN),
        ("+ 3.0 × D", "Damage Dealt to Opponent", ACCENT_BLUE),
        ("+ 4.0 pts", "Blank Self-Shot (Free Extra Turn)", ACCENT_TEAL),
        ("+ 2.5 pts", "Turn Denial (Successful Pool Floatie)", ACCENT_TEAL),
        ("+ 2.0 pts", "Valid Heal (Juice) / Peek (Mag Glass)", ACCENT_BLUE),
        ("- 2.5 × D", "Damage Taken from Opponents", RGBColor(220, 38, 38)),
        ("-10.0 pts", "Live Self-Shot Misplay Penalty", RGBColor(220, 38, 38)),
        ("-12.0 pts", "Elimination / Defeat Penalty", RGBColor(220, 38, 38)),
    ]
    for val, lbl, col in rewards_list:
        p_r = tf_rw.add_paragraph()
        p_r.text = f"{val:10s}  →  {lbl}"
        p_r.font.name = "Courier New"
        p_r.font.size = Pt(10.5)
        p_r.font.bold = True
        p_r.font.color.rgb = col

    slide5.notes_slide.notes_text_frame.text = (
        "To train the Deep Q-Network, we built an offline simulator that generated 3,000 matches, yielding 185,706 transition tuples.\n\n"
        "We used the Bellman Optimality Equation: Q(s, a) = r + gamma * max_a' Q(s', a').\n"
        "To steer learning effectively, we designed a Potential-Based Reward Shaping scheme shown on the right. Large positive rewards are granted for match victory (+15), eliminations (+5), and free consecutive turns (+4). Strict penalties are applied for misplays, especially shooting oneself with a live round (-10).\n\n"
        "Using Smooth L1 loss and Adam, our Huber Bellman loss dropped from 2.988 down to 0.226 over 30 epochs, producing a stable, convergent policy."
    )

    # =========================================================================
    # SLIDE 6: GAME-THEORETIC INNOVATIONS (2x2 Grid)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_page_bg(slide6)
    add_top_bar(slide6, "Strategic Innovations: Overcoming Multi-Agent Hazards")

    tactics_data = [
        ("Threat-Weighted Anti-Snowball Targeting",
         "The Kingmaker Problem: In 4-player games, naive focus-fire attacks the lowest-HP bot, allowing healthy leaders to free-ride. Team CyberCore targets lethal foes first, then attacks the highest-HP leader holding burst items (hand_saw*3 + floatie*2), maintaining table balance.",
         ACCENT_AMBER),
        ("Smart Floatie Turn-Denial Logic",
         "The Wasted Floatie Trap: If an opponent is confirmed to die on the current turn from a live shell, pinning them is wasted. CyberCore skips doomed targets and freezes the next surviving threat in turn order, guaranteeing an enemy turn-skip.",
         ACCENT_BLUE),
        ("Balanced Apex Draft Priority",
         "Utility Diversity: Rather than hoarding only juice, our policy drafts a complete arsenal: (1) Survival (maintain >= 2 Juice), (2) Vision (1-2 Mag Glass), (3) Burst (2 Hand Saws), (4) Control (1 Floatie), and (5) Hoard remaining Juice to starve enemies.",
         ACCENT_TEAL),
        ("Zero-Gamble Shooting Invariant",
         "Risk Minimization: The agent never gambles its life on probability. It shoots self if and only if p_blank == 1.0 (100% mathematically proven free turn). In all uncertain or live states, it directs fire at the opponent.",
         ACCENT_GREEN),
    ]

    for i, (t_title, t_desc, col) in enumerate(tactics_data):
        c_left = Inches(0.8 + (i % 2) * 5.95)
        c_top = Inches(1.6 + (i // 2) * 2.7)
        add_panel(slide6, c_left, c_top, Inches(5.75), Inches(2.5), bg=CARD_WHITE, border=col, border_width=1.2)

        tb = slide6.shapes.add_textbox(c_left + Inches(0.2), c_top + Inches(0.18), Inches(5.35), Inches(2.15))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = t_title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        p_d = tf.add_paragraph()
        p_d.text = t_desc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = BODY_TEXT

    slide6.notes_slide.notes_text_frame.text = (
        "Raw reinforcement learning alone can be vulnerable to local optima in multi-agent environments. We augmented our DQN with four key game-theoretic innovations:\n\n"
        "1. Threat-Weighted Anti-Snowball Targeting: When all bots target the lowest-HP player, Seat 3 or high-HP players get a free pass to victory. By attacking the highest-HP opponent holding lethal weapons, our bot suppresses the table leader and prevents snowballing.\n"
        "2. Smart Floatie: Prevents wasting turn-denial items on enemies who will die on the current turn anyway.\n"
        "3. Balanced Apex Draft: Ensures our inventory has a complete toolkit—vision, lethality, turn denial, and healing.\n"
        "4. Zero-Gamble Shooting: Never gamble with your life. Shoot self only when blank is 100% mathematically proven."
    )

    # =========================================================================
    # SLIDE 7: EMPIRICAL BENCHMARKS (Leaderboard Table + Embedded Charts)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_page_bg(slide7)
    add_top_bar(slide7, "Benchmark Verification: Official Tournament Leaderboard")

    # Table on top
    table_shape = slide7.shapes.add_table(5, 7, Inches(0.8), Inches(1.5), Inches(11.733), Inches(2.3))
    table = table_shape.table

    widths = [Inches(1.2), Inches(2.5), Inches(1.5), Inches(1.8), Inches(1.8), Inches(1.4), Inches(1.533)]
    for idx, w in enumerate(widths):
        table.columns[idx].width = w

    headers = ["Rank", "Submission", "Matches", "Win Rate", "Avg Points", "Faults", "Disqualified"]
    data = [
        ["🥇 #1", "my_bot (CyberCore)", "120", "42.50%", "+0.3500", "0", "0"],
        ["🥈 #2", "smart_bot", "120", "21.67%", "+0.1667", "0", "0"],
        ["🥉 #3", "random_bot", "120", "25.00%", "-0.0333", "0", "0"],
        ["4", "test_bot", "120", "10.83%", "-0.4833", "0", "0"],
    ]

    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = HEADER_TEXT

    for row_idx, row in enumerate(data):
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(254, 243, 199) if row_idx == 0 else CARD_WHITE
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.font.name = "Arial"
            p.font.size = Pt(10.5)
            p.font.bold = (row_idx == 0)
            p.font.color.rgb = ACCENT_AMBER if (row_idx == 0 and col_idx in (0, 1, 3, 4)) else HEADER_TEXT

    # 2 Charts Side by Side below Table
    if os.path.exists("charts/tournament_benchmark.png"):
        slide7.shapes.add_picture("charts/tournament_benchmark.png", Inches(0.8), Inches(4.0), Inches(5.7), Inches(3.0))

    if os.path.exists("charts/win_rate_benchmark.png"):
        slide7.shapes.add_picture("charts/win_rate_benchmark.png", Inches(6.8), Inches(4.0), Inches(5.733), Inches(3.0))

    slide7.notes_slide.notes_text_frame.text = (
        "This slide presents our official empirical benchmark results evaluated by the organizers' engine.\n\n"
        "We tested all bots across 120 matches representing every possible seating permutation and random seed. The official scoring metric ranks bots by average placement points:\n"
        "• Our bot captured Rank #1 with +0.3500 average points and a 42.50% win rate in 4-player Battle Royale.\n"
        "• Notice that random_bot and test_bot achieved negative scores (-0.0333 and -0.4833).\n"
        "• In 1v1 duels, our bot achieved an 87% win rate against random bots and 73.3% against smart bots.\n"
        "• Crucially, we registered 0 faults, 0 disqualifications, and 0 timeouts."
    )

    # =========================================================================
    # SLIDE 8: SUMMARY & TEAM CYBERCORE Q&A
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_page_bg(slide8)
    add_top_bar(slide8, "Conclusion: Deliverables, Engineering Rigor & Q&A")

    col_boxes = [
        ("Engineering Rigor", [
            ("Execution Speed", "0.02s match time out of 0.50s budget (25x safety margin)."),
            ("Decision Latency", "< 0.001s per decision against the 0.05s timeout limit."),
            ("Memory Compliance", "< 30 MB utilized against the 128 MB RAM ceiling."),
            ("Standard Library", "Zero external runtime dependencies in Docker container."),
        ], ACCENT_GREEN),
        ("Deliverables & Verification", [
            ("GitHub Repository", "Publicly hosted at github.com/viswakpullepu/cses-buckshot-roulette-rl."),
            ("Google Drive Bundle", "Complete submission package with bot.py, model_weights.json, and docs."),
            ("Clean Engine Validation", "Engine validator reports 'OK' with 0 faults and 0 disqualifications."),
            ("Model Footprint", "Compact 65 KB JSON weights loaded instantaneously."),
        ], ACCENT_BLUE),
        ("Team CyberCore", [
            ("Team Name", "CyberCore"),
            ("Participants", "Vishwak Naidu & Dhivija"),
            ("Institution", "NIT Warangal Technozion '26"),
            ("Status", "Rank #1 Tournament Champion"),
            ("Open for Q&A", "We look forward to questions and technical defense!"),
        ], ACCENT_AMBER),
    ]

    for i, (title, items, col) in enumerate(col_boxes):
        c_left = Inches(0.8 + i * 3.98)
        add_panel(slide8, c_left, Inches(1.6), Inches(3.78), Inches(5.3), bg=CARD_WHITE, border=col, border_width=1.2)

        h_box = slide8.shapes.add_textbox(c_left + Inches(0.2), Inches(1.85), Inches(3.38), Inches(0.5))
        p_h = h_box.text_frame.paragraphs[0]
        p_h.text = title
        p_h.font.name = "Arial"
        p_h.font.size = Pt(15)
        p_h.font.bold = True
        p_h.font.color.rgb = col

        b_box = slide8.shapes.add_textbox(c_left + Inches(0.2), Inches(2.4), Inches(3.38), Inches(4.3))
        tf_b = b_box.text_frame
        tf_b.word_wrap = True
        for j, (h_item, d_item) in enumerate(items):
            p_ih = tf_b.add_paragraph() if j > 0 else tf_b.paragraphs[0]
            p_ih.text = f"• {h_item}: "
            p_ih.font.name = "Arial"
            p_ih.font.size = Pt(11)
            p_ih.font.bold = True
            p_ih.font.color.rgb = HEADER_TEXT
            p_ih.text += d_item

    slide8.notes_slide.notes_text_frame.text = (
        "To summarize our submission:\n\n"
        "1. Team CyberCore satisfied every engineering requirement of the competition: standard library only, 25x faster than timeout limits, and zero external dependencies.\n"
        "2. All materials are open, reproducible, and ready for immediate evaluation on GitHub and Google Drive.\n"
        "3. By synthesizing Deep Q-Learning with Bayesian probability and threat-weighted anti-snowball heuristics, we created a resilient agent that dominates multi-player stochastic arenas.\n\n"
        "Thank you. Vishwak Naidu and Dhivija from Team CyberCore are now ready for your questions!"
    )

    prs.save(filename)
    print(f"[PPTX Generator] Successfully built CyberCore deck with images: {filename} ({os.path.getsize(filename)} bytes)")

if __name__ == "__main__":
    build_cybercore_deck()
