#!/usr/bin/env python3
"""
Create a feature list from a product specification.

Usage:
    python scripts/create-feature-list.py "Build a clone of claude.ai" --output feature-list.json
    python scripts/create-feature-list.py spec.md --output feature-list.json
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path


def parse_spec(spec_text: str) -> list[dict]:
    """
    Parse a product spec and generate atomic features.
    
    In a real implementation, this would use an LLM to decompose the spec.
    For now, this is a template that shows the expected output format.
    """
    # Template features - in production, this would be LLM-generated
    template_features = [
        {
            "id": "feat-001",
            "category": "core",
            "description": "User can see the main chat interface",
            "steps": [
                "Load the application",
                "Verify main chat area is visible",
                "Verify welcome message is displayed"
            ],
            "passes": False,
            "implementedBy": None,
            "commitHash": None,
            "createdAt": datetime.now().isoformat()
        },
        {
            "id": "feat-002",
            "category": "core",
            "description": "User can type a message in the input field",
            "steps": [
                "Focus the input field",
                "Type text",
                "Verify text appears in input"
            ],
            "passes": False,
            "implementedBy": None,
            "commitHash": None,
            "createdAt": datetime.now().isoformat()
        },
        {
            "id": "feat-003",
            "category": "core",
            "description": "User can send message by pressing Enter",
            "steps": [
                "Type a message",
                "Press Enter key",
                "Verify message appears in chat",
                "Verify input field is cleared"
            ],
            "passes": False,
            "implementedBy": None,
            "commitHash": None,
            "createdAt": datetime.now().isoformat()
        }
    ]
    
    print(f"ℹ️  Generated {len(template_features)} initial features from spec")
    print(f"📝 Spec preview: {spec_text[:100]}...")
    print(f"⚠️  In production, integrate with LLM to decompose spec into 50-200 atomic features")
    
    return template_features


def main():
    parser = argparse.ArgumentParser(description="Create feature list from product spec")
    parser.add_argument("spec", help="Product specification text or path to spec file")
    parser.add_argument("--output", "-o", default="feature-list.json", 
                        help="Output file path (default: feature-list.json)")
    parser.add_argument("--format", choices=["json", "markdown"], default="json",
                        help="Output format (default: json)")
    
    args = parser.parse_args()
    
    # Check if spec is a file path
    spec_path = Path(args.spec)
    if spec_path.exists():
        spec_text = spec_path.read_text()
    else:
        spec_text = args.spec
    
    # Generate features
    features = parse_spec(spec_text)
    
    # Create output structure
    output = {
        "metadata": {
            "spec": spec_text[:200],
            "createdAt": datetime.now().isoformat(),
            "totalFeatures": len(features)
        },
        "features": features
    }
    
    # Write output
    output_path = Path(args.output)
    
    if args.format == "json":
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"✅ Feature list written to {output_path}")
    else:
        # Markdown format for human review
        md_content = f"# Feature List\n\n**Generated**: {datetime.now().isoformat()}\n\n"
        md_content += f"**Spec**: {spec_text[:200]}...\n\n"
        md_content += f"**Total Features**: {len(features)}\n\n---\n\n"
        
        for feat in features:
            md_content += f"## {feat['id']}: {feat['description']}\n\n"
            md_content += f"**Category**: {feat['category']}\n\n"
            md_content += "**Steps**:\n"
            for step in feat['steps']:
                md_content += f"- [ ] {step}\n"
            md_content += f"\n**Status**: {'✅ Pass' if feat['passes'] else '❌ Failing'}\n\n---\n\n"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"✅ Feature list written to {output_path} (markdown)")
    
    print(f"\n📊 Summary:")
    print(f"   Total features: {len(features)}")
    print(f"   Passing: {sum(1 for f in features if f['passes'])}")
    print(f"   Failing: {sum(1 for f in features if not f['passes'])}")


if __name__ == "__main__":
    main()
