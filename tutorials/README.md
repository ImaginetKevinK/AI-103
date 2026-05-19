# tutorials/

Standalone, from-scratch walk-throughs that teach someone how to build one
of the numbered examples in `examples/` as a self-contained project — no
clone of this repo required.

## Naming convention

`eNN_Tutorial.txt` where `NN` matches the corresponding example in
`examples/eNN_*.py`. So `e22_Tutorial.txt` here teaches the reader how to
recreate `@/examples/e22_responses_tools_combined.py` from scratch.

## What each tutorial covers

Each file is plain text (no Markdown) and assumes the reader has nothing
beyond an Azure subscription and a computer. A complete tutorial walks
through:

1. Configuring Azure Foundry (portal, model deployment, copying credentials)
2. Installing Python and an editor
3. Creating a working folder and virtual environment
4. Writing a `.env` file
5. Writing the single Python script that mirrors the example
6. Explaining what the script does
7. Running and troubleshooting

## Adding a new tutorial

Pick the example you want to teach, copy `e22_Tutorial.txt` as a template,
and rewrite Steps 1, 5, 6, 7 to match your example's specifics. Steps 2–4
(Python, working folder, venv) and the troubleshooting section are largely
boilerplate and can stay close to the e22 wording.
