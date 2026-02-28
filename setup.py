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
PROFILE_IMAGE = os.path.join("assets", "profile.png")
PROMPT_OUTPUT = "cv-prompt.txt"


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


def make_circular_profile(image_path):
    """Center-crop a profile image to a circle with a transparent background."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print(f"\n  Skipping image crop — Pillow is not installed.")
        print(f"  To get a circular PNG, install it and re-run:")
        print(f"    pip install Pillow")
        return

    img = Image.open(image_path).convert("RGBA")

    # Center-crop to a square
    size = min(img.size)
    left = (img.width - size) // 2
    top = (img.height - size) // 2
    img = img.crop((left, top, left + size, top + size))

    # Create a circular mask
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)

    # Paste onto a transparent canvas and apply the mask
    result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    result.paste(img, mask=mask)
    result.save(image_path, "PNG")
    print(f"  Cropped {image_path} to a circle with transparent background")


def generate_prompt():
    """Write cv-prompt.txt: a ready-to-use LLM prompt for rewriting the CV content."""
    with open("README.md", "r", encoding="utf-8") as f:
        template_section = f.read()

    prompt_text = f"""\
You are helping me write my Curriculum Vitae in Markdown, following a specific template.

## Your task

Rewrite the CV content in the template below using MY personal information, which I will
provide at the end of this prompt.

## Rules

- Output ONLY the CV content (from `<div class="page-break"></div>` to the end of the
  document) — no explanation, no preamble.
- In the **first block** (name, profile picture, tagline, contact links, PDF download link),
  keep the name, picture, contact links, and PDF download link exactly as-is — but
  **rewrite the tagline** (the italic line below the picture) to reflect my actual profile.
- Freely rewrite everything after the first block (experience, education, skills, etc.)
  to reflect my background.
- Rename, add, or remove sections as needed to best represent my profile.
- Mirror the Markdown formatting: `##` for sections, `**Role** @ [Company](url) *(dates)*`
  for entries, bullet points for highlights, `***Technologies used:***` where relevant.
- Place `<div class="page-break"></div>` at natural page-break points (roughly every
  1-1.5 pages of content).
- Do not invent or infer details I have not provided.

## Template

{template_section}
---

## My information

[Paste your existing CV, describe your experience, education, skills, etc.
You can also attach a PDF or share a LinkedIn URL if your LLM supports it.]
"""

    with open(PROMPT_OUTPUT, "w", encoding="utf-8") as f:
        f.write(prompt_text)
    print(f"  Generated {PROMPT_OUTPUT}")


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

    if os.path.isfile(PROFILE_IMAGE):
        make_circular_profile(PROFILE_IMAGE)
    else:
        print(f"\n  Note: no image found at {PROFILE_IMAGE}.")
        print(f"  Add your photo there and re-run to get a circular crop.")

    generate_prompt()

    print("\nDone! Next steps:")
    print(f"  1. Open {PROMPT_OUTPUT}, add your details at the bottom, and paste it into")
    print(f"     your LLM of choice (attach your old CV or LinkedIn URL if it supports it).")
    print(f"  2. Replace the CV content in README.md with the LLM output.")
    print(f"  3. Enable GitHub Pages: Settings > Pages > Source: GitHub Actions.")
    print(f"  4. Commit and push — the Action will build the site and generate the PDF.")
    print(f"     If the Action fails because Pages was not yet enabled, re-run it from the Actions tab.")


if __name__ == "__main__":
    main()
