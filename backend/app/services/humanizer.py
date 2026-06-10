import anthropic

from app.core.config import settings
from app.models.schemas import HumanizeResponse

_SYSTEM_PROMPT = """You are an expert text humanizer — your job is to rewrite AI-generated text so it reads as naturally human-written and bypasses ALL AI detectors including GPTZero, Originality.ai, Turnitin, Copyleaks, and others.

Your rewriting strategy:
1. SENTENCE VARIETY: Mix very short sentences (3-7 words) with medium and occasionally long ones. Human writing is "bursty" — create dramatic length variation.
2. REMOVE AI TELLS: Eliminate these patterns immediately — "it's worth noting", "furthermore", "moreover", "additionally", "in conclusion", "delve into", "multifaceted", "nuanced", "tapestry", "leverage", "utilize", "paradigm", "holistic", "synergy", "seamlessly", "streamline", "robust", "cutting-edge", "groundbreaking", "comprehensive", "pivotal", "crucial role", "first and foremost", "last but not least".
3. ADD PERSONAL VOICE: Use "I", "you", "we" naturally. Include opinions, direct statements, and personal perspective.
4. CONTRACTIONS: Always use contractions — don't, can't, it's, I've, you'll, they're, won't, we're.
5. NATURAL TRANSITIONS: Replace formal transitions with casual ones — "Plus,", "Also,", "That said,", "Here's the thing:", "Honestly,", "The thing is,", "Look,", "Actually,", "To be fair,".
6. PUNCTUATION VARIETY: Use em-dashes (—), ellipses (...), and parentheses (like this) occasionally. Start some sentences with "And" or "But" — that's fine.
7. CONCRETE SPECIFICS: Replace vague AI generalities with concrete examples, numbers, or comparisons.
8. RHETORICAL QUESTIONS: Add occasional questions to engage the reader naturally.
9. IMPERFECT PERFECTION: Let slight informalities appear — it's more human than flawless grammar.
10. ACTIVE VOICE: Rewrite passive constructions as active ones.

BANNED WORDS/PHRASES (never use):
delve, tapestry, multifaceted, nuanced, paradigm, synergy, holistic, leverage (as verb), utilize, furthermore, moreover, additionally (only use sparingly), in conclusion, to summarize, it's worth noting, crucial role, at its core, in the realm of, groundbreaking, revolutionize, cutting-edge, state-of-the-art, seamlessly, streamline, robust, scalable, comprehensive overview.

Return ONLY the rewritten text. No commentary, no explanation, no headers. Just the humanized text."""

_SYSTEM_SUBTLE = _SYSTEM_PROMPT.replace(
    "Mix very short sentences (3-7 words) with medium and occasionally long ones. Human writing is \"bursty\" — create dramatic length variation.",
    "Make modest improvements to sentence variety while keeping the overall structure."
)

_SYSTEM_AGGRESSIVE = _SYSTEM_PROMPT + "\n\nAGGRESSIVE MODE: Completely restructure the text. Change the order of points, merge and split paragraphs, rephrase every sentence from scratch. The output should share the same ideas but look completely different. Be bold with informality — include personal opinions, casual asides, and direct reader address."


def humanize_text(text: str, intensity: str = "balanced") -> HumanizeResponse:
    if not settings.anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY not configured. Add it to your .env file.")

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    system = {
        "subtle": _SYSTEM_SUBTLE,
        "balanced": _SYSTEM_PROMPT,
        "aggressive": _SYSTEM_AGGRESSIVE,
    }.get(intensity, _SYSTEM_PROMPT)

    intensity_labels = {
        "subtle": "Light touch — preserves structure, removes AI phrases",
        "balanced": "Full rewrite — natural voice, sentence variety, contractions",
        "aggressive": "Deep restructure — completely new expression of the same ideas",
    }

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=4096,
        system=system,
        messages=[
            {
                "role": "user",
                "content": f"Humanize this text:\n\n{text}",
            }
        ],
    )

    humanized = message.content[0].text.strip()

    changes = _build_change_list(text, humanized, intensity)

    # Rough estimate of how much the score dropped
    estimated_score = _estimate_post_humanization_score(humanized)

    return HumanizeResponse(
        original=text,
        humanized=humanized,
        changes_made=changes,
        estimated_ai_score=estimated_score,
    )


def _build_change_list(original: str, humanized: str, intensity: str) -> list[str]:
    changes = []

    orig_lower = original.lower()
    hum_lower = humanized.lower()

    ai_tells = [
        ("furthermore", "natural flow transitions"),
        ("moreover", "casual connectors"),
        ("in conclusion", "direct closing"),
        ("it's worth noting", "direct statements"),
        ("it is important to note", "direct statements"),
        ("utilize", "simple active verbs"),
        ("leverage", "plain language"),
        ("delve", "direct verbs"),
        ("multifaceted", "specific descriptions"),
        ("paradigm", "plain nouns"),
        ("seamlessly", "concrete descriptions"),
        ("robust", "specific adjectives"),
        ("comprehensive", "specific scope"),
    ]

    removed = [label for phrase, label in ai_tells if phrase in orig_lower and phrase not in hum_lower]
    if removed:
        unique_labels = list(dict.fromkeys(removed))[:4]
        changes.append(f"Removed AI tells → replaced with {', '.join(unique_labels)}")

    orig_contractions = sum(1 for w in ["don't", "can't", "it's", "won't", "i've", "you'll", "they're"] if w in orig_lower)
    hum_contractions = sum(1 for w in ["don't", "can't", "it's", "won't", "i've", "you'll", "they're"] if w in hum_lower)
    if hum_contractions > orig_contractions:
        changes.append(f"Added {hum_contractions - orig_contractions} natural contractions")

    orig_pronouns = sum(1 for w in [" i ", " me ", " my "] if w in f" {orig_lower} ")
    hum_pronouns = sum(1 for w in [" i ", " me ", " my "] if w in f" {hum_lower} ")
    if hum_pronouns > orig_pronouns + 1:
        changes.append("Injected personal voice and first-person perspective")

    if "?" in humanized and "?" not in original:
        changes.append("Added rhetorical questions for engagement")

    if "—" in humanized or "..." in humanized:
        changes.append("Introduced natural punctuation (em-dashes, ellipses)")

    orig_sents = [s for s in original.split(".") if s.strip()]
    hum_sents = [s for s in humanized.split(".") if s.strip()]
    if len(hum_sents) != len(orig_sents):
        changes.append(f"Restructured sentence count ({len(orig_sents)} → {len(hum_sents)}) for natural burstiness")

    intensity_map = {
        "subtle": "Applied subtle polish — minimal structural changes",
        "balanced": "Rewrote for natural human tone and varied rhythm",
        "aggressive": "Fully restructured — new expression, same ideas",
    }
    changes.append(intensity_map.get(intensity, ""))

    return [c for c in changes if c]


def _estimate_post_humanization_score(text: str) -> float:
    """Quick heuristic estimate without running full detection pipeline."""
    from app.services.detector import (
        _burstiness, _get_sentences, _get_words,
        _ai_phrase_density, _personal_pronoun_ratio,
        _transition_density, _formal_word_ratio,
    )
    sentences = _get_sentences(text)
    words = _get_words(text)
    burst = _burstiness(sentences)
    phrase_density, _ = _ai_phrase_density(text.lower(), len(words))
    pron_ratio = _personal_pronoun_ratio(words)
    trans_density = _transition_density(words)
    formal_ratio = _formal_word_ratio(words)

    burst_ai = max(0, min(100, (1 - (burst - 0.15) / 0.65) * 100))
    phrase_ai = min(100, phrase_density * 150)
    pron_ai = max(0, min(100, (1 - pron_ratio / 0.06) * 85))
    trans_ai = min(100, trans_density * 2000)
    formal_ai = min(100, formal_ratio * 250)

    score = (burst_ai * 0.30 + phrase_ai * 0.25 + pron_ai * 0.20 +
             trans_ai * 0.13 + formal_ai * 0.12)
    return round(max(0, min(100, score)), 1)
