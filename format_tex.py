import re

def process_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # Change section to Roman
    content = re.sub(r'\\begin\{document\}', r'\\renewcommand{\\thesection}{\\Roman{section}.}\n\\renewcommand{\\thesubsection}{\\thesection\\arabic{subsection}}\n\\begin{document}', content)

    # Fix Tables
    def repl_table(m):
        table_content = m.group(0)

        col_def_match = re.search(r'\\begin\{longtable\}\[\]\{([^}]+)\}', table_content)
        if col_def_match:
            cols = col_def_match.group(1)
            cols = cols.replace('@{}', '')
            col_specs = re.findall(r'>\{\\raggedright.*?\}p\{[^}]+\}', cols)
            if col_specs:
                new_cols = "|".join(col_specs)
                table_content = table_content.replace(col_def_match.group(1), new_cols)

        table_content = re.sub(r'\\toprule(?:\\noalign\{\})?\n?', r'', table_content)
        table_content = re.sub(r'\\bottomrule(?:\\noalign\{\})?\n?', r'', table_content)
        table_content = re.sub(r'\\midrule(?:\\noalign\{\})?\n?', r'\\hline\n', table_content)

        lines = table_content.split('\n')
        for i in range(len(lines)):
            if lines[i].strip().endswith('\\\\'):
                if i+1 < len(lines):
                    next_line = lines[i+1].strip()
                    if not any(next_line.startswith(x) for x in ['\\hline', '\\endhead', '\\endlastfoot', '\\end{longtable}']):
                        lines[i] = lines[i] + ' \\hline'
        return '\n'.join(lines)

    content = re.sub(r'\\begin\{longtable\}.*?\\end\{longtable\}', repl_table, content, flags=re.DOTALL)

    # Handle references
    ref_idx = content.find(r'\subsubsection*{References}')
    if ref_idx == -1:
        ref_idx = content.find(r'\subsubsection{References}')
    if ref_idx != -1:
        before_ref = content[:ref_idx]
        bib_text = "\n\\renewcommand\\refname{\\vspace{-2em}} % Remove auto-generated 'References' heading if using article\n\\subsubsection*{References}\n\\bibliographystyle{plain}\n\\bibliography{references}\n\\end{document}"
        content = before_ref + bib_text

    # Inject background headers if missing
    header_bg = r"""
\usepackage{eso-pic}
\AddToShipoutPictureBG*{%
  \AtPageLowerLeft{%
    \includegraphics[width=\paperwidth,height=\paperheight]{header_bg.jpg}%
  }%
  \AtPageUpperLeft{%
    \put(0,-115){\includegraphics[width=\paperwidth]{header_fg.jpg}}%
  }%
}
"""
    if "eso-pic" not in content:
        content = content.replace(r'\begin{document}', header_bg + '\n\\begin{document}')

    with open(filename, 'w') as f:
        f.write(content)

process_file('transformed.tex')
process_file('test_style.tex')
