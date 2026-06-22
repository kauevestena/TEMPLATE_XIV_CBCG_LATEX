# Instructions for AI Agents and Contributors

## PDF Generation and Verification
This repository contains a LaTeX template for the XIV CBCG (Colóquio Brasileiro de Ciências Geodésicas).

- **Rendered PDFs are required:** For every change made to the LaTeX source files (`*.tex`), a new PDF version must be rendered and committed to the repository.
- **Human Verification:** These rendered PDFs are essential for humans to verify that the template is working correctly and that the layout matches the event's requirements.
- **Do NOT ignore PDFs:** The `.gitignore` file has been configured to allow tracking of `*.pdf` files. Ensure they are included in your commits.

## Build Process
To generate the PDFs, use the following sequence:
1. `pdflatex transformed.tex`
2. `bibtex transformed`
3. `pdflatex transformed.tex`
4. `pdflatex transformed.tex`

Repeat for `test_style.tex` if necessary.
