import os
import random
import io
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

CARDS_DIR = Path(__file__).parent / "cards"

SUIT_NAMES = {
    "Major Arcana": "Major Arcana",
    "Dynamism": "Dynamism",
    "Pattern": "Pattern",
    "Primordialism": "Primordialism",
    "Questing": "Questing",
}

CARD_DATA = {
    # ── MAJOR ARCANA ──────────────────────────────────────────────────
    "0 Fool":            {"upright": "New beginnings and infinite potential. The soul leaps into the unknown with reckless faith — a fresh Awakening.",          "reversed": "Recklessness without wisdom. Paradox accumulates because the mage acts before understanding the cost.",                                    "keywords": "Possibility, Courage, Enthusiasm, Creative Expression, Risk, Adventure",                                    "tradition": "Marauders"},
    "1 Mage":            {"upright": "Will, creativity, and mastery. The Mage shapes reality through focused intent and raw Quintessence.",                       "reversed": "Willpower turned inward against itself. Talent squandered, workings backfiring, potential locked behind ego.",                            "keywords": "Will, Communication, Natural Gift, Memory, Clarity, Organization, Invention, Originality",               "tradition": "Virtual Adepts"},
    "1 Cover Mage":      {"upright": "Will, creativity, and mastery. The Mage shapes reality through focused intent and raw Quintessence.",                       "reversed": "Willpower turned inward against itself. Talent squandered, workings backfiring, potential locked behind ego.",                            "keywords": "Will, Communication, Natural Gift, Memory, Clarity, Organization, Invention, Originality",               "tradition": "Virtual Adepts"},
    "2 High Priestess":  {"upright": "Intuition and inner wisdom. She guards the threshold between the conscious mind and the Umbra.",                            "reversed": "Hidden knowledge withheld or misread. The mage ignores their instincts and pays for it dearly.",                                         "keywords": "Enlightenment, Intuition, Independence, Meditation, Growth, Awareness, Mystery, Inner Illumination",     "tradition": "Dreamspeakers"},
    "03 The Empress":    {"upright": "Fertility, abundance, and creativity. Life flows through her — the Tapestry made manifest and generous.",                   "reversed": "Stagnation and creative block. The flow of Quintessence is dammed; growth turns inward and rots.",                                        "keywords": "Fertility, Wisdom, Earth Mother, Healing, Nurturing, Emotion, Creation, Cycles, Balance",                "tradition": "Verbena"},
    "4 Tarot Emperor":   {"upright": "Authority, structure, and order. He enforces the patterns that hold reality in place — Tradition or Technocracy.",          "reversed": "Tyranny and rigid control. A paradigm so hardened it cannot adapt — and cracks under the pressure.",                                      "keywords": "Governance, Leadership, Power, Decisions, Action, Inspiration, Motivation, Foundation, Mastery",         "tradition": "Order of Hermes"},
    "5 The Heirophant":  {"upright": "Tradition, spiritual guidance, and institutional wisdom. The keeper of inherited paradigms.",                               "reversed": "Dogma mistaken for truth. A Tradition that has forgotten why its rules exist — hollow ritual, no power.",                                  "keywords": "Morality, Learning, Teaching, Wisdom, Sacred, Initiation, Devotion, Intent, Focus, Community",           "tradition": "Celestial Chorus"},
    "6 The Lovers":      {"upright": "Love, harmony, and important choices. A crossroads where the heart and the soul must align.",                               "reversed": "Misaligned values and poor choices. A working built on a false premise — or a bond that costs too much.",                                  "keywords": "Attraction, Relationship, Loyalty, Passion, Devotion, Duality, Sincerity, Openness, Romance, Harmony",  "tradition": "Cult of Ecstasy"},
    "7 The Chariot":     {"upright": "Victory and willpower. The mage who masters inner conflict rides it as momentum to reshape the world.",                     "reversed": "Loss of control. Forces once harnessed now pull in opposite directions — the chariot veers off the road.",                                 "keywords": "Victory, Change, Movement, Growth, Evolution, Progress, Opportunity, Exploration, Conquest",              "tradition": "Sons of Ether"},
    "8 Strength":        {"upright": "Inner strength, patience, and compassion. True power comes from taming the beast within, not destroying it.",               "reversed": "Self-doubt and suppressed power. The mage fears their own Avatar — or lets it run unchecked.",                                            "keywords": "Power, Passion, Creativity, Risk, Charisma, Rebirth, Expression, Overcoming Fears, Faith, Intuition",   "tradition": "Quintessence"},
    "9 The Hermit":      {"upright": "Inner seeking, solitude, and wisdom. He walks the long road alone, lantern held high for others to follow.",                "reversed": "Isolation that has become a trap. Wisdom hoarded instead of shared; the Seeking turned to withdrawal.",                                     "keywords": "Guidance, Completion, Introspection, Contemplation, Experience, Wisdom, Courage, Seeking",               "tradition": "Hollow Ones"},
    "10 Wheel Fortune":  {"upright": "Cycles, fate, and turning points. The Wheel spins — even the Traditions rise and fall in their time.",                      "reversed": "Resisting the inevitable turn. Clinging to a paradigm past its moment; the Wheel grinds rather than lifts.",                              "keywords": "Fate, Opportunity, Breakthrough, Prosperity, Abundance, Flexibility, Fortune, Luck, Cycles",              "tradition": "Euthanatos"},
    "11 Justice":        {"upright": "Justice, balance, and cause and effect. Every working leaves a mark on the Tapestry — account for it.",                     "reversed": "Imbalance and denied consequences. Paradox ignored builds silently until the Tapestry tears back.",                                        "keywords": "Justice, Alignment, Balance, Truth, Clarity, Order, Seeing Illusions, Harmony",                          "tradition": "Akashic Brotherhood"},
    "12 The Hanged Man": {"upright": "Surrender and a new perspective. Wisdom is found by hanging still in the in-between, releasing control.",                   "reversed": "Martyrdom without meaning. Sacrifice made out of stubbornness rather than insight — stagnation disguised as patience.",                   "keywords": "Perspective, Surrender, Breaking Old Patterns, Freedom, Unlimited Life Force, Deep Spiritual Wisdom",    "tradition": "Paradox"},
    "13 Death":          {"upright": "Transformation and new beginnings. The Reaper clears the old paradigm so something truer can emerge.",                      "reversed": "Resisting necessary change. Clinging to a dead paradigm out of fear — decay instead of transformation.",                                   "keywords": "Rebirth, Liberation, Letting Go, Transformation, Expanding Consciousness, Emergence, Cycles, Change",    "tradition": "Vampire; Awakening"},
    "14 Temperance":     {"upright": "Balance, moderation, and purpose. The alchemist blends opposing forces into something neither could be alone.",              "reversed": "Excess and imbalance. Spheres pushed too hard, too fast — burnout, Quiet, or Paradox backlash.",                                          "keywords": "Harmony, Integration, Synergy, Unity, Experience, Alchemy, Moderation, Dream, Vision, Self Control",     "tradition": "Technocracy"},
    "15 The Devil":      {"upright": "Bonds and shadow self. The Technocracy's grip on the Sleepers — or the chains the mage forged themselves.",                 "reversed": "Breaking free from conditioning. Recognizing the chains as illusion; the first breath after paradigm collapse.",                          "keywords": "Bondage, Materialism, Ties, Sensation, Enchantment, Seduction, Dominion",                                "tradition": "The Wyrm; Nephandi"},
    "16 The Tower":      {"upright": "Sudden upheaval and liberation. When a false paradigm shatters, the fall is violent — but freeing.",                        "reversed": "Disaster prolonged by denial. The Tower should have fallen; instead it leans, threatening everything below it.",                          "keywords": "Purification, Ambition, Restoration, Change, Restructuring, Awakening, Recovery, Expansion, Alignment",  "tradition": "The Chantry"},
    "17 The Star":       {"upright": "Hope, inspiration, and renewal. After the storm, a quiet light guides the weary mage toward Ascension.",                    "reversed": "Lost faith and disillusionment. The mage has seen too much — the Star still shines but they can no longer see it.",                      "keywords": "Inspiration, Trust, Self-respect, Talent, Guidance, Creativity, Manifestation, Hope, Success",           "tradition": "Meditation"},
    "18 Luna":           {"upright": "Intuition, the unconscious, and illusion. The Moon hides as much as it reveals — trust your instincts carefully.",           "reversed": "Confusion and self-deception. The mage mistakes their own fears for reality, and acts on shadows.",                                        "keywords": "Intuition, Femininity, Receptivity, Reflection, Mystery, Romance, Discovering True Nature",               "tradition": "Quiet; Inner Tuition"},
    "19 The Sun":        {"upright": "Joy, success, and enlightenment. Pure Quintessence radiates outward — reality sings in harmony.",                           "reversed": "Overconfidence and blind optimism. The light is real, but the mage is flying too close to it.",                                           "keywords": "Freedom, Cooperation, Teamwork, Unlimited Energy, Motivation, Enthusiasm, Shared Visions, Success",      "tradition": "The Sun"},
    "20 Judgement":      {"upright": "Awakening, rebirth, and higher calling. The final Seeking before Ascension — the Avatar demands an answer.",                 "reversed": "Refusing the call. The mage hears the summons but turns away — and the Avatar's pressure intensifies.",                                    "keywords": "Reunion, Awakening, Consciousness, Discernment, Judgment, Perception, Insight, Integration, Manifestation", "tradition": "Avatar"},
    "21 Gaia":           {"upright": "Completion, wholeness, and Ascension. The mage has walked every path; the Tapestry and the self are one.",                  "reversed": "Almost there — but not yet. Success without integration; the final step held back by something unresolved.",                              "keywords": "Fulfillment, Reward, Freedom, Wholeness, Completion, Integration, Unification, Awareness, Vision",        "tradition": "The Tellurian"},
    # ── DYNAMISM (Air / Marauders) ────────────────────────────────────
    "1 Ace of Dynamism":      {"upright": "A spark of pure creative force. Unlimited potential waiting to ignite a new working or paradigm.",                     "reversed": "Creative energy blocked or misdirected. The spark smothered before it can catch — or igniting in the wrong place.",                      "keywords": "Knowledge, Conquest, Victory, Clarity, Inventiveness, Originality",                                      "tradition": "Innovation"},
    "2 of Dynamism":          {"upright": "Balance of opposing energies. Two forces held in tension, each strengthening the other.",                              "reversed": "Imbalance and overextension. The mage tries to manage too many workings at once — something will slip.",                                   "keywords": "Unease, Betrayal, Blindness, Decision, Peace, Integrated Mind",                                           "tradition": "Resolution"},
    "3 of Dynamism":          {"upright": "First fruits of creative effort. Early success that hints at the full power yet to be unlocked.",                      "reversed": "Premature celebration. The working shows promise but is not yet stable — overconfidence invites Paradox.",                                 "keywords": "Grief, Upheaval, Negativity, Limited View, Focus, Jealousy",                                              "tradition": "Separation"},
    "4 of Dynamism":          {"upright": "Celebration and foundation. A moment of earned rest before the next Seeking begins.",                                  "reversed": "Complacency and stagnation. Resting too long on past successes while the world moves on without you.",                                     "keywords": "Reality, Healing, Silence, Conflict Resolution, Truce, Rest",                                             "tradition": "Repose"},
    "5 of Dynamism":          {"upright": "Conflict and competition. Clashing paradigms that spark growth through friction — embrace the struggle.",               "reversed": "Pointless conflict with no winner. Energy burned on ego-driven battles that serve no higher purpose.",                                     "keywords": "Defeat, Decay, Injustice, Constraint, Fear, Distortion, Hollow Victory",                                 "tradition": "Dishonor"},
    "6 of Dynamism":          {"upright": "Victory and generosity. Power shared freely amplifies rather than diminishes — the Tradition grows stronger.",          "reversed": "Arrogance in victory. Winning that creates resentment; power hoarded instead of shared.",                                                 "keywords": "Transition, Journey, Travel, Rationality, Impartiality, Considering the Whole",                           "tradition": "Synthesis"},
    "7 of Dynamism":          {"upright": "Defiance and perseverance. Standing your ground against those who would unmake your reality.",                          "reversed": "Defensiveness masking weakness. The mage fights on out of stubbornness, unable to admit the position is lost.",                            "keywords": "Imbalance, Inefficiency, Insecurity, Helplessness, Despair, Sabotage, Lies",                              "tradition": "Betrayal"},
    "8 of Dynamism":          {"upright": "Swift momentum and clarity of purpose. Energy channeled so precisely it becomes unstoppable.",                          "reversed": "Burnout and scattered focus. Moving too fast without direction — power wasted on motion that goes nowhere.",                                 "keywords": "Crisis, Indecision, Constraint, Censorship, Doubt, Distrust, Confusion",                                  "tradition": "Captivity"},
    "9 of Dynamism":          {"upright": "Resilience under pressure. Battle-hardened will that bends but never breaks — scars as proof of survival.",             "reversed": "Paranoia born from past wounds. The mage is ready for a fight that is not coming — exhausted by their own vigilance.",                    "keywords": "Despair, Misery, Ruin, Catastrophe, Self-criticism, Mental Torment",                                      "tradition": "Suffering"},
    "10 of Dynamism":         {"upright": "The weight of accumulated power. Mastery achieved, but the burden of it grows heavier each day.",                      "reversed": "Collapse under the weight. Too much responsibility, too little support — the working unravels from the inside.",                           "keywords": "Ruin, Pain, Mental Despair, Paradox, Fear, Illusion",                                                     "tradition": "Failure"},
    "11 Page of Dynamism":    {"upright": "Curiosity and creative hunger. A young mage who sees every obstacle as an experiment to run.",                          "reversed": "Reckless experimentation without grounding. Paradox accumulates faster than wisdom can manage it.",                                        "keywords": "Aggression, Activation, Ferocity, Practical Concrete Thinking, Taking Action",                            "tradition": "Battle"},
    "12 Knight of Dynamism":  {"upright": "Headlong charge into the unknown. Reckless brilliance that reshapes the world in its wake.",                           "reversed": "Impulsiveness that destroys what it meant to build. The charge has no direction — only speed.",                                           "keywords": "Impulsiveness, Courage, Intuitive Thinking, Unconstrained Mind",                                          "tradition": "Wrath"},
    "13 King of Dynamism":    {"upright": "Commanding creative vision. A master who bends the flow of events with effortless authority.",                          "reversed": "Tyrannical imposition of vision. Brilliance that brooks no other perspective — the king burns those who disagree.",                        "keywords": "Judgment, Counsel, Wisdom, Focus, Intent, Concentration",                                                 "tradition": "Determination"},
    "14 Queen of Dynamism":   {"upright": "Vibrant and magnetic leadership. She inspires others to burn brighter than they thought possible.",                     "reversed": "Volatile and unpredictable. Her fire gives light — but also burns those who get too close.",                                               "keywords": "Perception, Trust, Rationality, Impartiality, Counseling Intelligence",                                   "tradition": "Observation"},
    # ── PATTERN (Earth / Technocracy) ────────────────────────────────
    "1 Ace of Pattern":       {"upright": "The seed of perfect order. A pristine template from which all structure unfolds.",                                      "reversed": "Order imposed where it does not belong. A paradigm too rigid to hold living reality inside it.",                                           "keywords": "Prosperity, Inheritance, Production, Practical Organization",                                             "tradition": "The Syndicate"},
    "2 Pattern":              {"upright": "Careful weighing of choices. Two paths, both real — precision matters before the first step.",                          "reversed": "Indecision and analysis paralysis. The mage studies every angle but never commits to a working.",                                         "keywords": "Balance, Change, Harmony, Yin/Yang, Stability, Adaptability",                                             "tradition": "Speculation"},
    "3 Pattern":              {"upright": "Skill made tangible. Craft and planning paying off in something beautifully constructed.",                              "reversed": "Poor collaboration or shoddy work. The structure looks sound but is riddled with hidden flaws.",                                           "keywords": "Effort, Perseverance, Tenacity, Priorities, Commitments, Focus, Intent, Direction",                       "tradition": "Construction"},
    "4 Pattern":              {"upright": "Security and consolidation. Holding what has been built while watching for cracks in the foundation.",                  "reversed": "Greed and excessive control. Hoarding resources or knowledge at the cost of the Tradition's health.",                                     "keywords": "Inheritance, Greed, Endurance, Power, Vitality, Empowerment, Possession",                                 "tradition": "Direction"},
    "5 Pattern":              {"upright": "Loss and hardship that carries a lesson. The pattern frays — but the unraveling reveals what was weak.",                "reversed": "Refusing to learn from loss. The same mistake repeated; the pattern breaks in the same place again.",                                    "keywords": "Poverty, Ruin, Loss, Loneliness, Worry, Anxiety",                                                         "tradition": "Anxiety"},
    "6 Pattern":              {"upright": "Generosity and flow. Resources move where they are needed; the pattern breathes and stays alive.",                     "reversed": "Debt and strings attached. Generosity with a hidden price — or charity that creates dependence.",                                         "keywords": "Philanthropy, Helpfulness, Success, Produce, Productivity, Concreteness",                                 "tradition": "Gifts"},
    "7 Pattern":              {"upright": "Patience and long-term assessment. The harvest is worth more than the quick gain — wait for it.",                       "reversed": "Impatience and poor investment. Chasing short-term results that hollow out long-term power.",                                              "keywords": "Reassessment, Indecision, Failure, Fear of Success, Delay",                                               "tradition": "Stress"},
    "8 Pattern":              {"upright": "Focused diligence. Mastery approached one careful, deliberate repetition at a time.",                                  "reversed": "Drudgery without growth. Repetition as habit, not craft — the mage goes through motions without advancement.",                            "keywords": "Skill, Artistry, Prudence, Attention to Detail, Organization",                                            "tradition": "Employment"},
    "9 Pattern":              {"upright": "Self-sufficiency and quiet achievement. Everything needed has been carefully and quietly gathered.",                     "reversed": "Isolation born of self-reliance taken too far. Independence hardened into an inability to accept help.",                                    "keywords": "Gain, Prudence, Utility, Balance, Order, Organization, Unification",                                       "tradition": "Profit"},
    "10 Pattern":             {"upright": "Abundance and legacy. The pattern complete — wealth, stability, and something to pass on to the next generation.",      "reversed": "Burden of legacy. Inherited obligations that crush the heir; abundance that has become a gilded cage.",                                    "keywords": "Stability, Wealth, Abundance, Prosperity, Enrichment",                                                    "tradition": "Wealth"},
    "11 Page of Pattern":     {"upright": "Studious and methodical curiosity. She dissects every system to understand it from the inside out.",                    "reversed": "Over-analysis and missed experience. So focused on understanding the map that she never walks the territory.",                              "keywords": "Tenacity, Care, Creativity, Mutation, Incubation",                                                        "tradition": "Void Engineers"},
    "12 Knight of Pattern":   {"upright": "Relentless, methodical pursuit. He advances without hurry and without stopping — slow and inevitable.",                 "reversed": "Inflexibility in the face of change. The methodical approach applied to situations that demand improvisation.",                            "keywords": "Reliability, Patience, Methodology, Physicality, Architect, Reform, Endurance",                           "tradition": "Iteration X"},
    "13 King pattern":        {"upright": "Disciplined mastery of material reality. His word is architecture; his will is law made solid.",                        "reversed": "Authoritarian rigidity. A ruler who cannot distinguish between order and control — the pattern calcifies.",                                 "keywords": "Industry, Endurance, Prosperity, Harvest, Abundance, Practicality, Finance",                              "tradition": "New World Order"},
    "14 Queen of Pattern":    {"upright": "Practical wisdom and quiet abundance. She builds worlds that outlast her — and knows exactly how.",                     "reversed": "Controlling and mistrustful. Practical wisdom curdled into suspicion; she manages everything because she trusts nothing.",                 "keywords": "Creativity, Talent, Fertility, Health, Nurturing, Stability, Contentment",                                "tradition": "Progenitors"},
    # ── PRIMORDIALISM (Water / Nephandi) ──────────────────────────────
    "1 Ace of Primordialism":    {"upright": "The raw power of nature unbound. Primal force before it is named or shaped — pure Life and Spirit.",                "reversed": "Primal force without direction. Wild energy that destroys rather than renews — instinct without wisdom.",                                  "keywords": "Breakthrough, Vitality, Open Heart, Spiritual Heart, Expression",                                         "tradition": "Feeling"},
    "2 of Primordialism":        {"upright": "Dueling instincts and elemental tension. Two ancient forces negotiate an uneasy but necessary truce.",              "reversed": "Inner conflict tearing the mage apart. Natural forces in the working pulling against each other destructively.",                          "keywords": "Reflection, Lust, Passion, Love",                                                                         "tradition": "Symbiosis"},
    "3 of Primordialism":        {"upright": "Collaboration rooted in primal trust. Three forces weave together something none of them could create alone.",       "reversed": "Distrust and territorial conflict. Natural allies fail to cooperate — the ecosystem collapses inward.",                                   "keywords": "License, Excess Indulgence, Abundance",                                                                   "tradition": "Carnality"},
    "4 of Primordialism":        {"upright": "Stillness and primal sanctuary. The wild at rest, conserving strength for what comes next.",                        "reversed": "Stagnation mistaken for peace. The sanctuary has become a cage; nothing grows, nothing moves.",                                           "keywords": "Dissipation, Emotional Luxury, Satisfaction, Indifference",                                               "tradition": "Ennui"},
    "5 of Primordialism":        {"upright": "Elemental conflict and upheaval. The natural order disrupted — painful, but necessary for renewal.",                 "reversed": "Destruction without renewal. The conflict leaves only ash — no seeds remain to grow from the ruin.",                                     "keywords": "Disappointment, Grief, Sorrow, Loss, Vulnerability, Depression",                                          "tradition": "Vulnerability"},
    "6 of Primordialism":        {"upright": "Harmony of natural cycles. Giving and receiving in rhythm with the living world — the web holds.",                  "reversed": "Disrupted cycles and imbalance. The natural flow broken; taking without returning, until the web tears.",                                  "keywords": "Beginnings, Pleasure, Rebirth, Invigoration, Memory, Enthusiasm",                                         "tradition": "Opportunity"},
    "7 of Primordialism":        {"upright": "Primal courage and instinct. Facing the unknown with the fearless clarity of a predator in its element.",           "reversed": "Fear and paralysis when instinct fails. The mage is out of their natural element — every shadow becomes a threat.",                        "keywords": "Seduction, Selfishness, Illusion, Debauchery, Addiction, Immorality",                                     "tradition": "Indulgence"},
    "8 of Primordialism.tif":    {"upright": "Untamed swiftness. Movement so natural it becomes invisible — pure instinct in perfect motion.",                    "reversed": "Restless and directionless movement. Speed without purpose; fleeing rather than pursuing.",                                                 "keywords": "Abandonment, Rejection, Misery, Laziness, Limits, Exhaustion, Withdrawal",                                "tradition": "Stagnation"},
    "9 of Primordialism":        {"upright": "Primal strength tested and proven. The lone survivor, scarred but unbroken by everything the wild threw.",           "reversed": "Isolation that has become a wound. Survival instinct so dominant the mage can no longer form bonds.",                                     "keywords": "Success, Achievement, Health, Opportunity, Expansion, Satisfaction, Prosperity",                          "tradition": "Possession"},
    "10 of Primordialism":       {"upright": "Overwhelming primal force fully unleashed. The weight of the natural world behind a single working.",               "reversed": "Crushed by primal forces beyond control. The working called powers that cannot be channeled — only endured.",                              "keywords": "Satisfaction, Emotional Contentment, Vitality, Expression, Energy, Enthusiasm",                           "tradition": "Satisfaction"},
    "11 Page of Primordialism":  {"upright": "Wild and eager apprentice. She learns by doing — touching fire to know it burns, and doing it again.",              "reversed": "Reckless and ungrounded. All instinct and no patience — she provokes forces she cannot yet survive.",                                     "keywords": "Rebirth, Emotional Objectivity, Control, Carrying Messages from Dreams",                                   "tradition": "Possession"},
    "12 Knight of Primordialism":{"upright": "Fierce champion of the natural world. He rides the storm and calls it home — nothing stops him.",                   "reversed": "Destructive force with no anchor. The storm with no eye; violence without the calm at its center.",                                       "keywords": "Emotion, Desire, Tantric Practices, Passion, Happiness",                                                  "tradition": "Bestiality"},
    "13 King of Primordialism":  {"upright": "Ancient and sovereign force of nature. He does not rule the wild — he is the wild, fully realized.",                "reversed": "Primal rage without wisdom. The king consumed by his own power — the forest burning, the beast unchained.",                                "keywords": "Power, Emotional Loyalty, Spontaneity, Ego, Generosity, Responsibility",                                  "tradition": "Vanity"},
    "14 Queen of Primordialism": {"upright": "Nurturing and formidable in equal measure. She protects her domain with fierce, patient love.",                     "reversed": "Smothering overprotection. Love that controls rather than frees; nature as a prison rather than a home.",                                  "keywords": "Imagination, Emotional Honesty, Self-reflection, New Identity, Non-judgmental Expression",                "tradition": "Perversity"},
    # ── QUESTING (Fire / Traditions) ──────────────────────────────────
    "1 Ace of Questing":      {"upright": "The call to adventure and purpose. A new Seeking begins — the road opens wide before the mage.",                       "reversed": "The call ignored or delayed. The mage hears the summons but hesitates — and the window begins to close.",                                  "keywords": "Birth, Creativity, Self-realization, Seeking, Truth, Elusive Life Force, Awakening",                      "tradition": "Beginnings; Ahl-i-Batin"},
    "2 of Questing.tif":      {"upright": "Bold vision and early resolve. Standing at the edge of the known, planning the leap with clear eyes.",                 "reversed": "Restlessness and lack of direction. Plans made without commitment; the horizon stared at but never crossed.",                              "keywords": "Mastery, Management, Initiative, Sovereignty, Power, Unification",                                        "tradition": "Sphere of Forces; Order of Hermes"},
    "3 of Questing":          {"upright": "Expansion and foresight. The first steps have been taken; now the horizon grows vast with possibility.",                "reversed": "Delays and setbacks on the path. The quest stalls before it truly begins — obstacles underestimated.",                                     "keywords": "Virtue, Cooperation, Partnership, Honesty, Consistency, Harmony",                                         "tradition": "Sphere of Prime; Celestial Chorus"},
    "4 of Questing":          {"upright": "Joyful homecoming and earned celebration. The quest complete — for now. Rest is part of the Seeking.",                 "reversed": "Instability beneath the celebration. The homecoming is forced or the victory hollow — something remains unresolved.",                      "keywords": "Celebration, Completion, Peace, Victory, Happiness, Success, New Beginnings, Wholeness",                  "tradition": "Sphere of Time; Cult of Ecstasy"},
    "5 of Questing":          {"upright": "Strife and competing ambitions. Fellow seekers clashing — friction that sharpens everyone involved.",                   "reversed": "Pointless conflict born of ego. The clashing serves no one; the Seeking fractures into petty rivalry.",                                    "keywords": "Conflict, Competition, Obstacles, Anxiety, Disappointment, Overactivity",                                 "tradition": ""},
    "6 of Questing":          {"upright": "Triumph and recognition. The road was hard; the return is glorious — and the Tradition takes notice.",                  "reversed": "Delayed recognition or false triumph. The victory celebrated prematurely; or success claimed by another.",                                  "keywords": "Victory, Success, Progress, Invigoration, Energy, Expansion",                                             "tradition": "Sphere of Life; Verbena"},
    "7 of Questing":          {"upright": "Holding the high ground. Defending a hard-won position against those who would claim it as their own.",                 "reversed": "Defensiveness and paranoia. The mage cannot tell allies from enemies — and alienates both in the process.",                                 "keywords": "Courage, Development, Purpose, Energy, Excellence, Vision, Value",                                        "tradition": "Sphere of Mind; Akashic Brotherhood"},
    "8 of Questing":          {"upright": "Rapid progress and decisive momentum. Events accelerate — the quest nears its climax at last.",                         "reversed": "Misdirected energy and hasty action. Moving fast in the wrong direction; speed that outpaces judgment.",                                    "keywords": "Movement, Journey, Ideas, Agility, Progress, Communication, Transformation, Problem Solving",              "tradition": "Sphere of Matter; Sons of Ether"},
    "9 of Questing":          {"upright": "Tested resolve on the final stretch. Every wound earned; every step still chosen freely — nearly there.",               "reversed": "Giving up when the end is close. Exhaustion winning over will; the last mile abandoned before it is walked.",                              "keywords": "Spirit, Preparation, Defense, Success, Vision, Spiritual and Intuitive Power, Unlimited Power",           "tradition": "Sphere of Spirit; Dreamspeakers"},
    "10 of Questing":         {"upright": "The burden of an overloaded quest. Too many obligations — but the seeker's shoulders are stronger than they know.",     "reversed": "Collapse under the weight of too much. The quest has become a burden; delegation is not weakness, it is wisdom.",                          "keywords": "Oppression, Burden, Trial, Ruin, Disruption, Failure, Limitation, Withdrawal",                            "tradition": "Sphere of Entropy; Euthanatos"},
    "11 Page of Questing":    {"upright": "Adventurous and endlessly curious. He sprints toward every horizon just to see what lies beyond.",                      "reversed": "Scattered enthusiasm without follow-through. Every new horizon abandoned for the next — no quest ever completed.",                          "keywords": "Brilliance, Learning, Courage, Beauty, Self-freedom, Spontaneous Expression, Freedom, Adventure",         "tradition": "Discovery"},
    "12 Knight of Questing":  {"upright": "Passionate and visionary crusader. She quests not for glory but because the cause demands it.",                         "reversed": "Fanaticism and tunnel vision. The crusade becomes the end in itself — the cause forgotten in the fervor.",                                  "keywords": "Conflict, Haste, Inspiring Creativity, Expression, Concentration, Expansion",                             "tradition": "Impetuousness"},
    "13 King of Questing":    {"upright": "Charismatic leader and master of purpose. His quest becomes the quest of everyone around him.",                         "reversed": "Overbearing vision that crushes others. The king's purpose so consuming it leaves no room for anyone else's.",                              "keywords": "Authority, Leadership, Inspiring Direction, Vision, Intuition, Evolution, Spiritual Growth, Energy",      "tradition": "Purpose"},
    "14 Queen of Questing":   {"upright": "Confident and warmly courageous. She knows her path and welcomes others to walk beside her.",                           "reversed": "Overconfidence and impatience with others. She charges ahead and wonders why no one can keep pace.",                                       "keywords": "Control, Command, Attraction, Honor, Self-knowledge, Transformation, Choice, Fluidity, Growth",           "tradition": "Aspiration"},
}

def load_all_cards() -> list[dict]:
    cards = []
    extensions = {".tif", ".tiff", ".png", ".jpg", ".jpeg"}
    for suit_dir in CARDS_DIR.iterdir():
        if not suit_dir.is_dir():
            continue
        suit = suit_dir.name
        for card_file in suit_dir.iterdir():
            if card_file.suffix.lower() in extensions:
                # Strip extension and trailing dots for display name
                stem = card_file.stem.rstrip(".")
                # Skip alternate versions to avoid duplicates (keep originals)
                if "alternate" in stem.lower():
                    continue
                cards.append({
                    "name": stem,
                    "suit": suit,
                    "path": card_file,
                })
    return cards


ALL_CARDS = load_all_cards()


def card_to_discord_file(card: dict) -> tuple[discord.File, str]:
    """Convert a card image to a Discord-sendable PNG file."""
    with Image.open(card["path"]) as img:
        img = img.convert("RGB")
        # Resize to a reasonable Discord embed size (max 800px wide)
        max_width = 600
        if img.width > max_width:
            ratio = max_width / img.width
            img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
    filename = f"{card['suit']}_{card['name']}.png".replace(" ", "_")
    return discord.File(buf, filename=filename), filename


def build_card_embed(card: dict, index: int, total: int, filename: str, reversed: bool = False) -> discord.Embed:
    suit_emojis = {
        "Major Arcana": "🌟",
        "Dynamism": "⚡",
        "Pattern": "🔷",
        "Primordialism": "🌿",
        "Questing": "⚔️",
    }
    emoji = suit_emojis.get(card["suit"], "🃏")
    orientation_tag = " *(Reversed)*" if reversed else ""
    title = f"{emoji} {card['name']}{orientation_tag}"
    if total > 1:
        title = f"Card {index}/{total} — {title}"

    data = CARD_DATA.get(card["name"], {})
    orientation = "reversed" if reversed else "upright"
    meaning = data.get(orientation, "")
    keywords = data.get("reversedKeywords" if reversed else "keywords", "")
    tradition = data.get("tradition", "")

    embed = discord.Embed(
        title=title,
        description=meaning if meaning else discord.utils.MISSING,
        color=discord.Color.dark_purple(),
    )
    if keywords:
        embed.add_field(name="Keywords", value=keywords, inline=False)
    if tradition:
        embed.add_field(name="Tradition / Relation", value=tradition, inline=True)

    footer_parts = [f"Suit: {card['suit']}", "Mage Tarot Cards (1st ed)"]
    if reversed:
        footer_parts.insert(0, "🔄 Reversed")
    embed.set_footer(text=" · ".join(footer_parts))
    embed.set_image(url=f"attachment://{filename}")
    return embed


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree


@bot.event
async def on_ready():
    await tree.sync()
    print(f"{bot.user} olarak giriş yapıldı. {len(ALL_CARDS)} kart yüklendi.")


@tree.command(name="tarot", description="Rastgele Mage Tarot kartı çek")
@app_commands.describe(adet="Kaç kart çekmek istiyorsun? (1, 3 veya 5)")
@app_commands.choices(adet=[
    app_commands.Choice(name="1 kart", value=1),
    app_commands.Choice(name="3 kart", value=3),
    app_commands.Choice(name="5 kart", value=5),
])
async def tarot(interaction: discord.Interaction, adet: app_commands.Choice[int] = None):
    count = adet.value if adet else 1
    await interaction.response.defer()

    drawn = random.sample(ALL_CARDS, min(count, len(ALL_CARDS)))

    files = []
    embeds = []
    for i, card in enumerate(drawn, 1):
        is_reversed = random.random() < 0.5
        file, filename = card_to_discord_file(card)
        embed = build_card_embed(card, i, len(drawn), filename, reversed=is_reversed)
        files.append(file)
        embeds.append(embed)

    await interaction.followup.send(embeds=embeds, files=files)


@tree.command(name="tarot_suit", description="Belirli bir takımdan rastgele kart çek")
@app_commands.describe(takim="Hangi takımdan kart çekmek istiyorsun?")
@app_commands.choices(takim=[
    app_commands.Choice(name="Major Arcana 🌟", value="Major Arcana"),
    app_commands.Choice(name="Dynamism ⚡", value="Dynamism"),
    app_commands.Choice(name="Pattern 🔷", value="Pattern"),
    app_commands.Choice(name="Primordialism 🌿", value="Primordialism"),
    app_commands.Choice(name="Questing ⚔️", value="Questing"),
])
async def tarot_suit(interaction: discord.Interaction, takim: app_commands.Choice[str]):
    suit_cards = [c for c in ALL_CARDS if c["suit"] == takim.value]
    if not suit_cards:
        await interaction.response.send_message("Bu takımda kart bulunamadı.", ephemeral=True)
        return

    await interaction.response.defer()
    card = random.choice(suit_cards)
    is_reversed = random.random() < 0.5
    file, filename = card_to_discord_file(card)
    embed = build_card_embed(card, 1, 1, filename, reversed=is_reversed)
    await interaction.followup.send(embed=embed, file=file)


if __name__ == "__main__":
    bot.run(TOKEN)
