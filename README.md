# XIV CBCG LaTeX Template

This repository contains the LaTeX version of the template for the **XIV Brazilian Colloquium on Geodetic Sciences (Colóquio Brasileiro de Ciências Geodésicas - CBCG)**.

The original MS Word template can be found [here](https://cbcg.ufpr.br/wp-content/uploads/2026/05/xiv_cbcg_full-paper_template.docx).
For more information about the event, visit the [official website](https://cbcg.ufpr.br).

## Project Structure

- `transformed.tex`: The main LaTeX template file.
- `test_style.tex`: A secondary LaTeX file used for style testing.
- `references.bib`: Bibliography file containing sample references.
- `header.png`: Header image for the template.
- `watermark.png`: Watermark image for the template.
- `transformed.pdf`: Rendered version of the main template (for verification).
- `test_style.pdf`: Rendered version of the style test (for verification).
- `AGENTS.md`: Special instructions for AI agents and contributors regarding PDF maintenance.

## How to Compile

To generate the PDF from the LaTeX source, you should have a LaTeX distribution installed (e.g., TeX Live). Use the following commands in your terminal:

```bash
pdflatex transformed.tex
bibtex transformed
pdflatex transformed.tex
pdflatex transformed.tex
```

## Contributing

If you are contributing to this repository or using an AI agent to make changes, please refer to [AGENTS.md](AGENTS.md) for important instructions regarding the tracking of rendered PDF files.

## License

This project is licensed under the terms of the LICENSE file included in the repository.
