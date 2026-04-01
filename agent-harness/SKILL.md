---
name: agent-harness
description: Guide coding agents to follow the Agent Harness paradigm for building reliable, long-running autonomous agents. Use when: (1) designing multi-agent systems with planner/generator/evaluator architecture, (2) implementing context reset and structured handoff for long-running tasks, (3) building incremental progress tracking with feature lists and git commits, (4) creating separate evaluation loops for quality control, (5) preventing context anxiety and premature task completion in autonomous coding sessions.
---

# Agent Harness Development Guide

This skill provides patterns and practices for building reliable autonomous coding agents using the Harness Engineering paradigm.

## Core Principles

### 1. Multi-Agent Architecture

Separate concerns across specialized agents:

| Agent Type | Responsibility | Key Behaviors |
|------------|----------------|---------------|
| **Planner/Initializer** | Task decomposition, environment setup | Create feature list, initialize progress tracking, set up first git commit |
| **Generator/Coder** | Incremental feature implementation | Work one feature at a time, leave clean state, commit progress |
| **Evaluator** | Quality assessment | Grade outputs against criteria, provide actionable feedback, be skeptical |

### 2. Context Management

**Problem**: Agents lose coherence as context fills; exhibit "context anxiety" near limits.

**Solution**: Context Reset + Structured Handoff

```
Session N ends → Create handoff artifact → Clear context → Session N+1 starts fresh
```

**Handoff artifact must include**:
- Current progress state (what's done, what's next)
- Feature list status (JSON format)
- Git commit history reference
- Any blocking issues or decisions needed

### 3. Incremental Progress

**Never one-shot complex tasks.** Instead:

1. Break work into atomic features (each completable in one session)
2. Implement one feature per session
3. Commit after each feature with descriptive message
4. Update progress tracking file
5. Mark feature as "passes: true" only when fully working

### 4. Separate Evaluation

**Problem**: Agents praise their own work even when mediocre.

**Solution**: Dedicated evaluator agent with tuned skepticism.

Evaluator grades against concrete criteria (see [references/evaluation-criteria.md](references/evaluation-criteria.md)).

## Environment Scaffolding

### Required Files

Initialize these files in the project root:

#### 1. `feature-list.json`

Track all features with pass/fail status. Use JSON (not Markdown) to prevent accidental overwrites.

```json
{
  "features": [
    {
      "id": "feat-001",
      "category": "functional",
      "description": "User can create new chat conversation",
      "steps": [
        "Navigate to main interface",
        "Click 'New Chat' button",
        "Verify new conversation created"
      ],
      "passes": false,
      "implementedBy": null,
      "commitHash": null
    }
  ]
}
```

**Rules**:
- Initializer creates all features marked `"passes": false`
- Coder only changes `passes` field (never remove/edit tests)
- Evaluator verifies before marking `passes: true`

#### 2. `progress.md` or `progress.json`

Session-by-session log of what was accomplished.

```markdown
## Session 1 (2026-04-01)
**Agent**: initializer-v1
**Goal**: Environment setup and feature decomposition

### Completed
- Created project structure (React + Vite + TypeScript)
- Generated feature-list.json with 47 features
- Initial git commit: "feat: initial project scaffolding"

### Next Session Should
- Implement feat-001: New chat button functionality
- Update feature-list.json passes field
```

#### 3. Git Repository

- Commit after every feature implementation
- Use conventional commits: `feat:`, `fix:`, `chore:`
- Enable easy rollback if agent goes off-rails

## Workflow Patterns

### Pattern 1: Long-Running App Build

```
┌─────────────────┐
│ User Request    │ "Build a clone of claude.ai"
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Initializer     │ 1. Parse requirements
│ Agent           │ 2. Generate feature-list.json (50-200 features)
│                 │ 3. Create project scaffolding
│                 │ 4. Make initial commit
│                 │ 5. Write progress.md
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Coding Agent    │ Loop per session:
│ (Session N)     │ 1. Read progress.md, feature-list.json
│                 │ 2. Pick next "passes: false" feature
│                 │ 3. Implement feature completely
│                 │ 4. Test and verify
│                 │ 5. Commit with message
│                 │ 6. Update feature-list.json
│                 │ 7. Update progress.md with handoff notes
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Evaluator       │ 1. Review completed feature
│ Agent           │ 2. Grade against criteria
│                 │ 3. If passes: mark true, continue
│                 │ 4. If fails: provide feedback, request revision
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Context Reset   │ Clear session, start fresh with handoff artifact
└─────────────────┘
```

### Pattern 2: Subjective Quality Tasks (Design/Frontend)

For tasks without binary pass/fail (e.g., "make it beautiful"):

1. **Define grading criteria upfront** (see [references/evaluation-criteria.md](references/evaluation-criteria.md))
2. **Generator** creates output following criteria
3. **Evaluator** grades each criterion 1-5 with justification
4. **Iterate** until average score ≥ threshold (e.g., 4.0)

### Pattern 3: Context Reset Trigger

Reset context when ANY of these conditions are met:

- Session token count > 80% of model limit
- Agent shows signs of context anxiety (rushing, skipping tests)
- Feature implementation exceeds 2 hours
- Evaluator requests major revision (clean slate helps)

## Anti-Patterns to Avoid

| Anti-Pattern | Symptom | Fix |
|--------------|---------|-----|
| One-shotting | Agent tries to build everything in one session | Enforce one-feature-per-session rule |
| Self-evaluation | Agent marks own work as "done" prematurely | Use separate evaluator agent |
| Context hoarding | Agent accumulates context instead of resetting | Implement automatic reset triggers |
| Unclear handoff | Next session spends time figuring out state | Structured handoff artifact required |
| Feature creep | Feature list grows mid-project | Freeze scope after initialization |

## Scripts

Use bundled scripts for common harness operations:

- [`scripts/create-feature-list.py`](scripts/create-feature-list.py) - Generate feature list from spec
- [`scripts/check-progress.py`](scripts/check-progress.py) - Validate progress tracking files
- [`scripts/reset-context.py`](scripts/reset-context.py) - Prepare handoff artifact and clear session

## References

- [evaluation-criteria.md](references/evaluation-criteria.md) - Grading rubrics for subjective tasks
- [handoff-template.md](references/handoff-template.md) - Structured handoff artifact format
- [session-prompt.md](references/session-prompt.md) - Prompt templates for each agent type

## When to Use This Skill

Apply Agent Harness patterns when:

✅ Task requires multiple hours/days of autonomous work
✅ Quality degrades over long sessions
✅ Agent exhibits context anxiety
✅ Self-evaluation produces unreliable results
✅ Need reproducible, auditable progress tracking

Do NOT use for:

❌ Simple one-off tasks (single API call, quick edit)
❌ Exploratory work without clear completion criteria
❌ Tasks requiring continuous human collaboration
