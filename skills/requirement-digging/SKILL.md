---
name: requirement-digging
description: Multi-agent system for requirement elicitation through conversational dialogue. Use when: (1) user has vague/natural language requirements that need clarification, (2) need to extract actionable story cards from user conversations, (3) need to ask probing questions to uncover hidden requirements, (4) need to transform ambiguous requests into developer-ready specifications, (5) need iterative requirement refinement with quality evaluation.
---

# Requirement Digging Multi-Agent System

This skill provides a 4-agent architecture for transforming vague user requirements into developer-ready story cards through structured conversational elicitation.

## System Architecture

```
User → [Conversation Guide] → [Requirement Analyst] → [Story Card Generator] → [Quality Evaluator] → Coding Agent
              ↑                       ↓                                              │
              └─────────────── [Context & Memory Management] ←────────────────────────┘
```

## Agent Roles

| Agent | Responsibility | Trigger | Output |
|-------|----------------|---------|--------|
| **Conversation Guide** | Multi-turn dialogue, requirement elicitation | User initiates request | Dialogue transcript + requirement points |
| **Requirement Analyst** | Structure and prioritize requirements | Guide completes digging | Categorized requirement list (MoSCoW) |
| **Story Card Generator** | Create developer-ready story cards | Analyst output confirmed | JSON story cards with acceptance criteria |
| **Quality Evaluator** | Evaluate story card quality | Generator completes | Pass/Fail + feedback |

## Core Workflow

### Phase 1: Requirement Elicitation (Conversation Guide)

**Goal**: Extract requirements through guided dialogue

**Process**:
1. Receive initial user request (may be vague)
2. Apply 5W1H questioning framework
3. Identify ambiguities and contradictions
4. Request concrete examples
5. Output structured requirement summary

**Questioning Framework**:
- **What**: "What specific features do you need?"
- **Who**: "Who is the target user?"
- **When**: "When will they use this? What scenarios?"
- **Where**: "Where will it be deployed?"
- **Why**: "Why is this important? What problem does it solve?"
- **How**: "How do you imagine it working?"

**Exit Conditions**:
- Minimum 5 dialogue turns completed
- Requirement coverage > 80%
- User explicitly says "that's enough"
- Maximum 20 turns (prevent fatigue)

### Phase 2: Requirement Analysis (Requirement Analyst)

**Goal**: Transform dialogue into structured requirements

**Process**:
1. Read dialogue transcript
2. Extract all requirement points
3. Classify using MoSCoW:
   - **Must**: Critical for MVP
   - **Should**: Important but not critical
   - **Could**: Nice to have
4. Identify dependencies
5. Flag risks and open questions

**Output Structure**:
```json
{
  "functional": [],
  "nonFunctional": [],
  "userStories": [],
  "openQuestions": [],
  "risks": []
}
```

### Phase 3: Story Card Generation (Story Card Generator)

**Goal**: Create atomic, testable story cards

**Process**:
1. Read structured requirements
2. Decompose each requirement into 1-3 story cards
3. Write acceptance criteria (Gherkin format)
4. Estimate complexity (S/M/L/XL)
5. Mark dependencies

**Story Card Template**:
```json
{
  "id": "story-001",
  "title": "User can...",
  "description": "As a [role], I want [feature], so that [value]",
  "acceptanceCriteria": [
    "Given [scenario], When [action], Then [result]"
  ],
  "priority": "Must|Should|Could",
  "estimatedComplexity": "S|M|L|XL",
  "dependencies": [],
  "notes": ""
}
```

### Phase 4: Quality Evaluation (Quality Evaluator)

**Goal**: Ensure story cards are development-ready

**Evaluation Criteria**:

| Dimension | Weight | Check |
|-----------|--------|-------|
| **Completeness** | 3x | Role/Feature/Value present |
| **Testability** | 2x | Acceptance criteria verifiable |
| **Atomicity** | 1.5x | Independently developable |
| **Clarity** | 1.5x | Unambiguous for developers |

**Scoring**:
- Calculate weighted average
- **Pass**: ≥ 4.0
- **Fail**: < 4.0 (return for revision)

**Evaluator Mindset**:
- Be skeptical, not generous
- Provide specific, actionable feedback
- Never evaluate your own work

## Context Management

### When to Reset Context

Trigger context reset when ANY condition is met:

- Dialogue turns > 15
- Token usage > 80% of model limit
- User明显 changes topic
- Agent shows "context anxiety" symptoms

### Handoff Artifact Structure

```markdown
# Requirement Digging Handoff

## Session State
- **Phase**: digging|analyzing|generating|evaluating
- **Turns Completed**: N
- **Requirements Extracted**: N

## Confirmed Requirements
[List]

## Open Questions
[List with IDs]

## User Preferences
[Noted preferences]

## Next Steps
[What next agent should do]
```

## Scripts

Use bundled scripts for automation:

- [`scripts/generate-story-cards.py`](scripts/generate-story-cards.py) - Transform requirements to story cards
- [`scripts/validate-requirements.py`](scripts/validate-requirements.py) - Check requirement completeness
- [`scripts/export-for-coding.py`](scripts/export-for-coding.py) - Format output for coding agent

## References

- [agent-prompts.md](references/agent-prompts.md) - Detailed prompts for each agent
- [questioning-framework.md](references/questioning-framework.md) - 5W1H question bank
- [story-card-examples.md](references/story-card-examples.md) - Example story cards

## Integration with Coding Agent

**Input to Coding Agent**:
1. Story cards JSON (feature-list.json format)
2. Project background summary (<500 words)
3. Tech stack recommendations
4. Known risks and open decisions

**Feedback Loop**:
- Coding Agent finds unclear requirement → Flag story card → Notify analyst
- Analyst clarifies → Update card → Coding Agent continues

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|--------------|---------|-----|
| Leading questions | "Don't you think you need X?" | Ask open questions |
| Premature closure | Stopping after 2-3 turns | Enforce minimum 5 turns |
| Vague acceptance criteria | "It should work well" | Require Gherkin format |
| Self-evaluation | Generator marks own work | Use separate evaluator |

## When to Use This Skill

✅ User requirement is vague/natural language
✅ Need structured handoff to development
✅ Complex requirements need decomposition
✅ Want quality gate before coding starts

❌ Simple one-off task ("add a button")
✅ User already provided detailed spec
❌ Exploratory discussion without implementation goal
