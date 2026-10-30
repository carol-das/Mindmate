# Directory of sample clinicians and verification resources with geographical metadata
CLINICIAN_DIRECTORY = [ 
    {
        "id": "dr_jenkins",
        "name": "Dr. Sarah Jenkins, PsyD",
        "title": "Clinical Psychologist",
        "modality": "Cognitive Behavioral Therapy (CBT) & Compassion-Focused",
        "specialties": ["Anxiety", "Work Stress", "Life Transitions", "Self-Criticism"],
        "telehealth": True,
        "city": "San Francisco",
        "state": "CA",
        "zip": "94102",
        "location": "San Francisco, CA (Licensed in CA, WA, OR, NV & 24 other states)",
        "in_person_address": "450 Sutter St, Suite 820, San Francisco, CA 94108",
        "contact": "s.jenkins@mindmate-referrals.org",
        "bio": "Specializes in helping high-stress professionals and thoughtful individuals deconstruct anxiety and rewrite harsh inner dialogue."
    },
    {
        "id": "marcus_vance",
        "name": "Marcus Vance, LMFT",
        "title": "Licensed Marriage & Family Therapist",
        "modality": "Mindfulness & Acceptance Commitment Therapy (ACT)",
        "specialties": ["Overwhelm", "Burnout", "Communication", "Couples"],
        "telehealth": True,
        "city": "Austin",
        "state": "TX",
        "zip": "78701",
        "location": "Austin, TX (In-Person Clinic & Telehealth)",
        "in_person_address": "1200 S Congress Ave, Suite 300, Austin, TX 78704",
        "contact": "m.vance@mindmate-referrals.org",
        "bio": "Passionate about demystifying therapy, improving relational communication, and helping clients build psychological flexibility."
    },
    {
        "id": "dr_patel",
        "name": "Dr. Maya Patel, LPC, SEP",
        "title": "Licensed Professional Counselor & Somatic Specialist",
        "modality": "Somatic Experiencing & Polyvagal Nervous System Regulation",
        "specialties": ["Intimate Emotions", "Trauma", "Emotional Regulation", "Grief", "Reluctance to Open Up"],
        "telehealth": True,
        "city": "Boulder",
        "state": "CO",
        "zip": "80302",
        "location": "Boulder, CO (Telehealth Nationwide & In-Clinic)",
        "in_person_address": "1001 Pearl St, Suite 210, Boulder, CO 80302",
        "contact": "m.patel@mindmate-referrals.org",
        "bio": "Focuses on the mind-body connection, guiding clients to sit comfortably with intimate emotions and soothe chronic nervous system distress without forcing painful storytelling."
    },
    {
        "id": "david_chen",
        "name": "David Chen, LMFT",
        "title": "Family Systems & Relational Specialist",
        "modality": "Emotionally Focused Therapy (EFT) & Attachment-Based",
        "specialties": ["Relationships", "Family Dynamics", "Vulnerability", "Conflict Repair"],
        "telehealth": True,
        "city": "New York",
        "state": "NY",
        "zip": "10010",
        "location": "New York, NY (In-Person & Telehealth in NY, NJ, CT)",
        "in_person_address": "285 Lexington Ave, 4th Floor, New York, NY 10016",
        "contact": "d.chen@mindmate-referrals.org",
        "bio": "Dedicated to breaking generational emotional barriers and exploring how personal emotional healing restores harmony with loved ones."
    },
    {
        "id": "dr_rostova",
        "name": "Dr. Elena Rostova, MD",
        "title": "Board-Certified Integrative Psychiatrist",
        "modality": "Integrative Psychiatry & Psychotherapy",
        "specialties": ["Severe Anxiety", "Mood Regulation", "Panic", "Depression"],
        "telehealth": False,
        "city": "Chicago",
        "state": "IL",
        "zip": "60611",
        "location": "Chicago, IL (In-Clinic Care)",
        "in_person_address": "676 N Michigan Ave, Suite 1500, Chicago, IL 60611",
        "contact": "e.rostova@mindmate-referrals.org",
        "bio": "Combines clinical psychotherapy with medical evaluation for holistic nervous system stabilization and complex mood balance."
    }
]

# Official external directories for broader search
EXTERNAL_RESOURCES = { 
    "Psychology Today Directory": "https://www.psychologytoday.com/us/therapists",
    "SAMHSA Behavioral Health Treatment Locator": "https://findtreatment.gov",
    "Association for Behavioral and Cognitive Therapies (ABCT)": "https://www.abct.org/find-a-therapist",
    "TherapyDen (Inclusive & Progressive Clinicians)": "https://www.therapyden.com",
    "Open Path Psychotherapy Collective (Affordable Care)": "https://openpathcollective.org"
}

def find_therapist_matches(user_concern: str = "", user_location: str = "", in_person_only: bool = False) -> list:
    """ 
    Returns a filtered and sorted list of clinicians based on concern and geographic locality.
    Prioritizes local in-person matches when a city/state is provided.
    """
    concern_q = user_concern.lower().strip() if user_concern and user_concern != "All Specialties" else ""
    loc_q = user_location.lower().strip() if user_location else ""
    
    matches = []
    
    for clinician in CLINICIAN_DIRECTORY:
        # Concern filter
        concern_matched = True
        if concern_q:
            concern_matched = any(
                concern_q in specialty.lower() or concern_q in clinician["modality"].lower()
                for specialty in clinician["specialties"]
            ) or (concern_q in clinician["name"].lower())
            
        if not concern_matched:
            continue
            
        # In-person only filter
        if in_person_only and clinician.get("telehealth") is False and not clinician.get("in_person_address"):
            continue
            
        # Location scoring & tagging
        is_local = False
        locality_badge = ""
        
        if loc_q:
            # Check city, state, or zip match
            c_city = clinician.get("city", "").lower()
            c_state = clinician.get("state", "").lower()
            c_loc = clinician.get("location", "").lower()
            c_zip = clinician.get("zip", "")
            
            if loc_q in c_city or loc_q in c_state or loc_q in c_zip or loc_q in c_loc:
                is_local = True
                locality_badge = f"📍 Nearby In-Person Clinic ({clinician['city']}, {clinician['state']})"
            elif clinician.get("telehealth"):
                locality_badge = "💻 Telehealth Licensed in Your Region"
            else:
                locality_badge = f"🏥 In-Clinic Only ({clinician['city']}, {clinician['state']})"
        else:
            if clinician.get("telehealth"):
                locality_badge = f"✅ In-Person ({clinician['city']}) & Telehealth"
            else:
                locality_badge = f"🏥 In-Person Practice ({clinician['city']}, {clinician['state']})"
                
        clinician_copy = dict(clinician)
        clinician_copy["is_local"] = is_local
        clinician_copy["locality_badge"] = locality_badge
        matches.append(clinician_copy)
        
    # Sort local matches to the top
    if loc_q:
        matches.sort(key=lambda x: 0 if x.get("is_local") else 1)
        
    return matches if matches else CLINICIAN_DIRECTORY

def recommend_clinician_for_expression(expression_text: str, user_location: str = "") -> dict:
    """
    Evaluates patient expression, hesitation cues, or specific emotional struggles
    and returns a tailored clinician match with an empathetic rationale.
    """
    msg = expression_text.lower().strip()
    loc_q = user_location.lower().strip() if user_location else ""
    
    # Check for hesitation, boundaries, or resistance to opening up
    hesitation_cues = [
        "don't want to open", "dont want to open", "not ready to open", "hard to open", 
        "don't want to talk", "dont want to talk", "can't talk", "cant talk", "cannot talk",
        "never mind", "nevermind", "forget it", "leave it", "drop it", "not comfortable",
        "too hard to explain", "too personal", "idk", "i don't know", "i dont know",
        "stop asking", "too painful", "scared to say", "can't express"
    ]
    is_hesitant = any(cue in msg for cue in hesitation_cues) or (len(msg.split()) <= 2 and msg in ["no", "skip", "pass", "nothing", "idk"])
    
    if is_hesitant:
        doc = next(d for d in CLINICIAN_DIRECTORY if d["id"] == "dr_patel")
        return {
            "clinician": doc,
            "category": "gentle_boundaries",
            "is_hesitant": True,
            "rationale": (
                "When putting feelings into words feels too invasive or exhausting, Somatic Experiencing provides a non-verbal, "
                "gentle approach. Dr. Patel works with physical safety, breathing, and nervous system regulation so you never have "
                "to retell painful stories until you are completely ready."
            )
        }
        
    # Check for relationship, marriage, or family dynamics
    relationship_cues = [
        "partner", "husband", "wife", "boyfriend", "girlfriend", "marriage", "relationship", 
        "family", "parents", "mother", "father", "kids", "fight", "loved ones", "loved one",
        "conflict", "distance", "disconnect", "yelling", "breakup", "divorce"
    ]
    if any(cue in msg for cue in relationship_cues):
        doc = next(d for d in CLINICIAN_DIRECTORY if d["id"] == "david_chen")
        return {
            "clinician": doc,
            "category": "relationships",
            "is_hesitant": False,
            "rationale": (
                "Our intimate emotions deeply influence how we connect with the people we love. David Chen specializes in Emotionally "
                "Focused Therapy (EFT) to help untangle communication patterns, reduce defensiveness, and restore warmth in close relationships."
            )
        }
        
    # Check for burnout, work exhaustion, or feeling overwhelmed
    burnout_cues = ["burnout", "overwhelm", "exhaust", "drowning", "too much", "work", "job", "career", "pressure", "deadline"]
    if any(cue in msg for cue in burnout_cues):
        doc = next(d for d in CLINICIAN_DIRECTORY if d["id"] == "marcus_vance")
        return {
            "clinician": doc,
            "category": "burnout_and_stress",
            "is_hesitant": False,
            "rationale": (
                "When chronic stress depletes your mental stamina, Marcus Vance uses Acceptance and Commitment Therapy (ACT) to help you "
                "set healthy boundaries, step off the relentless achievement treadmill, and regain psychological room to breathe."
            )
        }
        
    # Check for severe panic, medical symptoms, or dark mood swings
    panic_cues = ["panic attack", "panic", "heart racing", "severe depression", "medication", "dark thoughts", "psychiatrist"]
    if any(cue in msg for cue in panic_cues):
        doc = next(d for d in CLINICIAN_DIRECTORY if d["id"] == "dr_rostova")
        return {
            "clinician": doc,
            "category": "panic_and_integrative",
            "is_hesitant": False,
            "rationale": (
                "For acute panic or biological mood disruptions, Dr. Rostova provides integrative psychiatric evaluation alongside "
                "psychotherapy to gently stabilize your nervous system and support your daily functioning."
            )
        }
        
    # Default to Dr. Sarah Jenkins (CBT & Compassion-Focused)
    doc = next(d for d in CLINICIAN_DIRECTORY if d["id"] == "dr_jenkins")
    return {
        "clinician": doc,
        "category": "general_anxiety_and_growth",
        "is_hesitant": False,
        "rationale": (
            "Specializes in compassion-focused therapy and CBT, providing a safe, patient setting to untangle persistent worries, "
            "quiet self-critical thoughts, and build steady emotional confidence."
        )
    }

def generate_first_contact_email(clinician_name: str, primary_concern: str, user_name: str = "[Your Name]", user_location: str = "") -> str:
    """
    Generates a gentle, low-pressure outreach draft to help users overcome the initial barrier of contacting a therapist.
    """
    loc_clause = f"in the {user_location} area" if user_location else "for care"
    return f"""Subject: Consultation Inquiry regarding therapy services - {user_name}

Dear {clinician_name},

I hope you are having a peaceful week.

I am reaching out to inquire about your current availability for new adult clients {loc_clause}. I have been taking time to reflect on my mental health, specifically around {primary_concern.lower() if primary_concern else "navigating personal transitions and emotional regulation"}, and your background and therapeutic approach strongly resonated with me.

I have organized my preliminary reflection notes using MindMate so I can be grounded for an intake discussion. Do you currently offer an initial 10-15 minute consultation call or in-person / telehealth intake appointments in the coming weeks?

Thank you for your time, consideration, and the meaningful care you provide.

Warmly,
{user_name}
[Your Phone Number or Preferred Email]"""
