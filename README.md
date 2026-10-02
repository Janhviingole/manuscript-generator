
# Synthetic Manuscript Generator

An automated Python pipeline for generating synthetic historical manuscript folios with synchronized ground-truth annotations.

The generator supports:

- Devanagari
- Modi
- Sharada

It produces manuscript-style images with aged materials, manuscript text, handwriting variation, marginal annotations, highlighted text, folds, surface artifacts, ink variation, and synchronized Markdown annotations.

---

## Features

- Synthetic historical manuscript folio generation
- Support for Devanagari, Modi and Sharada scripts
- Aged handmade-paper backgrounds
- Palm-leaf inspired backgrounds
- Random material selection
- Historical manuscript-style text rendering
- Handwriting-like character variation
- Ink color variation
- Ink bleeding and fading effects
- Surface stains and smudges
- Page folds and creases
- Surface texture variation
- Marginal annotations
- Highlighted text
- Automatic Markdown ground-truth annotations
- Configurable number of generated images
- Command-line interface

---

## Project Structure

```text
synthetic-manuscript-generator/
│
├── generate.py
├── requirements.txt
├── README.md
│
├── fonts/
│   ├── NotoSansDevanagari-Regular.ttf
│   ├── NotoSansModi-Regular.ttf
│   └── NotoSansSharada-Regular.ttf
│
└── texts/
    ├── devanagari.txt
    ├── modi.txt
    └── sharada.txt
