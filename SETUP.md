# How to use this template

Hi everyone! This repository is a template and it's meant to be used as a starting point for your Curriculum Vitae.

Come on, updating the CV is already boring by itself, imagine having to take care of its formatting as well. So the idea is to update a single Markdown file (the README), and a Github Action will take care of the rest. It will:

- Put the CV online on **Github Pages**, built with Jekyll. You can even use a custom domain if you'd like. You don't need to worry too much about the formatting. Feel free to move from Jekyll to [one of these](https://github.com/pages-themes).
- Convert it to a **PDF**, which is uploaded as the `latest` Release. A link to it can be found at the top of the CV, so it can be easily downloaded from the online version.

At every commit into the `main` branch, everything will be rebuilt and updated.

## Getting started

1. Run `python setup.py` to fill in your personal details (name, email, social handles, etc.) and generate a `cv-prompt.txt` you can feed to any LLM to draft your CV content.
2. Replace the placeholder content in `README.md` with your own (manually or using the LLM output).
3. Enable Github Pages for your repo. Go to *Settings*, *Pages*, then under *Build and deployment* set the source to **Github Actions**.
4. Commit and push. If the Action fails because Pages wasn't enabled yet, simply re-run it from the Actions tab.

## Tips

**Forcing a page break in the PDF** — use the following HTML element anywhere in `README.md`:

```html
<div class="page-break"></div>
```

**Circular profile picture** — `setup.py` automatically crops `assets/profile.png` to a circle (requires `pip install Pillow`). Just replace that file with your own photo before running setup.

That's it, see ya! 👋
