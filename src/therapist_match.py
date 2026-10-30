# Directory of sample clinicians and verification resources
CLINICIAN_DIRECTORY = [ 
    { "name": "Dr. Sarah Jenkins, PsyD",
      "modality": "Cognitive Behavioral Therapy (CBT)",
      "specialties": ["Anxiety", "Work Stress", "Life Transitions"],
      "telehealth": True,
      "contact": "s.jenkins@mindmate-referrals.org"
       
     },
     { "name": "Marcus Vance, LMFT",
       "modality": "Mindfulness & Acceptance Commitment Therapy (ACT)",
       "specialties": ["Overwhelm", "Burnout", "Communication"],
       "telehealth": True,
       "contact": "m.vance@mindmate-referrals.org" 
     },
     { "name": "Dr. Elena Rostova, MD",
       "modality": "Integrative Psychiatry & Psychotherapy",
       "specialties": ["Severe Anxiety", "Mood Regulation", "Panic"],
       "telehealth": False,
       "contact": "e.rostova@mindmate-referrals.org"
     } 
     
]

# Official external directories for broader search
EXTERNAL_RESOURCES = { 
    "Psychology Today Directory": "https://www.psychologytoday.com/us/therapists",
    "SAMHSA Behavioral Health Locator": "https://findtreatment.gov",
    "Association for Behavioral and Cognitive Therapies (ABCT)": "https://www.abct.org/find-a-therapist"
} 

def find_therapist_matches(user_concern: str = "") -> list:
     """ 
     
     Returns a filtered list of sample clinicians based on modality or concern keywords.
     Non-diagnostic matching helper.
     """
     
     if not user_concern:
         return CLINICIAN_DIRECTORY
         
     query = user_concern.lower()
     matches = []
     
     for clinician in CLINICIAN_DIRECTORY:
           # Match against modalities or specialties
           match_score = any(
                 query in specialty.lower() or query in clinician["modality"].lower()
                 for specialty in clinician["specialties"]
           )
    
           if match_score or query in clinician["name"].lower():
               matches.append(clinician)
               
      # Return all clinicians if no specific keyword match is found
     return matches if matches else CLINICIAN_DIRECTORY
      
if __name__ == "__main__":
      print("--- Testing Clinician Referral Engine ---")
      results = find_therapist_matches("Anxiety")
      print(f"Found {len(results)} matches for 'Anxiety':")
      for doc in results:
          print(f"• {doc['name']} ({doc['modality']})")