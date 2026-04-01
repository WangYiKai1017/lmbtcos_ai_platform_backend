#!/usr/bin/env python3
"""
Validate progress tracking files and feature list consistency.

Usage:
    python scripts/check-progress.py
    python scripts/check-progress.py --feature-list feature-list.json --progress progress.md
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime


def load_feature_list(path: str) -> dict:
    """Load and parse feature list JSON."""
    feature_path = Path(path)
    if not feature_path.exists():
        raise FileNotFoundError(f"Feature list not found: {path}")
    
    with open(feature_path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_feature_list(data: dict) -> list[str]:
    """Validate feature list structure and consistency."""
    issues = []
    
    if "features" not in data:
        issues.append("❌ Missing 'features' array in feature-list.json")
        return issues
    
    features = data["features"]
    seen_ids = set()
    
    for i, feat in enumerate(features):
        # Check required fields
        required = ["id", "description", "passes"]
        for field in required:
            if field not in feat:
                issues.append(f"❌ Feature {i}: Missing required field '{field}'")
        
        # Check ID uniqueness
        if "id" in feat:
            if feat["id"] in seen_ids:
                issues.append(f"❌ Duplicate feature ID: {feat['id']}")
            seen_ids.add(feat["id"])
        
        # Check passes is boolean
        if "passes" in feat and not isinstance(feat["passes"], bool):
            issues.append(f"❌ Feature {feat.get('id', i)}: 'passes' must be boolean, got {type(feat['passes'])}")
        
        # Check commit hash if passes
        if feat.get("passes") and not feat.get("commitHash"):
            issues.append(f"⚠️  Feature {feat.get('id', i)}: Marked as passing but no commitHash")
        
        # Check steps is list
        if "steps" in feat and not isinstance(feat["steps"], list):
            issues.append(f"❌ Feature {feat.get('id', i)}: 'steps' must be an array")
    
    # Check feature ID sequencing
    ids = [f.get("id", "") for f in features]
    expected_prefix = "feat-"
    if all(id.startswith(expected_prefix) for id in ids if id):
        numbers = []
        for id in ids:
            try:
                numbers.append(int(id.replace(expected_prefix, "")))
            except ValueError:
                pass
        if numbers and numbers != sorted(numbers):
            issues.append("⚠️  Feature IDs are not sequential")
    
    return issues


def check_progress_file(path: str) -> list[str]:
    """Validate progress.md structure."""
    issues = []
    progress_path = Path(path)
    
    if not progress_path.exists():
        issues.append(f"❌ Progress file not found: {path}")
        return issues
    
    content = progress_path.read_text(encoding="utf-8")
    
    # Check for required sections
    required_sections = [
        "## Session",
        "### Completed",
        "### Next Session"
    ]
    
    for section in required_sections:
        if section not in content:
            issues.append(f"⚠️  Progress file missing section: {section}")
    
    # Check for recent update (within 24 hours for active projects)
    # This is a simple heuristic - look for date pattern
    import re
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', content)
    if dates:
        latest = max(dates)
        issues.append(f"ℹ️  Latest session date: {latest}")
    
    return issues


def check_git_status() -> list[str]:
    """Check git repository status."""
    import subprocess
    issues = []
    
    try:
        # Check if git repo exists
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            issues.append("⚠️  Not a git repository - consider initializing one")
            return issues
        
        # Check for uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.stdout.strip():
            issues.append("⚠️  Uncommitted changes detected:")
            for line in result.stdout.strip().split("\n")[:5]:
                issues.append(f"   {line}")
            if len(result.stdout.strip().split("\n")) > 5:
                issues.append("   ... and more")
        else:
            issues.append("✅ Working tree clean")
        
        # Get last commit
        result = subprocess.run(
            ["git", "log", "-1", "--oneline"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            issues.append(f"ℹ️  Last commit: {result.stdout.strip()}")
        
    except subprocess.TimeoutExpired:
        issues.append("⚠️  Git command timed out")
    except FileNotFoundError:
        issues.append("⚠️  Git not installed or not in PATH")
    
    return issues


def generate_report(feature_issues: list[str], progress_issues: list[str], git_issues: list[str]) -> str:
    """Generate a validation report."""
    report = []
    report.append("=" * 60)
    report.append("AGENT HARNESS PROGRESS CHECK REPORT")
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append("=" * 60)
    report.append("")
    
    # Feature List
    report.append("📋 FEATURE LIST")
    report.append("-" * 40)
    if feature_issues:
        for issue in feature_issues:
            report.append(f"  {issue}")
    else:
        report.append("  ✅ No issues found")
    report.append("")
    
    # Progress File
    report.append("📝 PROGRESS FILE")
    report.append("-" * 40)
    if progress_issues:
        for issue in progress_issues:
            report.append(f"  {issue}")
    else:
        report.append("  ✅ No issues found")
    report.append("")
    
    # Git Status
    report.append("🔀 GIT STATUS")
    report.append("-" * 40)
    if git_issues:
        for issue in git_issues:
            report.append(f"  {issue}")
    else:
        report.append("  ✅ No issues found")
    report.append("")
    
    # Summary
    all_issues = feature_issues + progress_issues + git_issues
    error_count = sum(1 for i in all_issues if i.startswith("❌"))
    warning_count = sum(1 for i in all_issues if i.startswith("⚠️"))
    
    report.append("=" * 60)
    report.append("SUMMARY")
    report.append("=" * 60)
    report.append(f"  Errors:   {error_count}")
    report.append(f"  Warnings: {warning_count}")
    report.append(f"  Info:     {sum(1 for i in all_issues if i.startswith('ℹ️'))}")
    report.append("")
    
    if error_count > 0:
        report.append("  🚨 Action required: Fix errors before continuing")
    elif warning_count > 0:
        report.append("  ⚠️  Consider addressing warnings")
    else:
        report.append("  ✅ All checks passed - ready for next session")
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Check progress tracking files")
    parser.add_argument("--feature-list", "-f", default="feature-list.json",
                        help="Path to feature-list.json")
    parser.add_argument("--progress", "-p", default="progress.md",
                        help="Path to progress.md")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON instead of human-readable")
    
    args = parser.parse_args()
    
    # Run checks
    try:
        feature_data = load_feature_list(args.feature_list)
        feature_issues = check_feature_list(feature_data)
    except FileNotFoundError as e:
        feature_issues = [str(e)]
    except json.JSONDecodeError as e:
        feature_issues = [f"❌ Invalid JSON: {e}"]
    
    progress_issues = check_progress_file(args.progress)
    git_issues = check_git_status()
    
    # Generate report
    if args.json:
        output = {
            "timestamp": datetime.now().isoformat(),
            "featureList": {
                "path": args.feature_list,
                "issues": feature_issues,
                "stats": {
                    "total": len(feature_data.get("features", [])),
                    "passing": sum(1 for f in feature_data.get("features", []) if f.get("passes")),
                    "failing": sum(1 for f in feature_data.get("features", []) if not f.get("passes"))
                }
            },
            "progressFile": {
                "path": args.progress,
                "issues": progress_issues
            },
            "gitStatus": git_issues
        }
        print(json.dumps(output, indent=2))
    else:
        report = generate_report(feature_issues, progress_issues, git_issues)
        print(report)
    
    # Exit code based on errors
    error_count = sum(1 for i in feature_issues + progress_issues if i.startswith("❌"))
    sys.exit(1 if error_count > 0 else 0)


if __name__ == "__main__":
    main()
