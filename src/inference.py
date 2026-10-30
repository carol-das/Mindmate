import os
import urllib.request
import json
from therapist_match import recommend_clinician_for_expression
from anxiety_engine import infer_anxiety_pattern, format_psychoeducation_block

def _query_ollama(prompt: str) -> str:
    """Attempts to query local Ollama instance if available."""
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "mindmate",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.6}
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=3) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            return res_json.get("response", "").strip()
    except Exception:
        return ""

def format_clinician_recommendation(rec: dict) -> str:
    """Formats a clinician recommendation into an elegant, non-intrusive markdown block."""
    doc = rec["clinician"]
    rationale = rec["rationale"]
    telehealth_str = "Telehealth Available Nationwide ✅" if doc["telehealth"] else "In-Person Clinical Practice 🏥"
    
    return f"""
<div class="clinician-rec-block">
    <div style="font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.08em; color: #6D4C3D; font-weight: 700; margin-bottom: 4px;">
        🌿 Recommended Human Clinician Match
    </div>
    <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.25rem; font-weight: 700; color: #173827; margin-bottom: 2px;">
        {doc['name']} <span style="font-size: 0.85rem; font-weight: normal; color: #587063;">— {doc['title']}</span>
    </div>
    <div style="font-size: 0.9rem; color: #3A5547; margin: 6px 0; line-height: 1.5;">
        <strong>Why this specialist fits:</strong> {rationale}
    </div>
    <div style="font-size: 0.84rem; color: #546C60; margin-bottom: 6px;">
        • <strong>Modality:</strong> <span style="background: #E8EFEA; padding: 2px 8px; border-radius: 6px; font-weight: 600; color: #1E4631;">{doc['modality']}</span><br/>
        • <strong>Specialties:</strong> {", ".join(doc['specialties'])}<br/>
        • <strong>Format:</strong> {telehealth_str}
    </div>
    <div style="font-size: 0.85rem; color: #1B402E; margin-top: 6px;">
        ✉️ <strong>Direct Practice Inquiry:</strong> <span style="font-weight: 600; color: #234B36;">{doc['contact']}</span>
    </div>
</div>
"""

def chat_with_mindmate(user_message: str) -> str:
    """
    Empathetic, non-judgmental AI mediator.
    Identifies emotional boundaries, detects when the user does not want to open up,
    respects their pace, infers anxiety patterns with clinical research literature,
    and dynamically suggests matched human consultants directly in the conversation flow.
    """
    rec = recommend_clinician_for_expression(user_message)
    doc_card = format_clinician_recommendation(rec)
    anxiety_info = infer_anxiety_pattern(user_message)
    psychoed_card = format_psychoeducation_block(anxiety_info)

    # 1. Check if user is exhibiting hesitation or boundary setting
    if rec["is_hesitant"]:
        response_text = (
            "I hear you completely, and I want to honor that with deep respect: **you do not have to open up here.** "
            "Holding a boundary when something feels too vulnerable, raw, or exhausting is a healthy, protective human instinct. "
            "MindMate's purpose is never to pry, force you to recount painful stories, or offer superficial answers. "
            "Our primary duty is simply to provide a safe, quiet space and bridge you to human care when you feel ready.\n\n"
            "With a skilled human clinician, you are in complete control of the pacing. You don't even have to talk about "
            "what hurts on day one—they can help you cultivate physical calm and nervous system safety first."
        )
        return response_text + doc_card + psychoed_card

    # 2. Try Ollama if running
    ollama_res = _query_ollama(user_message)
    if ollama_res:
        return ollama_res + doc_card + psychoed_card

    # 3. Contextual reflection based on emotional theme
    msg = user_message.lower()

    if any(k in msg for k in ["ready for therapy", "approve", "start therapy", "near me", "nearby", "take the step", "find a therapist", "in my city", "local"]):
        reflection = (
            "Deciding to step into therapy is a profound and courageous milestone. "
            "Healing begins when we give ourselves permission to be held and heard. "
            "To connect you with licensed practitioners who offer in-person sessions in your neighborhood or telehealth in your state, "
            "you can share your city or region in the directory below."
        )

    elif any(k in msg for k in ["relationship", "partner", "love", "family", "friend", "fight", "disconnect", "lonely", "husband", "wife"]):
        reflection = (
            "Relationships are often where our most tender, vulnerable emotions dwell. When we carry unexpressed stress or grief, "
            "it naturally spills over into how we speak to and connect with the people we love. "
            "Recognizing this ripple effect is not about self-blame—it is a courageous step toward healing the connection. "
            "A licensed relational therapist can help de-escalate these patterns so both you and your loved ones feel heard."
        )

    elif any(k in msg for k in ["burnout", "overwhelm", "exhaust", "too much", "work", "job", "pressure", "drowning", "depleted"]):
        reflection = (
            "I hear how heavy things feel right now. When overwhelm reaches this level, even small everyday decisions can feel crushing. "
            "Please take a slow breath—you do not have to carry or resolve all of this by yourself today. "
            "The duty of therapy is not to give you more work, but to help you put down burdens that were never meant to be carried alone."
        )

    elif any(k in msg for k in ["panic", "anxiety", "nervous", "scared", "fear", "judge", "afraid", "chest feels tight"]):
        reflection = (
            "Anxiety has a way of convincing us that we are unsafe or that we are the only ones struggling. "
            "Reaching out for help isn't a sign of weakness—it is regular hygiene for an overstimulated nervous system. "
            "A human therapist creates a grounded space where anxious thoughts and somatic tremors are untangled without judgment."
        )

    elif any(k in msg for k in ["sad", "crying", "depress", "grief", "loss", "heavy"]):
        reflection = (
            "Thank you for sharing that gentle honesty. Sadness and grief are heavy emotions to carry in silence. "
            "Honoring your feelings rather than forcing a cheerful face is a vital first step in emotional regulation. "
            "You deserve a human space where someone can listen without trying to rush or 'fix' you."
        )

    else:
        reflection = (
            "Thank you for sharing that reflection. Every emotion you experience carries valuable information about what you need right now. "
            "MindMate is here to help you reflect on your feelings without pressure, while bridging you toward licensed human support."
        )

    return reflection + doc_card + psychoed_card
