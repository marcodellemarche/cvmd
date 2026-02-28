#!/usr/bin/env python3
"""
Setup script for the cvmd template.
Replaces {{PLACEHOLDER}} tokens in README.md and _config.yml with your personal details.

Usage:
    python setup.py
    python3 setup.py
"""

import os
import sys


FILES_TO_UPDATE = ["README.md", "_config.yml"]


def prompt(label, default=None, required=True):
    hint = f" [{default}]" if default else (" (optional, press Enter to skip)" if not required else "")
    while True:
        value = input(f"  {label}{hint}: ").strip()
        if not value and default:
            return default
        if not value and not required:
            return ""
        if not value:
            print("  This field is required.")
            continue
        return value


def replace_in_file(path, replacements):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    for old, new in replacements.items():
        content = content.replace(old, new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Updated {path}")


def main():
    # Always run from the directory where this script lives
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Check that the template files exist
    missing = [f for f in FILES_TO_UPDATE if not os.path.isfile(f)]
    if missing:
        print(f"Error: could not find {', '.join(missing)}. Make sure you run this script from the repo root.")
        sys.exit(1)

    print("\n=== CV Setup ===")
    print("Answer the prompts below to personalise your CV template.")
    print("You can always edit README.md manually afterwards.\n")

    full_name = prompt("Full name (e.g. Jane Doe)")
    email = prompt("Email address")
    github_username = prompt("GitHub username")
    repo_name = prompt("Repository name", default=os.path.basename(script_dir))
    linkedin_username = prompt("LinkedIn username (the part after linkedin.com/in/)")
    instagram_username = prompt("Instagram username", required=False)

    replacements = {
        "{{FULL_NAME}}": full_name,
        "{{EMAIL}}": email,
        "{{GITHUB_USERNAME}}": github_username,
        "{{REPO_NAME}}": repo_name,
        "{{LINKEDIN_USERNAME}}": linkedin_username,
    }

    if instagram_username:
        replacements["{{INSTAGRAM_USERNAME}}"] = instagram_username
    else:
        # Remove the entire Instagram link (including the separator) from the contacts line
        replacements[" / [Instagram](https://www.instagram.com/{{INSTAGRAM_USERNAME}})"] = ""

    print("\nApplying changes...")
    for filepath in FILES_TO_UPDATE:
        replace_in_file(filepath, replacements)

    print("\nDone! Next steps:")
    print("  1. Replace the placeholder CV content in README.md with your own.")
    print("  2. Enable GitHub Pages: Settings > Pages > Source: GitHub Actions.")
    print("  3. Commit and push — the Action will build the site and generate the PDF.")
    print("     If the Action fails because Pages was not yet enabled, re-run it from the Actions tab.")


if __name__ == "__main__":
    main()
