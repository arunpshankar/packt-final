#!/usr/bin/env python3
"""
Build individual chapter PDFs and the full consolidated book PDF.
Outputs all PDFs to ../book/ relative to the chapters/ directory.
"""
import subprocess
import os
import shutil

CHAPTERS_DIR = "/Users/arunprasathshankar/Desktop/repos/packt-final/chapters"
BOOK_DIR = "/Users/arunprasathshankar/Desktop/repos/packt-final/book"

PREAMBLE = r"""\documentclass[11pt, oneside, onecolumn, openany]{book}
\def\outputformat{ebook}
\usepackage{pentemplate}
\let\cleardoublepage\clearpage
\titleformat{\chapter}[display]
    {\sffamily\HUGE\fontseries{sb}\selectfont\setstretch{1.1}\raggedright}
    {\rule{0pt}{96pt}\setlength{\parskip}{0pt}\fontsize{84}{0}\fontseries{sb}\selectfont{\thechapter}}
    {0.5em}{#1}
\title{Reinforcement Learning for LLMs}
\edition{1}
\subtitle{A Complete Guide}
\author{Arun Shankar}
"""

# (chapter_counter, tex_filename, output_pdf_name)
# counter = N-1 since \mainmatter starts at 0 and first \chapter increments to 1
CHAPTERS = [
    (0,  "01_Chapter1",      "chapter01"),
    (1,  "02_Chapter2",      "chapter02"),
    (2,  "03_Chapter3",      "chapter03"),
    (3,  "04_Chapter4",      "chapter04"),
    (4,  "05_Chapter5",  "chapter05"),
    (5,  "06_Chapter6",  "chapter06"),
    (6,  "07_Chapter7",  "chapter07"),
    (7,  "08_Chapter8",  "chapter08"),
    (8,  "09_Chapter9",  "chapter09"),
    (9,  "10_Chapter10", "chapter10"),
    (10, "11_Chapter11", "chapter11"),
    (11, "12_Chapter12", "chapter12"),
    (12, "13_Chapter13", "chapter13"),
    (13, "14_Chapter14",     "chapter14"),
    (14, "15_Chapter15",     "chapter15"),
    (15, "16_Chapter16",     "chapter16"),
    (16, "17_Chapter17",     "chapter17"),
    (17, "18_Chapter18",     "chapter18"),
    (18, "19_Chapter19",     "chapter19"),
]

def run_pdflatex(texfile, cwd):
    return subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", texfile],
        capture_output=True,
        cwd=cwd,
    )

def clean(base, cwd):
    for ext in ["tex", "aux", "log", "out", "toc"]:
        try:
            os.remove(os.path.join(cwd, f"{base}.{ext}"))
        except FileNotFoundError:
            pass

os.makedirs(BOOK_DIR, exist_ok=True)

print("=== Building individual chapter PDFs ===\n")
failed = []

for counter, filename, output_name in CHAPTERS:
    print(f"  {filename}...", end=" ", flush=True)

    wrapper = PREAMBLE + rf"""
\begin{{document}}
\setcounter{{tocdepth}}{{3}}
\setlength{{\parskip}}{{0.75em minus 0.25em}}
\setstretch{{1.35}}
\mainmatter
\setcounter{{chapter}}{{{counter}}}
\input{{{filename}}}
\end{{document}}
"""
    tmp = f"_tmp_{output_name}"
    with open(os.path.join(CHAPTERS_DIR, f"{tmp}.tex"), "w") as f:
        f.write(wrapper)

    run_pdflatex(f"{tmp}.tex", CHAPTERS_DIR)
    run_pdflatex(f"{tmp}.tex", CHAPTERS_DIR)  # second pass for cross-refs

    pdf_src = os.path.join(CHAPTERS_DIR, f"{tmp}.pdf")
    pdf_dst = os.path.join(BOOK_DIR, f"{output_name}.pdf")

    if os.path.exists(pdf_src):
        shutil.move(pdf_src, pdf_dst)
        print(f"OK → book/{output_name}.pdf")
    else:
        print(f"FAILED")
        failed.append(filename)

    clean(tmp, CHAPTERS_DIR)

print(f"\n=== Building full book (thebook.pdf) ===\n")
run_pdflatex("main.tex", CHAPTERS_DIR)
run_pdflatex("main.tex", CHAPTERS_DIR)

main_pdf = os.path.join(CHAPTERS_DIR, "main.pdf")
if os.path.exists(main_pdf):
    shutil.move(main_pdf, os.path.join(BOOK_DIR, "thebook.pdf"))
    print("  OK → book/thebook.pdf")
else:
    print("  FAILED — check chapters/main.log for errors")
    failed.append("thebook")

for ext in ["aux", "log", "out", "toc"]:
    try:
        os.remove(os.path.join(CHAPTERS_DIR, f"main.{ext}"))
    except FileNotFoundError:
        pass

print(f"\n=== Done ===")
if failed:
    print(f"Failed: {', '.join(failed)}")
else:
    print(f"All PDFs written to: {BOOK_DIR}")
