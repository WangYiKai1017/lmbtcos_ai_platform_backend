# Evaluation Criteria for Subjective Tasks

Use these criteria when evaluating outputs that cannot be verified with binary tests (e.g., design, UX, writing).

## Core Criteria

### 1. Design Quality (Weight: 3x)

**Question**: Does the output feel like a coherent whole rather than a collection of parts?

**Strong indicators**:
- Colors, typography, layout combine to create distinct mood/identity
- Consistent visual language throughout
- Deliberate design decisions evident

**Weak indicators**:
- Mismatched styles or tones
- Generic/template appearance
- Inconsistent spacing, colors, or typography

**Grading scale**:
- 5: Exceptional - professional-grade, distinctive character
- 4: Good - cohesive, minor inconsistencies
- 3: Acceptable - functional but unremarkable
- 2: Poor - noticeable inconsistencies, feels assembled
- 1: Fails - incoherent, conflicting elements

---

### 2. Originality (Weight: 2x)

**Question**: Is there evidence of custom decisions, or is this template defaults and AI patterns?

**Strong indicators**:
- Custom component design, not library defaults
- Unique combinations or approaches
- No telltale AI patterns (purple gradients on white cards, generic hero sections)

**Weak indicators**:
- Stock components without modification
- Template layouts with minimal customization
- Obvious AI-generated patterns

**Grading scale**:
- 5: Highly original - clear creative choices throughout
- 4: Mostly original - some custom elements, few defaults
- 3: Mixed - balance of custom and template elements
- 2: Mostly templated - minimal customization
- 1: Copy-paste - obvious template or AI default

---

### 3. Craft (Weight: 1.5x)

**Question**: Is the technical execution competent?

**Check**:
- Typography hierarchy (headings, body, captions)
- Spacing consistency (margins, padding, gaps)
- Color harmony and contrast ratios
- Code quality (if applicable)

**Grading scale**:
- 5: Flawless - professional polish
- 4: Solid - minor issues only
- 3: Acceptable - functional but rough edges
- 2: Sloppy - multiple craft issues
- 1: Broken - fundamentals failing

---

### 4. Functionality (Weight: 1.5x)

**Question**: Can users accomplish their goals without confusion?

**Check**:
- Primary actions are discoverable
- User flow is intuitive
- No broken interactions
- Error states handled

**Grading scale**:
- 5: Delightful - exceeds expectations
- 4: Working - all features functional
- 3: Usable - core features work, minor friction
- 2: Problematic - key features broken or confusing
- 1: Unusable - cannot complete basic tasks

---

## Calculation

```
Final Score = (Design×3 + Originality×2 + Craft×1.5 + Functionality×1.5) / 8
```

**Pass threshold**: ≥ 4.0

**Revision required**: < 4.0

---

## Evaluator Instructions

1. **Be skeptical** - Default to critical assessment
2. **Justify scores** - Explain why each score was given
3. **Actionable feedback** - Tell generator what to improve
4. **No self-evaluation** - Never evaluate your own work

---

## Example Evaluation

```json
{
  "featureId": "feat-012",
  "evaluator": "evaluator-v1",
  "timestamp": "2026-04-01T14:30:00Z",
  "scores": {
    "designQuality": { "score": 4, "notes": "Cohesive color scheme, but typography hierarchy could be stronger" },
    "originality": { "score": 3, "notes": "Some custom buttons, but hero section feels templated" },
    "craft": { "score": 5, "notes": "Pixel-perfect spacing, excellent contrast ratios" },
    "functionality": { "score": 4, "notes": "All interactions work, error states missing" }
  },
  "finalScore": 4.06,
  "passes": true,
  "feedback": "Good overall. Prioritize: (1) Add error state handling, (2) Customize hero section more"
}
```
