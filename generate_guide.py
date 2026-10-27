import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import pypdf

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print 'Page X of Y' on every page,
    with clean headers and footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Top Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 750, "PulseHR: Strategic Talent Analytics & AI Attrition Predictor")
            self.drawRightString(558, 750, "Executive Presentation & Demo Guide")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

        # Bottom Footer (all pages)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Confidential • Prepared for Academic & Stakeholder Presentation")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()


def create_presentation_pdf(output_filename="PulseHR_Presentation_Guide_and_Script.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#1e1b4b")     # Deep Indigo
    SECONDARY = colors.HexColor("#4f46e5")   # Electric Indigo
    TEXT_DARK = colors.HexColor("#0f172a")   # Slate 900
    TEXT_MUTED = colors.HexColor("#475569")  # Slate 600
    BG_LIGHT = colors.HexColor("#f8fafc")    # Slate 50
    ACCENT_GREEN = colors.HexColor("#059669")
    ACCENT_AMBER = colors.HexColor("#d97706")
    ACCENT_ROSE = colors.HexColor("#e11d48")

    # Typography Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=PRIMARY,
        spaceAfter=5
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13.5,
        leading=17,
        textColor=PRIMARY,
        spaceBefore=11,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=12.5,
        textColor=TEXT_DARK,
        spaceAfter=5
    )

    script_speaker_style = ParagraphStyle(
        "ScriptSpeaker",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13.5,
        textColor=SECONDARY,
        spaceBefore=7,
        spaceAfter=2,
        keepWithNext=True
    )

    script_action_style = ParagraphStyle(
        "ScriptAction",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=12,
        textColor=ACCENT_AMBER,
        spaceAfter=2
    )

    script_speech_style = ParagraphStyle(
        "ScriptSpeech",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=12.8,
        textColor=TEXT_DARK,
        leftIndent=10,
        spaceAfter=6
    )

    callout_style = ParagraphStyle(
        "CalloutText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=12.5,
        textColor=TEXT_DARK
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, EXECUTIVE OVERVIEW & CORE TERMINOLOGY
    # =========================================================================
    header_table = Table(
        [[
            Paragraph("<b>PULSEHR SUITE</b> • DEMONSTRATION & PRESENTATION GUIDE", ParagraphStyle("Tag", fontName="Helvetica-Bold", fontSize=8, textColor=colors.HexColor("#4f46e5"))),
        ]],
        colWidths=[504]
    )
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#eef2ff")),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor("#c7d2fe")),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Strategic HR Analytics & Employee Attrition Predictor", title_style))
    story.append(Paragraph("Executive Overview, KPI Metric Explanations, Feature Guide, and Word-for-Word Presenter Script", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#4f46e5"), spaceBefore=0, spaceAfter=10))

    story.append(Paragraph("1. Executive Overview: What is PulseHR & Why Does It Matter?", h1_style))
    story.append(Paragraph(
        "Employee turnover (when employees resign and leave an organization) is among the most costly problems modern companies face. "
        "Replacing a single skilled employee typically costs <b>50% to 200% of their annual salary</b> in recruitment fees, onboarding delays, and lost team momentum. "
        "<b>PulseHR</b> transforms Human Resources from <i>reactive</i> (learning someone is unhappy only during an exit interview) into <i>proactive</i> "
        "(identifying flight risk months ahead and providing managers with targeted retention strategies).",
        body_style
    ))

    overview_box = Table([[
        Paragraph(
            "<b>Key Takeaway for Presenters:</b> PulseHR answers three fundamental business questions:<br/>"
            "1. <b>What is happening right now?</b> (Live Headcount, Attrition Rate %, Average Compensation, Job Satisfaction).<br/>"
            "2. <b>Why are people leaving?</b> (Overtime burnout, compensation disparities, early-tenure turnover).<br/>"
            "3. <b>Who is at risk next, and how do we retain them?</b> (AI predictive flight risk scoring and tailored HR action plans).",
            callout_style
        )
    ]], colWidths=[504])
    overview_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(overview_box)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Essential Terminology Glossary", h1_style))
    story.append(Paragraph("Use these standardized industry terms during your presentation to speak with confidence and clarity:", body_style))

    term_data = [
        [Paragraph("<b>Term</b>", ParagraphStyle("TH", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white)),
         Paragraph("<b>Plain-English Meaning</b>", ParagraphStyle("TH", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white)),
         Paragraph("<b>How It Applies in the Platform</b>", ParagraphStyle("TH", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white))],

        [Paragraph("<b>Attrition Rate (%)</b>", body_style),
         Paragraph("The percentage of the workforce that resigns over a period.", body_style),
         Paragraph("Shown as a primary KPI card (14.2%). Healthy industry benchmarks stay under 15%.", body_style)],

        [Paragraph("<b>Flight Risk</b>", body_style),
         Paragraph("The calculated likelihood (0%–100%) that an employee will leave.", body_style),
         Paragraph("Visualized on the Radial Gauge Meter in Tab 2 and in the 360° Profile Inspector.", body_style)],

        [Paragraph("<b>Tenure</b>", body_style),
         Paragraph("How many years an employee has worked at the company.", body_style),
         Paragraph("Reveals vulnerable turnover zones, particularly during the first 0–2 years.", body_style)],

        [Paragraph("<b>Hygiene vs. Motivator Factors</b>", body_style),
         Paragraph("Herzberg's HRM theory: Hygiene factors (salary, overtime) cause turnover if bad; Motivators (satisfaction, growth) drive retention.", body_style),
         Paragraph("Tested across both dimensions: compensation/overtime (hygiene) and satisfaction score (motivator).", body_style)],

        [Paragraph("<b>Random Forest Classifier</b>", body_style),
         Paragraph("An ensemble AI algorithm combining decision trees to predict flight risk accurately without bias.", body_style),
         Paragraph("Powers the interactive prediction form in Tab 2 with balanced class weighting.", body_style)],

        [Paragraph("<b>Feature Importance</b>", body_style),
         Paragraph("A ranking showing which factors have the highest impact on turnover decisions.", body_style),
         Paragraph("Visualized as a horizontal bar chart, proving OverTime is the #1 churn driver.", body_style)],
    ]

    term_table = Table(term_data, colWidths=[110, 194, 200])
    term_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(term_table)

    # =========================================================================
    # PAGE 2: DEEP DIVE: TOP EXECUTIVE KPI CARDS EXPLAINED
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Deep Dive: Top Executive KPI Cards Explained", h1_style))
    story.append(Paragraph(
        "At the top of the dashboard, five high-visibility metric cards summarize the current organizational health. "
        "Here is what each number represents, why it matters to leadership, and exactly what the presenter should say:",
        body_style
    ))

    kpi_data = [
        [Paragraph("<b>KPI Card</b>", ParagraphStyle("THK", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white)),
         Paragraph("<b>Current Value & Meaning</b>", ParagraphStyle("THK", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white)),
         Paragraph("<b>Strategic Business Importance</b>", ParagraphStyle("THK", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white)),
         Paragraph("<b>What the Presenter Should Say</b>", ParagraphStyle("THK", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white))],

        [Paragraph("<b>👥 Total Headcount</b>", body_style),
         Paragraph("<b>1,200</b><br/><i>(100.0% of org)</i><br/>The total number of employee records currently matching the active filter criteria.", body_style),
         Paragraph("Represents organizational size and statistical sample. Dynamic: if you filter by 'Sales', it automatically reflects the Sales headcount.", body_style),
         Paragraph("<i>\"This card gives us our active headcount baseline—1,200 employees across all divisions. As we filter by department or income, it adjusts in real time.\"</i>", body_style)],

        [Paragraph("<b>📉 Attrition Rate</b>", body_style),
         Paragraph("<b>14.2%</b><br/><i>(171 Exited Staff)</i><br/>The percentage of the total workforce that has resigned or separated.", body_style),
         Paragraph("<b>The #1 HR vital.</b> Industry standard for healthy turnover is under 15%. PulseHR color-codes this card: Green (<12%), Amber (12–20%), Red (>20%).", body_style),
         Paragraph("<i>\"Our current attrition rate is 14.2%, accounting for 171 departures. It is color-coded amber to signal that turnover is near the caution threshold.\"</i>", body_style)],

        [Paragraph("<b>💵 Avg. Monthly Income</b>", body_style),
         Paragraph("<b>$10,982</b><br/><i>(Per Employee / Mo)</i><br/>The mean gross monthly compensation across all roles and experience tiers.", body_style),
         Paragraph("Establishes the internal compensation benchmark. When compared to the lower pay of departed staff in Tab 1, it proves salary disparity drives resignations.", body_style),
         Paragraph("<i>\"Our average monthly compensation stands at $10,982. This acts as our salary baseline to verify whether lower pay is driving talent poaching.\"</i>", body_style)],

        [Paragraph("<b>⭐ Avg. Job Satisfaction</b>", body_style),
         Paragraph("<b>2.54 / 4.0</b><br/><i>(Status: Moderate)</i><br/>Average employee morale score from pulse surveys, rated 1 (Low) to 4 (Very High).", body_style),
         Paragraph("Measures sentiment and engagement. In HR theory, satisfaction is the key motivator factor. When satisfaction drops below 2.0, flight risk skyrockets.", body_style),
         Paragraph("<i>\"Job satisfaction averages 2.54 out of 4, rated as Moderate. In retention theory, satisfaction is the core motivator preventing voluntary exits.\"</i>", body_style)],

        [Paragraph("<b>⏱️ OverTime Load</b>", body_style),
         Paragraph("<b>29.8%</b><br/><i>(Active Overtime Ratio)</i><br/>The proportion of the workforce regularly clocking mandatory or extra hours.", body_style),
         Paragraph("<b>The primary burnout thermometer.</b> When nearly 30% of employees work overtime, chronic fatigue sets in. In our ML model, this is the #1 churn driver.", body_style),
         Paragraph("<i>\"Nearly 30% of our staff is working overtime. This is a critical indicator of workload fatigue and the primary predictor of upcoming turnover.\"</i>", body_style)],
    ]

    kpi_table = Table(kpi_data, colWidths=[85, 125, 135, 159])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Real-Time Dynamic Sidebar Filter Controls", h2_style))
    story.append(Paragraph(
        "On the left sidebar, three controls allow users to slice and dice the workforce: "
        "<b>1. Department</b> (multi-select for R&D, Sales, HR), "
        "<b>2. OverTime Commitment</b> (segmented toggle: All Staff, Overtime Only, Standard Hours), and "
        "<b>3. Monthly Income Slider</b> (dynamic range). Clicking <b>'↺ Reset All Filters'</b> instantly restores the full organization view.",
        body_style
    ))

    # =========================================================================
    # PAGE 3: THE THREE MAIN FUNCTIONAL TABS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Step-by-Step Feature Walkthrough: The Three Functional Tabs", h1_style))
    story.append(Paragraph("PulseHR divides workforce analysis into three focused operational views:", body_style))

    tab_data = [
        [Paragraph("<b>Tab View</b>", ParagraphStyle("THT", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white)),
         Paragraph("<b>Visual Elements & Charts</b>", ParagraphStyle("THT", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white)),
         Paragraph("<b>What It Tells the Presenter & Audience</b>", ParagraphStyle("THT", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white))],

        [Paragraph("<b>📊 Tab 1:<br/>Workforce Insights & Analytics</b>", body_style),
         Paragraph("• <b>Departmental Attrition:</b> Grouped bar chart comparing active vs exited staff.<br/>"
                   "• <b>Monthly Income Box Plot:</b> Shows salary distribution and median income gap between stayers and leavers.<br/>"
                   "• <b>Job Satisfaction Bar:</b> Turnover percentage across satisfaction tiers 1 to 4.<br/>"
                   "• <b>Tenure vs. Overtime Scatter:</b> Correlates company years, salary, and overtime.<br/>"
                   "• <b>HRM Takeaways Callout:</b> Summarizes macro-level retention insights.", body_style),
         Paragraph("Provides the <b>macro-level 'Why'</b>. Proves statistically that: (1) departed employees had significantly lower median incomes, (2) turnover peaks in years 0–2 (early tenure churn), and (3) employees on overtime experience twice the turnover rate of standard-hour workers.", body_style)],

        [Paragraph("<b>🎯 Tab 2:<br/>Attrition Risk Predictor (ML)</b>", body_style),
         Paragraph("• <b>Employee Profile Simulation Form:</b> Sliders for Age, Tenure, Overtime toggle, Monthly Income, and Satisfaction.<br/>"
                   "• <b>Radial Gauge Meter:</b> Displays exact probability score (0% to 100%).<br/>"
                   "• <b>Risk Badges:</b> Low (<30%, Green), Moderate (30–60%, Amber), High (>60%, Red).<br/>"
                   "• <b>Feature Importance Chart:</b> Ranks top churn drivers.<br/>"
                   "• <b>Actionable Retention Interventions:</b> Contextual management playbooks.", body_style),
         Paragraph("Provides the <b>predictive 'Who & What to do'</b>. Simulates any employee's flight risk on the fly. Rather than just giving a score, it provides specific retention actions (e.g. rebalance overtime, schedule skip-level 1-on-1, benchmark compensation, assign mentor).", body_style)],

        [Paragraph("<b>📁 Tab 3:<br/>Employee Records & Search</b>", body_style),
         Paragraph("• <b>Universal Search Bar:</b> Instant query across Employee ID, Job Role, and Department.<br/>"
                   "• <b>Talent Facets:</b> Filter by Attrition status, Job Role, Satisfaction, Tenure.<br/>"
                   "• <b>Multi-Column Sorting:</b> Sort by Income, Tenure, Morale, Age, ID.<br/>"
                   "• <b>Live Cohort KPIs:</b> Summary metrics for the filtered group.<br/>"
                   "• <b>Individual 360° Profile Inspector:</b> Pulls up full file and calculates real-time ML risk.<br/>"
                   "• <b>CSV Export:</b> One-click audit report download.", body_style),
         Paragraph("Provides the <b>operational execution tool</b> for HR managers. Allows looking up specific individuals or cohorts (e.g. all R&D engineers with low satisfaction) and downloading clean CSV reports for leadership meetings.", body_style)],
    ]

    tab_table = Table(tab_data, colWidths=[110, 204, 190])
    tab_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(tab_table)

    # =========================================================================
    # PAGE 4: WORD-FOR-WORD PRESENTER SCRIPT (5-MINUTE DEMO FLOW)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("5. Word-for-Word Presenter Script (5-Minute Demonstration Flow)", h1_style))
    story.append(Paragraph("Use this exact script during live presentations or video demos. Pair each spoken line with the screen action:", body_style))

    # Step 1
    story.append(Paragraph("Step 1: The Hook & Introduction [0:00 - 0:45]", script_speaker_style))
    story.append(Paragraph("<b>Action on Screen:</b> Stand on the main dashboard showing the Hero Banner and Top KPI cards.", script_action_style))
    story.append(Paragraph(
        "<i>\"Hello everyone. Today, I'm presenting <b>PulseHR</b>, a modern Talent Analytics and Attrition Predictor platform.<br/>"
        "In business, employee turnover is an expensive crisis—replacing a talented staff member costs between 50% and 200% of their salary in recruitment fees, "
        "training delays, and lost productivity. Most companies only learn an employee is unhappy during their exit interview—when it is already too late. "
        "PulseHR changes this: it moves HR from <b>reactive firefighting</b> to <b>proactive retention</b> using analytics and machine learning.\"</i>",
        script_speech_style
    ))

    # Step 2
    story.append(Paragraph("Step 2: Executive Health KPIs & Live Dynamic Filters [0:45 - 1:45]", script_speaker_style))
    story.append(Paragraph("<b>Action on Screen:</b> Point out the 5 KPI cards. Then adjust the sidebar Department filter and Monthly Income slider.", script_action_style))
    story.append(Paragraph(
        "<i>\"At the top of our dashboard, we see five key organizational vitals: a Total Headcount of 1,200 employees, an overall Attrition Rate of 14.2% "
        "(representing 171 departures), an average monthly salary of $10,982, average job satisfaction of 2.54 out of 4, and an OverTime load of 29.8%.<br/>"
        "On the left sidebar, we have dynamic filter controls. Watch what happens when I filter down to the <b>Sales</b> department and adjust our salary slider. "
        "Every single metric card, chart, and data record on the dashboard recalculates instantly. This lets leadership evaluate specific departments or salary bands in seconds.\"</i>",
        script_speech_style
    ))

    # Step 3
    story.append(Paragraph("Step 3: Deep Workforce Insights (Tab 1) [1:45 - 2:45]", script_speaker_style))
    story.append(Paragraph("<b>Action on Screen:</b> Click Tab 1: 'Workforce Insights & Analytics'. Point to the box plot and the overtime scatter plot.", script_action_style))
    story.append(Paragraph(
        "<i>\"In our <b>Workforce Insights</b> tab, we explore <b>why</b> people leave.<br/>"
        "Looking at our Monthly Income Box Plot, we observe a noticeable compensation gap: employees who left earned significantly lower median wages than those who stayed, "
        "confirming that salary competitiveness is critical.<br/>"
        "Next, looking at our Tenure versus Overtime scatter plot, we discover two vital patterns: turnover peaks during the first 0 to 2 years—known as early-career churn—and "
        "employees on overtime experience nearly double the turnover rate of standard-hour workers, proving that chronic burnout drives resignations.\"</i>",
        script_speech_style
    ))

    # Step 4
    story.append(Paragraph("Step 4: Live AI Attrition Risk Predictor Demo (Tab 2) [2:45 - 4:00]", script_speaker_style))
    story.append(Paragraph("<b>Action on Screen:</b> Click Tab 2. In the form, set Age=32, Tenure=2, OverTime=Yes, Monthly Income=$4,200, Satisfaction=Low (1). Click 'Predict Attrition Risk'.", script_action_style))
    story.append(Paragraph(
        "<i>\"Now let's examine our most powerful feature: the <b>Attrition Risk Predictor</b> powered by a machine-learning Random Forest model.<br/>"
        "Imagine an HR manager wants to evaluate a 32-year-old engineer who has been with us for 2 years, earns $4,200 a month, works overtime, and reported low satisfaction.<br/>"
        "I'll click <b>'Predict Attrition Risk'</b>... and instantly, our AI calculates an <b>81% Flight Risk (High Risk Tier)</b> on the radial gauge.<br/>"
        "Crucially, PulseHR doesn't just deliver a number; it provides <b>Actionable Retention Interventions</b>. The system recommends: workload rebalancing to mitigate overtime burnout, "
        "a structured 1-on-1 skip-level meeting to address sentiment, and a salary parity review. This gives managers a precise playbook to retain that talent before they submit their notice.\"</i>",
        script_speech_style
    ))

    # Step 5
    story.append(Paragraph("Step 5: Talent Search, 360° Profile & CSV Export (Tab 3) [4:00 - 5:00]", script_speaker_style))
    story.append(Paragraph("<b>Action on Screen:</b> Click Tab 3. Type 'Research' in the search bar. Open 'Inspect Individual Employee 360° Profile'. Point to 'Export Searched Cohort to CSV'.", script_action_style))
    story.append(Paragraph(
        "<i>\"Finally, in Tab 3, we have our <b>Employee Directory & Advanced Talent Search</b>.<br/>"
        "HR managers can use our universal search bar or filter facets to isolate cohorts—such as employees with low satisfaction. "
        "Above the table, live Cohort KPI cards calculate the exact average salary and turnover rate of the searched group.<br/>"
        "We can also open the <b>Individual Employee 360° Profile Inspector</b> to review any team member's full compensation and real-time flight risk score.<br/>"
        "And with one click on <b>'Export Searched Cohort to CSV'</b>, HR can download a clean report for executive meetings.\"</i>",
        script_speech_style
    ))

    # Closing
    story.append(Paragraph("Closing & Q&A Readiness [5:00 - 5:30]", script_speaker_style))
    story.append(Paragraph(
        "<i>\"In summary, PulseHR bridges data science and human capital management to protect an organization's most valuable asset—its people. "
        "Thank you, and I look forward to your questions!\"</i>",
        script_speech_style
    ))

    # =========================================================================
    # SECTION 6: ANTICIPATED QUESTIONS & WINNING ANSWERS
    # =========================================================================
    story.append(Spacer(1, 14))
    story.append(Paragraph("6. Anticipated Questions & Winning Answers for the Presenter", h1_style))
    story.append(Paragraph("Be prepared for these common questions from professors, interviewers, or managers:", body_style))

    qa_data = [
        [Paragraph("<b>Question</b>", ParagraphStyle("THQA", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white)),
         Paragraph("<b>Recommended Winning Answer</b>", ParagraphStyle("THQA", fontName="Helvetica-Bold", fontSize=8.5, textColor=colors.white))],

        [Paragraph("<b>\"Where does the employee dataset come from?\"</b>", body_style),
         Paragraph("<i>\"The data is statistically generated using NumPy with a fixed random seed. It mirrors the realistic distributions of standard industry benchmarks (like the IBM HR Analytics dataset), incorporating realistic correlations like overtime stress and early-tenure turnover.\"</i>", body_style)],

        [Paragraph("<b>\"How does the Machine Learning model calculate flight risk?\"</b>", body_style),
         Paragraph("<i>\"We train a Random Forest Classifier with balanced class weights using Scikit-Learn. It evaluates key features—Overtime, Monthly Income, Job Satisfaction, Age, and Company Tenure—and generates a calibrated probability score (0% to 100%) indicating how closely the employee matches historical departure patterns.\"</i>", body_style)],

        [Paragraph("<b>\"Why is OverTime the strongest predictor of attrition?\"</b>", body_style),
         Paragraph("<i>\"In HRM organizational psychology, sustained overtime leads directly to work-life conflict and burnout. In our feature importance ranking, Overtime emerged as the single highest-weighted flight risk driver, proving that compensation alone cannot offset chronic workload fatigue.\"</i>", body_style)],

        [Paragraph("<b>\"Why does attrition peak in the first 0 to 2 years of tenure?\"</b>", body_style),
         Paragraph("<i>\"This reflects early-career onboarding vulnerability. New hires who experience poor onboarding, unclear expectations, or role misalignment will quickly look for opportunities elsewhere. After year 3, employees typically form stronger organizational ties.\"</i>", body_style)],

        [Paragraph("<b>\"How would a real-world enterprise integrate PulseHR?\"</b>", body_style),
         Paragraph("<i>\"In a live corporate environment, PulseHR connects directly to HR Information Systems (HRIS) like Workday, BambooHR, or SAP SuccessFactors via API. It runs quarterly retention scans and alerts department heads when high-performing staff enter high-risk flight zones.\"</i>", body_style)],
    ]

    qa_table = Table(qa_data, colWidths=[150, 354])
    qa_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(qa_table)

    # Build Document using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated: {output_filename}")

if __name__ == "__main__":
    create_presentation_pdf()
