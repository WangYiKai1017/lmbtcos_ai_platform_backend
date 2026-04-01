# Agent Harness Skill - Quick Reference

## 📦 What's Included

```
agent-harness/
├── SKILL.md                          # Main skill documentation
├── scripts/
│   ├── create-feature-list.py        # Generate feature list from spec
│   ├── check-progress.py             # Validate progress tracking
│   └── reset-context.py              # Prepare context reset handoff
├── references/
│   ├── evaluation-criteria.md        # Grading rubrics for subjective tasks
│   ├── handoff-template.md           # Structured handoff artifact format
│   └── session-prompt.md             # Prompt templates for each agent type
└── assets/
    ├── example-feature-list.json     # Sample feature list
    └── example-progress.md           # Sample progress log
```

---

## 🚀 Quick Start

### 1. Initialize a Long-Running Project

```bash
# Generate feature list from your spec
python scripts/create-feature-list.py "Build a chat application" -o feature-list.json

# Initialize progress tracking
echo "# Progress Log\n\n## Session 1\n" > progress.md

# Initialize git repo
git init
git add .
git commit -m "feat: initial project setup"
```

### 2. Run Initializer Agent

Give the Initializer Agent prompt (see `references/session-prompt.md`) to your AI agent along with:
- Product specification
- This skill's SKILL.md

The initializer will:
- Decompose spec into atomic features
- Set up project scaffolding
- Create initial commits

### 3. Run Coding Agent Loop

For each session:

```bash
# Check current state
python scripts/check-progress.py

# Give Coding Agent prompt to agent
# Agent implements ONE feature, commits, updates progress

# After agent completes
python scripts/check-progress.py  # Verify state
```

### 4. Context Reset (When Needed)

```bash
# Prepare handoff and reset
python scripts/reset-context.py --reason session_timeout -o handoff-session-3.md

# Start new session with handoff file as input
```

---

## 🎯 Key Patterns

### One Feature Per Session

```
❌ BAD:  Try to implement multiple features
✅ GOOD: Complete one feature, commit, reset context
```

### Separate Evaluation

```
❌ BAD:  Coding agent marks own work as "done"
✅ GOOD: Dedicated evaluator agent grades work
```

### Structured Handoff

```
❌ BAD:  "Continue where I left off"
✅ GOOD: Handoff artifact with exact next steps
```

---

## 📊 Feature List Format

```json
{
  "features": [
    {
      "id": "feat-001",
      "description": "User can send message",
      "steps": ["Step 1", "Step 2"],
      "passes": false,
      "commitHash": null
    }
  ]
}
```

**Rules**:
- All features start with `"passes": false`
- Only change `passes` to `true` after evaluator approval
- Never remove features from the list

---

## 🔍 Validation Commands

```bash
# Check project state
python scripts/check-progress.py

# JSON output for automation
python scripts/check-progress.py --json

# Custom file paths
python scripts/check-progress.py -f my-features.json -p my-progress.md
```

---

## ⚠️ Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| One-shotting | Agent tries to build everything at once | Enforce one-feature rule |
| Context anxiety | Agent rushes near session end | Trigger context reset earlier |
| Self-evaluation | Agent marks mediocre work as done | Use separate evaluator |
| Unclear handoff | Next session confused | Use handoff template |

---

## 📈 Success Metrics

Track these to measure harness effectiveness:

- **Features per session**: Target 1-2 (atomic features)
- **Evaluator pass rate**: Target >80% first-time pass
- **Context resets per project**: Normal: 10-50+ for large projects
- **Regression rate**: Features breaking after marked complete (should be <5%)

---

## 🔗 Related Resources

- Anthropic: [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- Anthropic: [Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- LangGraph: [Harness engineering patterns](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/)

---

*For detailed guidance, see SKILL.md*
