import re
import os

def process_file(filename):
    if not os.path.exists(filename):
        return

    with open(filename, 'r') as f:
        content = f.read()

    # Change section to Roman (idempotent)
    if r'\renewcommand{\thesection}' not in content:
        content = re.sub(r'\\begin\{document\}', r'\\renewcommand{\\thesection}{\\Roman{section}.}\n\\renewcommand{\\thesubsection}{\\thesection\\arabic{subsection}}\n\\begin{document}', content)

    # Fix Tables
    def repl_table(m):
        table_content = m.group(0)

        col_def_match = re.search(r'\\begin\{longtable\}\[\]\{([^}]+)\}', table_content)
        if col_def_match:
            cols = col_def_match.group(1)
            # Only apply if we haven't already replaced it (which we detect if there is |)
            if '|' not in cols:
                cols = cols.replace('@{}', '')
                col_specs = re.findall(r'>\{\\raggedright.*?\}p\{[^}]+\}', cols)
                if col_specs:
                    new_cols = "|".join(col_specs)
                    table_content = table_content.replace(col_def_match.group(1), new_cols)

        table_content = re.sub(r'\\toprule(?:\\noalign\{\})?\n?', r'', table_content)
        table_content = re.sub(r'\\bottomrule(?:\\noalign\{\})?\n?', r'', table_content)
        table_content = re.sub(r'\\midrule(?:\\noalign\{\})?\n?', r'\\hline\n', table_content)

        lines = table_content.split('\n')
        # Only do this if it wasn't done before
        if not any(l.endswith('\\hline') for l in lines):
            for i in range(len(lines)):
                if lines[i].strip().endswith('\\\\'):
                    if i+1 < len(lines):
                        next_line = lines[i+1].strip()
                        if not any(next_line.startswith(x) for x in ['\\hline', '\\endhead', '\\endlastfoot', '\\end{longtable}']):
                            lines[i] = lines[i] + ' \\hline'
        return '\n'.join(lines)

    content = re.sub(r'\\begin\{longtable\}.*?\\end\{longtable\}', repl_table, content, flags=re.DOTALL)

    # Handle references (idempotent)
    if r'\bibliography{references}' not in content:
        ref_idx = content.find(r'\subsubsection*{References}')
        if ref_idx == -1:
            ref_idx = content.find(r'\subsubsection{References}')
        if ref_idx != -1:
            before_ref = content[:ref_idx]
            bib_text = "\n\\renewcommand\\refname{\\vspace{-2em}} % Remove auto-generated 'References' heading if using article\n\\subsubsection*{References}\n\\nocite{*}\n\\bibliographystyle{plain}\n\\bibliography{references}\n\\end{document}"
            content = before_ref + bib_text

    # Inject background headers if missing (idempotent)
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
    if r'\usepackage{eso-pic}' not in content:
        content = content.replace(r'\begin{document}', header_bg + '\n\\begin{document}')

    with open(filename, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    # 1. Clean up script logic:
    # First, run original transformations to keep base formatting

    with open('transformed.tex', 'r') as f:
        content = f.read()

    # Original Add necessary packages and settings
    preamble = r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{mathptmx} % Times New Roman
\usepackage[left=2.1cm,right=2.1cm,top=2.1cm,bottom=2.1cm,headheight=155pt]{geometry}
\usepackage{titlesec}
\usepackage{indentfirst}
\usepackage{setspace}
\usepackage{graphicx}
\usepackage{caption}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{url}
\usepackage[hidelinks]{hyperref}
\usepackage{calc}
\usepackage{amsmath}
\usepackage{array}
\usepackage{soul}
\usepackage{xcolor}

\titleformat{\section}{\fontsize{14pt}{16.8pt}\selectfont\bfseries}{\thesection}{1em}{}
\titlespacing*{\section}{0pt}{14pt}{0pt}

\titleformat{\subsection}{\fontsize{12pt}{14.4pt}\selectfont\bfseries}{\thesubsection}{1em}{}
\titlespacing*{\subsection}{0pt}{12pt}{0pt}

\titleformat{\subsubsection}{\fontsize{12pt}{14.4pt}\selectfont\itshape}{\thesubsubsection}{1em}{}
\titlespacing*{\subsubsection}{0pt}{12pt}{0pt}

\setlength{\parindent}{0.5cm}
\setlength{\parskip}{6pt}
\setstretch{1.25} % Line spacing of at least 18pt

\pagestyle{plain} % Page numbers starting at 1, no headers

\begin{document}
"""

    if r'\usepackage{mathptmx}' not in content:
        body_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', content, re.DOTALL)
        if body_match:
            body = body_match.group(1)
        else:
            body = content

        body = re.sub(r'\\hypertarget\{[^}]*\}\{%\n', '', body)
        body = re.sub(r'\\label\{[^}]*\}\}', '', body)
        body = re.sub(r'\\section\{\\texorpdfstring\{(.*?)\s*\}\{.*\}\}', r'\\section{\1}', body)
        body = re.sub(r'\\subsection\{\\texorpdfstring\{(.*?)\s*\}\{.*\}\}', r'\\subsection{\1}', body)
        body = re.sub(r'\\subsubsection\{\\texorpdfstring\{(.*?)\s*\}\{.*\}\}', r'\\subsubsection{\1}', body)
        body = re.sub(r'\\section\{([^}]*)\}\}', r'\\section{\1}', body)
        body = re.sub(r'\\subsection\{([^}]*)\}\}', r'\\subsection{\1}', body)
        body = re.sub(r'\\subsubsection\{([^}]*)\}\}', r'\\subsubsection{\1}', body)

        # Replace Title Block
        if r'\textbf{Full paper Template: Author Guidelines}' in body:
            body = re.sub(r'\\textbf\{Full paper Template: Author Guidelines\}', r'\\begin{center}\n\\vspace*{3.5em}\\fontsize{16pt}{19.2pt}\\selectfont\\textbf{Full paper Template: Author Guidelines}\\vspace{12pt}\n\\end{center}', body)

        if r'First Author\textsuperscript{1}, Second Author \textsuperscript{2},' in body:
            body = re.sub(r'First Author\\textsuperscript\{1\}, Second Author \\textsuperscript\{2\},\nThird Author \\textsuperscript\{2\}\*',
                          r'\\begin{center}\n\\fontsize{12pt}{14.4pt}\\selectfont {\\color{red}First Author\\textsuperscript{1}, Second Author \\textsuperscript{2}, Third Author \\textsuperscript{2}*}\\vspace{12pt}\n\\end{center}', body)

        if r'\textsuperscript{1} Department' in body:
            body = re.sub(r'\\begin\{quote\}\n\\textsuperscript\{1\} Department.*?approved\n\\end\{quote\}',
                          r'\\begin{center}\n\\fontsize{12pt}{14.4pt}\\selectfont \\color{red}\n\\textsuperscript{1} Department/Unit (if applicable), Organization, City, Brazil, author1@email.com.br*\n\n\\textsuperscript{2} Department/Unit (if applicable), Organization, City, Brazil, \\{author2, author3\\}@email.com.br *\n\n*Those information should be filled only after the work has been approved\n\\end{center}', body, flags=re.DOTALL)

        # Fix Abstract text alignment
        body = re.sub(r'\\textbf\{Abstract\}', r'\\noindent\\textbf{Abstract}', body)

        # Fix Keyword line
        body = re.sub(r'\\textbf\{Keywords:\}', r'\\noindent\\textbf{Keywords:}', body)

        content = preamble + body + "\n\\end{document}\n"
        with open('transformed.tex', 'w') as f:
            f.write(content)

    # Then apply new formatting rules
    process_file('transformed.tex')
    process_file('test_style.tex')
