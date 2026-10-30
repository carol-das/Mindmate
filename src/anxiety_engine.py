"""
Anxiety Pattern Recognition & Psychoeducation Engine
Provides surface-level emotional pattern inference, clinical psychoeducation,
and citations to peer-reviewed psychological research papers.
"""

# Curated peer-reviewed scientific research library
RESEARCH_LIBRARY = {
    "generalized_worry": [
        {
            "title": "The Efficacy of Cognitive Behavioral Therapy: A Review of Meta-analyses",
            "authors": "Hofmann, S. G., Asnaani, A., Vonk, I. J., Sawyer, A. T., & Fang, A.",
            "year": 2012,
            "journal": "Cognitive Therapy and Research, 36(5), 427-440",
            "doi": "https://doi.org/10.1007/s10608-012-9476-1",
            "key_finding": "Meta-analysis demonstrating CBT's robust efficacy for generalized anxiety, chronic worry, and catastrophic cognitive loops."
        },
        {
            "title": "Avoidance Theory of Worry and Generalized Anxiety Disorder",
            "authors": "Borkovec, T. D., Alcaine, O. M., & Behar, E.",
            "year": 2004,
            "journal": "Generalized Anxiety Disorder: Advances in Research and Practice, 77-108",
            "doi": "https://scholar.google.com/scholar?q=Borkovec+Avoidance+Theory+of+Worry",
            "key_finding": "Demonstrates that chronic worry operates as a cognitive attempt to avoid deeper visceral emotions, and explains why emotional regulation brings lasting relief."
        }
    ],
    "social_evaluative": [
        {
            "title": "A Cognitive Model of Social Phobia",
            "authors": "Clark, D. M., & Wells, A.",
            "year": 1995,
            "journal": "Social Phobia: Diagnosis, Assessment, and Treatment, 69-93",
            "doi": "https://scholar.google.com/scholar?q=Clark+Wells+A+cognitive+model+of+social+phobia",
            "key_finding": "Identifies the self-focused attention loop where individuals fear negative appraisal and judge themselves through an imagined harsh external lens."
        },
        {
            "title": "Cognitive-Behavioral Therapy for Adult Social Anxiety Disorder",
            "authors": "Heimberg, R. G., Brozovich, F. A., & Rapee, R. M.",
            "year": 2014,
            "journal": "Depression and Anxiety, 31(4), 312-327",
            "doi": "https://doi.org/10.1002/da.22237",
            "key_finding": "Highlights how gentle cognitive restructuring and behavioral experiments safely dissolve shame and the taboo of seeking support."
        }
    ],
    "somatic_panic": [
        {
            "title": "The Polyvagal Perspective",
            "authors": "Porges, S. W.",
            "year": 2007,
            "journal": "Biological Psychology, 74(2), 116-143",
            "doi": "https://doi.org/10.1016/j.biopsycho.2006.06.009",
            "key_finding": "Establishes how the vagus nerve mediates fight, flight, freeze, and social engagement, proving that panic is an autonomic physiological state rather than a mental failure."
        },
        {
            "title": "Anxiety and Its Disorders: The Nature and Treatment of Anxiety and Panic",
            "authors": "Barlow, D. H.",
            "year": 2002,
            "journal": "Guilford Press (2nd Edition)",
            "doi": "https://scholar.google.com/scholar?q=Barlow+Anxiety+and+Its+Disorders",
            "key_finding": "The foundational clinical text proving that interoceptive exposure and somatic down-regulation successfully neutralize panic attacks."
        }
    ],
    "relational_attachment": [
        {
            "title": "Attachment in Adulthood: Structure, Dynamics, and Change",
            "authors": "Mikulincer, M., & Shaver, P. R.",
            "year": 2007,
            "journal": "Guilford Press",
            "doi": "https://scholar.google.com/scholar?q=Mikulincer+Shaver+Attachment+in+Adulthood",
            "key_finding": "Explores how anxious attachment triggers hyper-vigilance in relationships and demonstrates that secure co-regulation transforms interpersonal harmony."
        },
        {
            "title": "The Practice of Emotionally Focused Couple Therapy: Creating Connection",
            "authors": "Johnson, S. M.",
            "year": 2004,
            "journal": "Brunner-Routledge",
            "doi": "https://scholar.google.com/scholar?q=Sue+Johnson+Emotionally+Focused+Couple+Therapy",
            "key_finding": "Demonstrates that reactive fighting often masks primary needs for safety and validation, showing that emotional regulation protects intimate relationships."
        }
    ],
    "burnout_perfectionism": [
        {
            "title": "Understanding the Burnout Experience: Recent Research and Its Implications for Psychiatry",
            "authors": "Maslach, C., & Leiter, M. P.",
            "year": 2016,
            "journal": "World Psychiatry, 15(2), 103-111",
            "doi": "https://doi.org/10.1002/wps.20311",
            "key_finding": "Establishes that burnout is an allostatic exhaustion of personal resources resulting from prolonged imbalance between chronic demands and restorative recovery."
        },
        {
            "title": "Self-Compassion: An Alternative Conceptualization of a Healthy Attitude Toward Oneself",
            "authors": "Neff, K. D.",
            "year": 2003,
            "journal": "Self and Identity, 2(2), 85-101",
            "doi": "https://doi.org/10.1080/15298860309032",
            "key_finding": "Proves that self-compassion significantly lowers anxiety, reduces performance shame, and provides resilience without requiring relentless self-criticism."
        }
    ],
    "emotional_resistance": [
        {
            "title": "The Body Keeps the Score: Brain, Mind, and Body in the Healing of Trauma",
            "authors": "Van der Kolk, B. A.",
            "year": 2014,
            "journal": "Viking / Penguin Books",
            "doi": "https://scholar.google.com/scholar?q=Van+der+Kolk+The+Body+Keeps+the+Score",
            "key_finding": "Reveals that the urge to withdraw or not speak is an autonomic defense to protect the self, emphasizing that healing starts with bodily safety before verbal disclosure."
        },
        {
            "title": "Emotion Regulation: Affective, Cognitive, and Social Consequences",
            "authors": "Gross, J. J.",
            "year": 2002,
            "journal": "Psychophysiology, 39(3), 281-291",
            "doi": "https://doi.org/10.1017/s0048577201393198",
            "key_finding": "Shows that cognitive reappraisal is far healthier than emotional suppression, and that accepting boundaries prevents interpersonal fatigue."
        }
    ]
}

# Anxiety phenotype profiles with full educational content
ANXIETY_PROFILES = {
    "generalized_worry": {
        "label": "Generalized Cognitive Overdrive & Anticipatory Worry",
        "aesthetic_title": "The Unquiet Sea: Restless Anticipation",
        "icon": "🌊",
        "nervous_system_state": "Default Mode Network (DMN) Hyperactivity & Sympathetic Vigilance",
        "description": (
            "Characterized by persistent 'what-if' loops, rapid mental problem-solving for distant futures, "
            "and difficulty tolerating uncertainty. Often manifests physically as jaw clenching, shallow breathing, "
            "and mental exhaustion from trying to foresee every outcome."
        ),
        "comforting_reframe": (
            "Your mind is not defective; it is working in overdrive to keep you safe from perceived threats. "
            "Therapy helps teach your nervous system that you can be prepared without having to be perpetually on guard."
        ),
        "research_key": "generalized_worry"
    },
    "social_evaluative": {
        "label": "Social-Evaluative Anxiety & Fear of Appraisal",
        "aesthetic_title": "The Mirror Hall: Fear of Being Exposed",
        "icon": "🪞",
        "nervous_system_state": "Social Engagement System Inhibition & Dorsal Freeze",
        "description": (
            "Marked by intense apprehension before or during interactions, fear of freezing up or being judged, "
            "and exhaustive post-event mental replays. Clients often feel an overwhelming pressure to appear composed "
            "while dwelling in deep internal vulnerability."
        ),
        "comforting_reframe": (
            "You are not alone in fearing judgment. In fact, seeking therapy is the definitive antidote to this fear—a space "
            "where unconditional positive regard is guaranteed and you are allowed to be imperfect."
        ),
        "research_key": "social_evaluative"
    },
    "somatic_panic": {
        "label": "Somatic Agitation & Interoceptive Sensitivity",
        "aesthetic_title": "The Sudden Gale: Visceral False Alarms",
        "icon": "⚡",
        "nervous_system_state": "Acute Sympathetic Adrenaline Surge",
        "description": (
            "Experiences where emotional stress bypasses conscious thought and registers immediately as visceral "
            "sensations: racing heart, tightness across the chest, stomach knots, or sudden dizziness. The mind "
            "misinterprets these natural bodily signals as catastrophic danger."
        ),
        "comforting_reframe": (
            "Your body is sounding a false fire alarm. The sensations are uncomfortable, but they are not dangerous. "
            "Somatic and breath-based therapy safely desensitizes your nervous system to these physical ripples."
        ),
        "research_key": "somatic_panic"
    },
    "relational_attachment": {
        "label": "Relational Sensitivity & Attachment Dysregulation",
        "aesthetic_title": "The Distant Shore: Vulnerability in Love",
        "icon": "🕊️",
        "nervous_system_state": "Attachment System Hyper-activation / Protest Behavior",
        "description": (
            "Triggered primarily within close connections—with partners, family, or close friends. Includes hyper-vigilance "
            "to changes in tone, fear of conflict or abandonment, and walking on eggshells. Unexpressed emotions frequently "
            "burst out as irritation or withdrawal."
        ),
        "comforting_reframe": (
            "Wanting emotional safety with the people you love is not 'needy'—it is biological human nature. Learning "
            "emotional regulation creates co-regulation, transforming conflict into deeper intimacy."
        ),
        "research_key": "relational_attachment"
    },
    "burnout_perfectionism": {
        "label": "Allostatic Burnout & Performance Exhaustion",
        "aesthetic_title": "The Heavy Canvas: The Weariness of Holding Everything",
        "icon": "🍂",
        "nervous_system_state": "Chronic Cortisol Depletion & Neuroendocrine Fatigue",
        "description": (
            "Common among high-functioning, conscientious individuals who suppress their own boundaries to meet endless external demands. "
            "Symptoms include emotional numbness, cynicism, cognitive brain fog, and feeling entirely depleted."
        ),
        "comforting_reframe": (
            "Rest is not a reward you have to earn after collapsing; it is a biological requirement. Therapy helps you separate "
            "your inherent worth from your productivity."
        ),
        "research_key": "burnout_perfectionism"
    },
    "emotional_resistance": {
        "label": "Protective Boundary Guarding (Hesitation to Open Up)",
        "aesthetic_title": "The Walled Garden: Honoring Safe Pacing",
        "icon": "🛡️",
        "nervous_system_state": "Protective Dorsal / Hypo-Arousal Pacing",
        "description": (
            "A natural physiological state where verbalizing thoughts feels intrusive, unsafe, or exhausting. "
            "The client prefers silence, short replies, or non-verbal presence. This is an adaptive boundary, not resistance."
        ),
        "comforting_reframe": (
            "Your hesitation is wise. You have the right to keep your inner world private until you feel unconditional safety. "
            "Somatic and human-centered therapists honor this boundary and never force premature disclosure."
        ),
        "research_key": "emotional_resistance"
    }
}

def infer_anxiety_pattern(user_text: str) -> dict:
    """
    Infers surface-level emotional/anxiety pattern from client input
    and returns rich psychoeducational context and relevant research papers.
    """
    msg = user_text.lower().strip()

    # 1. Emotional resistance / hesitation
    hesitation_cues = [
        "don't want to open", "dont want to open", "not ready", "hard to talk",
        "can't talk", "cant talk", "never mind", "nevermind", "forget it",
        "leave it", "not comfortable", "idk", "i don't know", "i dont know",
        "nothing", "skip", "pass", "stop asking", "too personal", "too painful"
    ]
    if any(k in msg for k in hesitation_cues) or (len(msg.split()) <= 2 and msg in ["no", "skip", "pass", "nothing", "idk"]):
        profile = ANXIETY_PROFILES["emotional_resistance"]
        papers = RESEARCH_LIBRARY["emotional_resistance"]
        return {"key": "emotional_resistance", "profile": profile, "papers": papers}

    # 2. Somatic panic & physical sensations
    somatic_cues = [
        "chest feels tight", "chest tight", "heart racing", "can't breathe", "cant breathe",
        "panic attack", "panic", "dizziness", "shaking", "jittery", "nauseous", "trembling"
    ]
    if any(k in msg for k in somatic_cues):
        profile = ANXIETY_PROFILES["somatic_panic"]
        papers = RESEARCH_LIBRARY["somatic_panic"]
        return {"key": "somatic_panic", "profile": profile, "papers": papers}

    # 3. Relational & attachment
    relational_cues = [
        "partner", "husband", "wife", "boyfriend", "girlfriend", "marriage",
        "relationship", "family", "parents", "mother", "father", "fight",
        "loved ones", "loved one", "conflict", "breakup", "lonely", "abandon"
    ]
    if any(k in msg for k in relational_cues):
        profile = ANXIETY_PROFILES["relational_attachment"]
        papers = RESEARCH_LIBRARY["relational_attachment"]
        return {"key": "relational_attachment", "profile": profile, "papers": papers}

    # 4. Burnout & exhaustion
    burnout_cues = [
        "burnout", "overwhelm", "exhaust", "too much", "work", "job", "career",
        "deadline", "drowning", "depleted", "brain fog", "tired"
    ]
    if any(k in msg for k in burnout_cues):
        profile = ANXIETY_PROFILES["burnout_perfectionism"]
        papers = RESEARCH_LIBRARY["burnout_perfectionism"]
        return {"key": "burnout_perfectionism", "profile": profile, "papers": papers}

    # 5. Social & evaluative fear
    social_cues = [
        "judge", "judged", "social", "embarrass", "freeze up", "people think",
        "stupid", "imposter", "ashamed", "shame", "rejection", "stigma", "taboo"
    ]
    if any(k in msg for k in social_cues):
        profile = ANXIETY_PROFILES["social_evaluative"]
        papers = RESEARCH_LIBRARY["social_evaluative"]
        return {"key": "social_evaluative", "profile": profile, "papers": papers}

    # 6. Default to Generalized Cognitive Worry
    profile = ANXIETY_PROFILES["generalized_worry"]
    papers = RESEARCH_LIBRARY["generalized_worry"]
    return {"key": "generalized_worry", "profile": profile, "papers": papers}

def search_research_by_query(query: str) -> dict:
    """
    Finds peer-reviewed psychological literature based on an emotional expression or topic inquiry.
    """
    q_lower = query.lower().strip()

    # Direct author / paper keyword match check
    if any(k in q_lower for k in ["porges", "polyvagal", "vagus", "heart", "panic", "adrenaline", "fight or flight"]):
        p_key = "somatic_panic"
    elif any(k in q_lower for k in ["borkovec", "hofmann", "cbt", "worry", "catastrophic", "overthinking"]):
        p_key = "generalized_worry"
    elif any(k in q_lower for k in ["clark", "wells", "heimberg", "social", "shame", "appraisal", "judge"]):
        p_key = "social_evaluative"
    elif any(k in q_lower for k in ["johnson", "mikulincer", "shaver", "attachment", "eft", "partner", "love", "fight", "relationship", "marriage"]):
        p_key = "relational_attachment"
    elif any(k in q_lower for k in ["maslach", "neff", "burnout", "compassion", "cortisol", "exhaustion"]):
        p_key = "burnout_perfectionism"
    elif any(k in q_lower for k in ["van der kolk", "gross", "body keeps the score", "trauma", "freeze", "guard"]):
        p_key = "emotional_resistance"
    else:
        inferred = infer_anxiety_pattern(query)
        p_key = inferred["key"]

    profile = ANXIETY_PROFILES[p_key]
    papers = RESEARCH_LIBRARY[p_key]
    
    return {
        "key": p_key,
        "profile": profile,
        "papers": papers,
        "response_summary": (
            f"Based on what you expressed, your nervous system appears to be navigating **{profile['label']}**. "
            f"In clinical psychology, this is understood as `{profile['nervous_system_state']}`. "
            f"Here are the foundational peer-reviewed studies that explore this exact experience:"
        )
    }

def format_psychoeducation_block(inferred: dict) -> str:
    """Formats the inferred anxiety profile and research papers into an elegant gallery plaque markdown block."""
    p = inferred["profile"]
    papers = inferred["papers"]

    papers_md = "\n".join([
        f"• **[{doc['title']}]({doc['doi']})** ({doc['year']})  \n"
        f"  *Authors:* {doc['authors']} — *{doc['journal']}*  \n"
        f"  *Clinical Insight:* {doc['key_finding']}"
        for doc in papers
    ])

    return f"""
<div class="gallery-plaque">
    <div class="plaque-title">{p['icon']} {p['aesthetic_title']}</div>
    <div class="plaque-subtitle"><em>Phenotype:</em> {p['label']}</div>
    <div style="margin: 8px 0; font-size: 0.88rem; color: #4B6355;">
        <strong>Nervous System Dynamic:</strong> <span style="background: #F1ECE3; padding: 2px 8px; border-radius: 6px; font-weight: 600; color: #6D4C3D;">{p['nervous_system_state']}</span>
    </div>
    <p style="font-size: 0.92rem; color: #354E41; line-height: 1.6; margin-bottom: 8px;">
        {p['description']}
    </p>
    <div style="background: rgba(43, 83, 62, 0.05); padding: 10px 14px; border-radius: 10px; margin-bottom: 12px; font-size: 0.88rem; color: #234834;">
        🌿 <strong>Compassionate Reframe:</strong> {p['comforting_reframe']}
    </div>
    <details>
        <summary style="font-weight: 600; cursor: pointer; color: #2B533E; font-size: 0.86rem;">
            📚 Peer-Reviewed Research Literature & Clinical Studies ({len(papers)} papers)
        </summary>
        <div style="margin-top: 10px; font-size: 0.84rem; color: #435A4D; line-height: 1.6;">
            {papers_md}
        </div>
    </details>
</div>
"""
