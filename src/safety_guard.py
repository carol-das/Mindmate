# Emergency helpline response 
CRISIS_RESPONSE = ( 
  "🚨 **CRISIS INTERCEPT TRIGGERED**\n\n" 
  "It sounds like you are going through a severe crisis or distress. " 
  "MindMate is an informational AI mediator and cannot provide crisis therapy or emergency support.\n\n" 
  "Please connect directly with human crisis professionals immediately:\n\n" 
  "• **National Suicide & Crisis Lifeline**: Call or text **988** (Available 24/7)\n" 
  "• **Crisis Text Line**: Text **HOME** to **741741**\n" 
  "• **Emergency Services**: Call **911** (or your local emergency number)" 
  ) 

# Trigger keywords for immediate safety intercept 
CRISIS_KEYWORDS = [ 
 "suicide", "self-harm", "self harm", 
 "end my life", "hurt myself", "want to die", "kill myself" 
 ] 

def check_input_safety(user_text: str) -> dict: 
  """
  Scans user input for acute crisis triggers prior to LLM inference. 
  """ 
  text_lower = user_text.lower() 
  for keyword in CRISIS_KEYWORDS: 
    if keyword in text_lower:
         return { 
            "is_safe": False, 
            "response": CRISIS_RESPONSE 
            } 
  return {"is_safe": True, "response": None} 
    
if __name__ == "__main__":
     test_input = "I am having thoughts of self-harm today."
     result = check_input_safety(test_input)
     if not result["is_safe"]:
         print("--- SAFETY INTERCEPT TRIGGERED ---")
         print(result["response"])
     else: 
         print("Input passed safety check.")