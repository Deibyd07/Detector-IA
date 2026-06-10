import math
import re
import statistics
from collections import Counter
from typing import Any

import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.models.schemas import DetectResponse, MetricDetail, SentenceScore

# ---------------------------------------------------------------------------
# NLTK bootstrap (runs once per process)
# ---------------------------------------------------------------------------
for _pkg in ("punkt", "punkt_tab", "stopwords"):
    try:
        nltk.data.find(f"tokenizers/{_pkg}" if "punkt" in _pkg else f"corpora/{_pkg}")
    except LookupError:
        nltk.download(_pkg, quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

_STOPWORDS = set(stopwords.words("english"))


# ---------------------------------------------------------------------------
# AI phrase lexicon — 160+ high-confidence AI markers
# ---------------------------------------------------------------------------
AI_PHRASES = [
    # ── Epistemic hedges (very AI) ──────────────────────────────────────────
    "it's worth noting", "it is worth noting",
    "it's worth mentioning", "it is worth mentioning",
    "it's important to note", "it is important to note",
    "it's important to understand", "it is important to understand",
    "it's crucial to", "it is crucial to",
    "it's essential to", "it is essential to",
    "it's clear that", "it is clear that",
    "it's evident that", "it is evident that",
    "it's apparent that", "it is apparent that",
    "it's safe to say", "it is safe to say",
    "it should be noted", "it should be emphasized",
    "it cannot be overstated", "it bears mentioning",
    "needless to say", "it goes without saying",
    "suffice it to say", "that being said",
    "with that said", "having said that",
    "rest assured",

    # ── Conclusion / summary phrases ────────────────────────────────────────
    "in conclusion", "to summarize", "in summary",
    "to sum up", "in closing", "to conclude",
    "all things considered", "on the whole",
    "all in all", "in the final analysis",
    "at the end of the day",

    # ── Connector / transition overuse ──────────────────────────────────────
    "furthermore", "moreover", "additionally",
    "consequently", "as a result", "as such",
    "on the other hand", "on one hand",
    "conversely", "in contrast",
    "first and foremost", "last but not least",
    "not only that", "beyond that",
    "by and large", "that said",

    # ── Time / era framing ──────────────────────────────────────────────────
    "in the realm of", "in the world of",
    "in today's world", "in today's society",
    "in today's digital age", "in modern society",
    "in the modern era", "in contemporary society",
    "throughout history", "since the dawn of",
    "in recent years", "over the past few years",
    "moving forward", "going forward",
    "looking ahead", "in the years to come",
    "over the course of",

    # ── Exploration / unpacking verbs ────────────────────────────────────────
    "delve into", "let's delve", "delves into",
    "dive deep", "deep dive", "let's explore",
    "let us explore", "as we explore", "as we navigate",
    "unpack", "unravel", "shed light on",
    "shed light on the", "elucidate",
    "underscores the importance", "underscores the need",
    "highlights the importance", "highlights the need",
    "brings to light",

    # ── AI self-reference ────────────────────────────────────────────────────
    "as an ai", "as an ai language model",
    "as a large language model", "as an ai assistant",
    "i cannot and will not", "i'm unable to",
    "i'd be happy to", "i'd be glad to",
    "allow me to", "let me explain",
    "great question", "excellent question",
    "certainly!", "absolutely!", "of course!",

    # ── Overused AI descriptors ──────────────────────────────────────────────
    "multifaceted", "nuanced approach",
    "nuanced understanding", "nuanced perspective",
    "tapestry", "intricate tapestry",
    "myriad of", "a myriad", "plethora of",
    "paradigm shift", "paradigm",
    "holistic approach", "holistic view",
    "holistic understanding", "holistic perspective",
    "comprehensive overview", "comprehensive guide",
    "comprehensive understanding", "comprehensive analysis",
    "cutting-edge", "state-of-the-art",
    "groundbreaking", "revolutionize",
    "transformative", "game-changing",
    "innovative solution", "robust solution",
    "scalable solution", "seamlessly integrate",
    "streamline", "leverage", "utilize", "utilization",
    "synergy", "synergistic",

    # ── Role / function phrases ──────────────────────────────────────────────
    "plays a crucial role", "plays a pivotal role",
    "plays an integral role", "plays an important role",
    "plays a significant role", "plays a key role",
    "at its core", "at the heart of",
    "the fact remains", "the bottom line is",
    "the key takeaway", "the main takeaway",
    "a key aspect", "a crucial aspect",
    "an important aspect", "a fundamental aspect",
    "a significant factor", "a key factor",
    "a major factor", "a critical component",
    "a wide range of", "a broad range of",

    # ── Previously mentioned markers ─────────────────────────────────────────
    "as previously mentioned", "as mentioned above",
    "as mentioned earlier", "as noted above",
    "as discussed above", "as stated above",
    "as outlined above", "as highlighted above",

    # ── Contextual framing ───────────────────────────────────────────────────
    "in this context", "in this regard",
    "in this way", "in this sense",
    "to this end", "to that end",
    "with this in mind", "bearing this in mind",
    "in light of this", "given the above",
    "as evidenced by", "as demonstrated by",
    "as illustrated by", "as shown by",

    # ── Certainty / emphasis overuse ─────────────────────────────────────────
    "it cannot be denied", "there is no denying",
    "without a doubt", "undoubtedly",
    "without question", "unquestionably",
    "as we can see", "as we have seen",
    "this is especially true", "this is particularly true",
    "the same holds true", "the same can be said",
    "it stands to reason",

    # ── Common AI essay structures ───────────────────────────────────────────
    "pros and cons", "advantages and disadvantages",
    "benefits and drawbacks", "strengths and weaknesses",
    "each and every", "time and time again",
]

_AI_PHRASES_LOWER = [p.lower() for p in AI_PHRASES]

# ---------------------------------------------------------------------------
# Contraction pattern — absence is a strong AI signal in non-academic prose
# ---------------------------------------------------------------------------
_CONTRACTION_RE = re.compile(
    r"\b(don't|doesn't|didn't|won't|wouldn't|can't|couldn't|shouldn't"
    r"|isn't|aren't|wasn't|weren't|haven't|hasn't|hadn't"
    r"|i'm|i've|i'd|i'll|you're|you've|you'd|you'll"
    r"|he's|he'd|he'll|she's|she'd|she'll"
    r"|we're|we've|we'd|we'll|they're|they've|they'd|they'll"
    r"|that's|there's|here's|who's|what's|let's"
    r"|could've|should've|would've|might've|must've"
    r"|it's|it'd|it'll)\b",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# AI sentence opener words / phrases
# ---------------------------------------------------------------------------
_AI_OPENER_WORDS = {
    "however", "moreover", "furthermore", "additionally", "therefore",
    "thus", "hence", "consequently", "nevertheless", "nonetheless",
    "accordingly", "subsequently", "conversely", "alternatively",
    "importantly", "notably", "significantly", "essentially",
    "ultimately", "fundamentally", "specifically", "generally",
    "typically", "traditionally", "historically", "overall",
}

_AI_OPENER_PHRASES = (
    "it is ", "it's ", "this is ", "this means ", "this suggests ",
    "this indicates ", "this demonstrates ", "this shows ", "this highlights ",
    "this underscores ", "this reflects ", "there are ", "there is ",
    "in conclusion", "in summary", "in essence", "in general",
    "in order to", "as a result", "as mentioned", "as noted",
    "to summarize", "to conclude", "to understand ",
    "when considering", "when we consider",
)

# ---------------------------------------------------------------------------
# Other word group sets
# ---------------------------------------------------------------------------
_TRANSITION_WORDS = {
    "furthermore", "moreover", "additionally", "consequently",
    "nevertheless", "nonetheless", "therefore", "thus", "hence",
    "subsequently", "accordingly", "conversely", "alternatively",
    "notably", "importantly", "significantly", "evidently",
    "undoubtedly", "admittedly", "ultimately",
}

_PERSONAL_PRONOUNS = {"i", "me", "my", "mine", "myself", "we", "us", "our", "ours"}

_FORMAL_WORDS = {
    "utilize", "utilization", "leverage", "facilitate", "implement",
    "endeavor", "commence", "terminate", "ascertain", "elucidate",
    "demonstrate", "indicate", "regarding", "pertaining", "pursuant",
    "aforementioned", "subsequent", "initial", "primary", "additional",
    "significant", "substantial", "considerable", "approximately",
    "fundamental", "essential", "critical", "crucial", "paramount",
    "comprehensive", "extensive", "numerous", "various", "multiple",
    "robust", "scalable", "seamless", "streamlined", "innovative",
    "sophisticated", "advanced", "enhanced", "optimized", "efficient",
    "multifaceted", "nuanced", "transformative", "holistic",
    "synergistic", "groundbreaking", "revolutionize", "paradigm",
    "plethora", "myriad",
}

_HEDGE_WORDS = {
    "perhaps", "maybe", "might", "could", "seems", "appears",
    "likely", "probably", "possibly", "seemingly", "presumably",
    "supposedly", "allegedly", "arguably",
}


# ---------------------------------------------------------------------------
# Syllable counter & Flesch
# ---------------------------------------------------------------------------
def _count_syllables(word: str) -> int:
    word = word.lower()
    count = len(re.findall(r"[aeiouy]+", word))
    if word.endswith("e") and count > 1:
        count -= 1
    return max(1, count)


def _flesch_reading_ease(text: str) -> float:
    sentences = sent_tokenize(text)
    words = [w for w in word_tokenize(text) if w.isalpha()]
    if not sentences or not words:
        return 50.0
    syllables = sum(_count_syllables(w) for w in words)
    asl = len(words) / len(sentences)
    asw = syllables / len(words)
    return 206.835 - 1.015 * asl - 84.6 * asw


# ---------------------------------------------------------------------------
# Feature extractors
# ---------------------------------------------------------------------------

def _get_sentences(text: str) -> list[str]:
    sents = sent_tokenize(text)
    return [s.strip() for s in sents if len(s.strip().split()) >= 3]


def _get_words(text: str) -> list[str]:
    return [w.lower() for w in word_tokenize(text) if w.isalpha()]


def _burstiness(sentences: list[str]) -> float:
    """CV of sentence lengths. AI: ~0.20–0.38 | Human: ~0.45–0.90."""
    lengths = [len(s.split()) for s in sentences]
    if len(lengths) < 3:
        return 0.5
    mean = statistics.mean(lengths)
    if mean == 0:
        return 0.0
    std = statistics.stdev(lengths)
    return std / mean


def _mattr(words: list[str], window: int = 50) -> float:
    """Moving Average Type-Token Ratio — lexical diversity."""
    if len(words) < window:
        return len(set(words)) / max(len(words), 1)
    ttrs = [
        len(set(words[i: i + window])) / window
        for i in range(len(words) - window + 1)
    ]
    return statistics.mean(ttrs)


def _ai_phrase_density(text_lower: str, word_count: int) -> tuple[float, list[str]]:
    found = [p for p in _AI_PHRASES_LOWER if p in text_lower]
    density = len(found) / max(word_count / 100, 1)
    return min(density, 2.0), list(dict.fromkeys(found))


def _personal_pronoun_ratio(words: list[str]) -> float:
    if not words:
        return 0.0
    return sum(1 for w in words if w in _PERSONAL_PRONOUNS) / len(words)


def _transition_density(words: list[str]) -> float:
    if not words:
        return 0.0
    return sum(1 for w in words if w in _TRANSITION_WORDS) / len(words)


def _formal_word_ratio(words: list[str]) -> float:
    content = [w for w in words if w not in _STOPWORDS]
    if not content:
        return 0.0
    return sum(1 for w in content if w in _FORMAL_WORDS) / len(content)


def _contraction_ratio(text: str, word_count: int) -> float:
    """Ratio of contractions to total words. Low = AI-like."""
    if word_count == 0:
        return 0.0
    return len(_CONTRACTION_RE.findall(text)) / word_count


def _opener_ai_ratio(sentences: list[str]) -> float:
    """Fraction of sentences that begin with AI-typical connector / framing words."""
    if not sentences:
        return 0.0
    count = 0.0
    for sent in sentences:
        parts = sent.split()
        if not parts:
            continue
        first = parts[0].lower().rstrip(",;:")
        first_two = " ".join(parts[:2]).lower() + " "
        if first in _AI_OPENER_WORDS:
            count += 1.0
        elif any(first_two.startswith(p) for p in _AI_OPENER_PHRASES):
            count += 0.8
    return count / len(sentences)


def _paragraph_coherence(text: str) -> float:
    """Cosine similarity between consecutive paragraphs. High = AI (overly coherent)."""
    paras = [p.strip() for p in re.split(r"\n{2,}", text) if len(p.strip().split()) > 10]
    if len(paras) < 2:
        return 0.5
    try:
        vec = TfidfVectorizer(stop_words="english", max_features=500)
        tfidf = vec.fit_transform(paras)
        sims = [
            float(cosine_similarity(tfidf[i], tfidf[i + 1])[0][0])
            for i in range(len(paras) - 1)
        ]
        return statistics.mean(sims) if sims else 0.5
    except Exception:
        return 0.5


def _sentence_entropy(sentences: list[str]) -> float:
    entropies = []
    for s in sentences:
        freq = Counter(s.lower())
        total = sum(freq.values())
        if total < 5:
            continue
        ent = -sum((c / total) * math.log2(c / total) for c in freq.values())
        entropies.append(ent)
    return statistics.mean(entropies) if entropies else 3.5


# ---------------------------------------------------------------------------
# Score calibration — stretches results away from 50 for better discrimination
# ---------------------------------------------------------------------------

def _calibrate(raw: float) -> float:
    """Mild nonlinear stretch to push human scores down and AI scores up."""
    c = raw - 50.0
    stretched = 50.0 + c * 1.18 + (c / 50.0) ** 3 * 10.0
    return max(0.0, min(100.0, stretched))


# ---------------------------------------------------------------------------
# Sentence-level scoring (per-sentence AI probability)
# ---------------------------------------------------------------------------

def _score_sentences(sentences: list[str]) -> list[SentenceScore]:
    results = []
    for sent in sentences:
        words = _get_words(sent)
        sent_lower = sent.lower()

        phrase_hits = sum(1 for p in _AI_PHRASES_LOWER if p in sent_lower)
        trans_hits = sum(1 for w in words if w in _TRANSITION_WORDS)
        pron_ratio = _personal_pronoun_ratio(words)
        formal_ratio = _formal_word_ratio(words)
        has_contraction = bool(_CONTRACTION_RE.search(sent))

        parts = sent.split()
        first = parts[0].lower().rstrip(",;:") if parts else ""
        first_two = " ".join(parts[:2]).lower() + " " if len(parts) >= 2 else ""
        ai_opener = first in _AI_OPENER_WORDS or any(
            first_two.startswith(p) for p in _AI_OPENER_PHRASES
        )

        score = 35.0
        score += min(phrase_hits * 20, 42)
        score += min(trans_hits * 10, 20)
        score -= pron_ratio * 260
        score += formal_ratio * 30
        if has_contraction:
            score -= 18
        if ai_opener:
            score += 12

        wc = len(words)
        if 15 <= wc <= 24:
            score += 8
        elif wc < 5 or wc > 40:
            score -= 12

        results.append(SentenceScore(text=sent, score=round(max(0.0, min(100.0, score)), 1)))
    return results


# ---------------------------------------------------------------------------
# Main detection entry point
# ---------------------------------------------------------------------------

def detect_ai(text: str) -> DetectResponse:
    sentences = _get_sentences(text)
    words = _get_words(text)
    text_lower = text.lower()

    word_count = len(words)
    sent_count = len(sentences)

    warning = None
    if word_count < 150:
        warning = "For best accuracy, provide at least 150 words. Short texts reduce reliability."

    # ── Raw features ──────────────────────────────────────────────────────────
    burst = _burstiness(sentences)
    mattr_val = _mattr(words)
    phrase_density, found_phrases = _ai_phrase_density(text_lower, word_count)
    pron_ratio = _personal_pronoun_ratio(words)
    trans_density = _transition_density(words)
    formal_ratio = _formal_word_ratio(words)
    coherence = _paragraph_coherence(text)
    contraction_ratio = _contraction_ratio(text, word_count)
    opener_ratio = _opener_ai_ratio(sentences)
    entropy_val = _sentence_entropy(sentences)
    readability = _flesch_reading_ease(text)

    sent_lengths = [len(s.split()) for s in sentences]
    avg_sent_len = statistics.mean(sent_lengths) if sent_lengths else 0

    phrase_raw = len(found_phrases)

    # ── Convert features → 0–100 AI subscores ────────────────────────────────

    # Burstiness: AI CV ≈ 0.20–0.38 → high AI score; Human CV ≈ 0.48–0.90 → low
    # CV=0.20→92, CV=0.35→63, CV=0.50→35, CV=0.65→6, CV=0.68+→0
    burst_ai = round(max(0.0, min(100.0, (0.68 - burst) / 0.52 * 100)), 1)

    # AI phrase density: 0 phrases → 0; 1/200w → ~34; 3/300w → ~73; 5+ → 100
    phrase_ai = round(min(100.0, phrase_density * 55.0 + min(phrase_raw * 6.0, 42.0)), 1)

    # MATTR: AI clusters at 0.72–0.82; low or high = more human
    mattr_ai = round(max(0.0, min(100.0, (1.0 - abs(mattr_val - 0.76) / 0.26) * 70.0)), 1)

    # Personal pronouns: very low → AI; high → human
    # ratio=0→88, ratio=0.025→44, ratio=0.055+→0
    pron_ai = round(max(0.0, min(100.0, (0.055 - pron_ratio) / 0.055 * 88.0)), 1)

    # Transition density: AI overuses specific connectors
    # density=0.006→24, 0.012→48, 0.020→80, 0.025+→100
    trans_ai = round(min(100.0, trans_density * 4000.0), 1)

    # Formal vocabulary: overly academic vocabulary → AI
    # ratio=0.05→45, 0.09→81, 0.12+→100
    formal_ai = round(min(100.0, formal_ratio * 900.0), 1)

    # Paragraph coherence: AI is suspiciously coherent between paragraphs
    coherence_ai = round(max(0.0, min(100.0, (coherence - 0.10) / 0.50 * 100.0)), 1)

    # Contraction absence: AI almost never uses contractions in formal text
    # ratio=0→85, ratio=0.010→54, ratio=0.020→24, ratio=0.028+→0
    contraction_ai = round(max(0.0, min(100.0, (0.028 - contraction_ratio) / 0.028 * 85.0)), 1)

    # Sentence opener repetition: AI overuses connector/framing openers
    # opener_ratio=0→0, 0.20→44, 0.35→77, 0.45+→100
    opener_ai = round(min(100.0, opener_ratio * 220.0), 1)

    # ── Weighted ensemble (weights sum to 1.0) ────────────────────────────────
    weights: dict[str, tuple[float, float]] = {
        "burstiness":         (0.20, burst_ai),
        "ai_phrases":         (0.24, phrase_ai),
        "contraction":        (0.09, contraction_ai),
        "personal_voice":     (0.09, pron_ai),
        "transition_density": (0.10, trans_ai),
        "opener_diversity":   (0.07, opener_ai),
        "formality":          (0.08, formal_ai),
        "sentence_structure": (0.07, mattr_ai),
        "coherence":          (0.06, coherence_ai),
    }

    raw_score = sum(w * s for w, s in weights.values())

    # Readability adjustment: AI ~45–68 Flesch; extreme values = more human
    if 45.0 <= readability <= 68.0:
        raw_score = min(100.0, raw_score * 1.03)
    elif readability > 80.0 or readability < 25.0:
        raw_score = max(0.0, raw_score * 0.93)

    # Apply nonlinear calibration to spread scores from the center
    total_score = round(_calibrate(raw_score), 1)

    # ── Verdict & confidence ──────────────────────────────────────────────────
    if total_score < 25:
        verdict, confidence = "Human Written", "High"
    elif total_score < 42:
        verdict, confidence = "Likely Human", "Medium"
    elif total_score < 58:
        verdict, confidence = "Uncertain", "Low"
    elif total_score < 72:
        verdict, confidence = "Likely AI", "Medium"
    elif total_score < 87:
        verdict, confidence = "AI Generated", "High"
    else:
        verdict, confidence = "AI Generated", "Very High"

    if word_count < 150:
        confidence = "Low"

    # ── Breakdown ─────────────────────────────────────────────────────────────
    breakdown: dict[str, MetricDetail] = {
        "burstiness": MetricDetail(
            score=burst_ai,
            label="Sentence Variation" if burst_ai < 50 else "Uniform Structure",
            description=f"Sentence length CV: {burst:.3f} — {'natural variation' if burst > 0.48 else 'suspiciously uniform (AI)'}",
            weight=0.20,
        ),
        "ai_phrases": MetricDetail(
            score=phrase_ai,
            label="AI Phrase Patterns",
            description=f"Found {phrase_raw} AI-signature phrases ({phrase_density:.2f} per 100 words)",
            weight=0.24,
        ),
        "contraction": MetricDetail(
            score=contraction_ai,
            label="Contraction Use" if contraction_ai < 50 else "No Contractions",
            description=f"Contraction ratio: {contraction_ratio:.4f} — {'human-like' if contraction_ratio > 0.015 else 'AI-like absence of contractions'}",
            weight=0.09,
        ),
        "personal_voice": MetricDetail(
            score=pron_ai,
            label="Personal Voice",
            description=f"First-person pronoun ratio: {pron_ratio:.3f} — {'impersonal (AI)' if pron_ratio < 0.01 else 'personal'}",
            weight=0.09,
        ),
        "transition_density": MetricDetail(
            score=trans_ai,
            label="Transition Words",
            description=f"Transition density: {trans_density:.4f} — {'overused (AI)' if trans_density > 0.010 else 'natural usage'}",
            weight=0.10,
        ),
        "opener_diversity": MetricDetail(
            score=opener_ai,
            label="Sentence Openers",
            description=f"AI-style openers: {opener_ratio:.1%} of sentences — {'repetitive AI pattern' if opener_ratio > 0.30 else 'varied openers'}",
            weight=0.07,
        ),
        "formality": MetricDetail(
            score=formal_ai,
            label="Formality Level",
            description=f"Formal word ratio: {formal_ratio:.3f} — {'overly formal (AI)' if formal_ratio > 0.08 else 'conversational'}",
            weight=0.08,
        ),
        "sentence_structure": MetricDetail(
            score=mattr_ai,
            label="Lexical Diversity",
            description=f"MATTR score: {mattr_val:.3f} — {'typical AI range' if 0.70 <= mattr_val <= 0.85 else 'varied vocabulary'}",
            weight=0.07,
        ),
        "coherence": MetricDetail(
            score=coherence_ai,
            label="Paragraph Coherence",
            description=f"Inter-paragraph similarity: {coherence:.3f} — {'suspiciously consistent (AI)' if coherence > 0.40 else 'natural flow'}",
            weight=0.06,
        ),
    }

    stats: dict[str, Any] = {
        "word_count": word_count,
        "sentence_count": sent_count,
        "avg_sentence_length": round(avg_sent_len, 1),
        "burstiness": round(burst, 3),
        "mattr": round(mattr_val, 3),
        "flesch_reading_ease": round(readability, 1),
        "ai_phrases_count": phrase_raw,
        "personal_pronoun_ratio": round(pron_ratio, 4),
    }

    sentence_scores = _score_sentences(sentences)

    return DetectResponse(
        score=total_score,
        verdict=verdict,
        confidence=confidence,
        breakdown=breakdown,
        ai_phrases_found=found_phrases[:15],
        sentences=sentence_scores,
        stats=stats,
        warning=warning,
    )
