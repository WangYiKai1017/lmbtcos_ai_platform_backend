#!/usr/bin/env python3
"""
Prepare context reset handoff artifact and clear session state.

Usage:
    python scripts/reset-context.py --reason "session_timeout"
    python scripts/reset-context.py --reason "evaluator_revision" --session-id abc123
"""

import json
import argparse
import sys
from datetime import datetime
from pathlib import Path


def load_current_state(feature_list_path: str, progress_path: str) -> dict:
    """Load current project state."""
    state = {}
    
    # Load feature list
    feature_path = Path(feature_list_path)
    if feature_path.exists():
        with open(feature_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            features = data.get("features", [])
            state["features"] = {
                "total": len(features),
                "passing": sum(1 for f in features if f.get("passes")),
                "failing": sum(1 for f in features if not f.get("passes")),
                "next": next((f for f in features if not f.get("passes")), None)
            }
    
    # Load progress
    progress_file = Path(progress_path)
    if progress_file.exists():
        state["progress"] = progress_file.read_text(encoding="utf-8")[-2000:]  # Last 2000 chars
    
    return state


def create_handoff_artifact(state: dict, reason: str, session_id: str = None) -> str:
    """Create a structured handoff artifact for the next agent."""
    
    handoff = f"""# Context Reset Handoff

**Reset Time**: {datetime.now().isoformat()}
**Reason**: {reason}
**Session ID**: {session_id or "N/A"}

---

## Current State Summary

"""
    
    if "features" in state:
        feat = state["features"]
        handoff += f"""### Feature Progress
- **Total Features**: {feat['total']}
- **Completed**: {feat['passing']} ({feat['passing']/feat['total']*100:.1f}% if feat['total'] > 0 else 0)
- **Remaining**: {feat['failing']}

### Next Feature to Implement
"""
        if feat["next"]:
            handoff += f"""
**ID**: {feat['next']['id']}
**Description**: {feat['next']['description']}
**Steps**:
"""
            for i, step in enumerate(feat['next'].get('steps', []), 1):
                handoff += f"{i}. {step}\n"
        else:
            handoff += "\n✅ All features completed!\n"
    
    handoff += f"""
---

## Recent Progress

```
{state.get('progress', 'No progress file found')}
```

---

## Instructions for Next Agent

1. **Read this handoff** - This is your ONLY context from previous sessions
2. **Check feature-list.json** - Verify the state matches what's described here
3. **Start with next feature** - Begin implementation of the feature listed above
4. **Follow harness patterns** - One feature per session, commit after completion
5. **Update progress** - Document your work in progress.md before ending session

---

## Reset Checklist

- [ ] Handoff artifact saved
- [ ] Feature list is current
- [ ] Progress file is updated
- [ ] Git commits are pushed
- [ ] Session can be safely cleared

---

**End of Handoff** - Next agent starts fresh with this document as context.
"""
    
    return handoff


def verify_clean_state() -> list[str]:
    """Verify the repository is in a clean state for handoff."""
    import subprocess
    issues = []
    
    try:
        # Check for uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.stdout.strip():
            issues.append("⚠️  Uncommitted changes exist - consider committing before reset")
            for line in result.stdout.strip().split("\n")[:3]:
                issues.append(f"   {line}")
        
        # Check current branch
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            branch = result.stdout.strip()
            if branch != "main" and branch != "master":
                issues.append(f"ℹ️  Currently on branch: {branch}")
        
    except subprocess.TimeoutExpired:
        issues.append("⚠️  Git command timed out")
    except FileNotFoundError:
        issues.append("⚠️  Git not available")
    
    return issues


def main():
    parser = argparse.ArgumentParser(description="Prepare context reset and handoff")
    parser.add_argument("--reason", "-r", required=True,
                        choices=["session_timeout", "token_limit", "context_anxiety", 
                                 "evaluator_revision", "manual", "error_recovery"],
                        help="Reason for context reset")
    parser.add_argument("--session-id", "-s", default=None,
                        help="Current session ID for tracking")
    parser.add_argument("--feature-list", "-f", default="feature-list.json",
                        help="Path to feature-list.json")
    parser.add_argument("--progress", "-p", default="progress.md",
                        help="Path to progress.md")
    parser.add_argument("--output", "-o", default=None,
                        help="Output handoff to file (default: print to stdout)")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Suppress status output")
    
    args = parser.parse_args()
    
    # Load current state
    if not args.quiet:
        print(f"🔄 Preparing context reset...")
        print(f"   Reason: {args.reason}")
        if args.session_id:
            print(f"   Session: {args.session_id}")
    
    state = load_current_state(args.feature_list, args.progress)
    
    # Verify clean state
    state_issues = verify_clean_state()
    if state_issues and not args.quiet:
        print("\n⚠️  State warnings:")
        for issue in state_issues:
            print(f"   {issue}")
    
    # Create handoff
    handoff = create_handoff_artifact(state, args.reason, args.session_id)
    
    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(handoff, encoding="utf-8")
        if not args.quiet:
            print(f"\n✅ Handoff saved to: {output_path}")
    else:
        print("\n" + "=" * 60)
        print(handoff)
        print("=" * 60)
    
    # Summary
    if not args.quiet and "features" in state:
        feat = state["features"]
        print(f"\n📊 Progress Summary:")
        print(f"   {feat['passing']}/{feat['total']} features complete ({feat['passing']/feat['total']*100:.1f}%)")
        if feat["next"]:
            print(f"   Next: {feat['next']['id']} - {feat['next']['description'][:50]}...")
    
    if not args.quiet:
        print(f"\n✅ Context reset prepared successfully")
        print(f"   → Clear current session context")
        print(f"   → Start new session with handoff artifact as input")


if __name__ == "__main__":
    main()
