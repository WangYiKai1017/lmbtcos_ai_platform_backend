# Session Handoff Template

Use this template when ending a session and preparing for context reset.

---

## Handoff Artifact

```markdown
# Handoff: [Project Name] - Session [N] → [N+1]

**Timestamp**: YYYY-MM-DD HH:MM:SS
**Session ID**: [session-uuid]
**Agent**: [agent-type-and-version]

---

## Current State

### Summary
[2-3 sentences describing overall project status]

### Progress Overview
- **Total Features**: [X]
- **Completed**: [Y] ([Z]%)
- **In Progress**: [A]
- **Not Started**: [B]

---

## What Was Done This Session

### Features Implemented
| Feature ID | Description | Status | Commit |
|------------|-------------|--------|--------|
| feat-001 | [description] | ✅ Pass | [hash] |
| feat-002 | [description] | ✅ Pass | [hash] |

### Key Changes
- [Major change 1]
- [Major change 2]
- [Major change 3]

### Files Modified
- `path/to/file1.ext` - [brief description]
- `path/to/file2.ext` - [brief description]

---

## What Next Session Should Do

### Immediate Next Task
**Feature**: feat-XXX - [feature description]

**Starting Point**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Outcome**: [what "done" looks like]

**Potential Pitfalls**:
- [Thing to watch out for]
- [Known issue or decision needed]

---

## Open Issues / Decisions Needed

| Issue | Priority | Context | Decision Needed |
|-------|----------|---------|-----------------|
| [issue] | High/Med/Low | [context] | [what needs deciding] |

---

## Environment State

### Git Status
- **Current Branch**: [branch-name]
- **Last Commit**: [hash] - [message]
- **Uncommitted Changes**: [yes/no, describe if yes]

### Dependencies
- **New packages added**: [list or "none"]
- **Breaking changes**: [describe or "none"]

### Known Issues
- [Any bugs, limitations, or technical debt introduced]

---

## Feature List Status

**Location**: `./feature-list.json`

**Quick Stats**:
```json
{
  "total": 47,
  "passes": 12,
  "failing": 35
}
```

---

## Context for Next Agent

### What Worked Well
- [Approach or pattern that was effective]

### What to Avoid
- [Thing that caused problems]

### Tips
- [Helpful insight for next agent]

---

## Verification Checklist

Before starting next session, verify:

- [ ] `feature-list.json` is up to date
- [ ] All commits are pushed
- [ ] No uncommitted critical changes
- [ ] Progress file reflects current state
- [ ] No blocking issues unaddressed

---

**End of Handoff**
```

---

## Usage Instructions

1. **Fill all sections** - Incomplete handoffs cause next session to waste time
2. **Be specific** - "Fix the bug" → "Fix null pointer in userService.getProfile() line 47"
3. **Include commit hashes** - Enables rollback if needed
4. **Note decisions made** - Prevents re-litigation
5. **Flag uncertainties** - If unsure about something, mark it explicitly

---

## Example (Abbreviated)

```markdown
# Handoff: Claude.ai Clone - Session 3 → 4

**Timestamp**: 2026-04-01 15:45:00
**Agent**: coder-v2

## Current State

### Summary
Core chat interface is functional. 12 of 47 features complete. 
Next session should focus on sidebar conversation management.

### Progress Overview
- **Total Features**: 47
- **Completed**: 12 (25.5%)
- **In Progress**: 1
- **Not Started**: 34

## What Was Done This Session

### Features Implemented
| Feature ID | Description | Status | Commit |
|------------|-------------|--------|--------|
| feat-003 | Send message with Enter key | ✅ Pass | a3f8c2d |
| feat-004 | Display AI response streaming | ✅ Pass | b7e1f9a |

## What Next Session Should Do

### Immediate Next Task
**Feature**: feat-007 - Sidebar shows conversation history

**Starting Point**:
1. Create ConversationList component in src/components/
2. Connect to existing conversation store
3. Add click handler to load conversation

**Expected Outcome**: 
- Sidebar displays list of past conversations
- Clicking loads conversation into main view
- Active conversation is highlighted

**Potential Pitfalls**:
- Conversation store may need migration for new format
- Long conversation titles need truncation
```
