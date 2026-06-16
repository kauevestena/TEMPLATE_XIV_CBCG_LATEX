import re

with open('transformed.tex', 'r') as f:
    content = f.read()

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
\usepackage{eso-pic}
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage{array}
\usepackage{soul}

\titleformat{\section}{\fontsize{14pt}{16.8pt}\selectfont\bfseries}{\thesection}{1em}{}
\titlespacing*{\section}{0pt}{14pt}{0pt}

\titleformat{\subsection}{\fontsize{12pt}{14.4pt}\selectfont\bfseries}{\thesubsection}{1em}{}
\titlespacing*{\subsection}{0pt}{12pt}{0pt}

\titleformat{\subsubsection}{\fontsize{12pt}{14.4pt}\selectfont\itshape}{\thesubsubsection}{1em}{}
\titlespacing*{\subsubsection}{0pt}{12pt}{0pt}

\setlength{\parindent}{0.5cm}
\setlength{\parskip}{6pt}
\setstretch{1.25} % Line spacing of at least 18pt

\pagestyle{plain}

\AddToShipoutPictureBG*{%
  \AtPageLowerLeft{%
    \includegraphics[width=\paperwidth,height=\paperheight]{header_bg.jpg}%
  }%
  \AtPageUpperLeft{%
    \put(0,-115){\includegraphics[width=\paperwidth]{header_fg.jpg}}%
  }%
}

\begin{document}
"""

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

# Fix Title
body = re.sub(r'\\textbf\{Full paper Template: Author Guidelines\}', r'\\begin{center}\n\\vspace*{3.5em}\\fontsize{16pt}{19.2pt}\\selectfont\\textbf{Full paper Template: Author Guidelines}\\vspace{12pt}\n\\end{center}', body)

# Fix Authors block roughly
body = re.sub(r'First Author\\textsuperscript\{1\}, Second Author \\textsuperscript\{2\},\nThird Author \\textsuperscript\{2\}\*',
              r'\\begin{center}\n\\fontsize{12pt}{14.4pt}\\selectfont {\\color{red}First Author\\textsuperscript{1}, Second Author \\textsuperscript{2}, Third Author \\textsuperscript{2}*}\\vspace{12pt}\n\\end{center}', body)

body = re.sub(r'\\begin\{quote\}\n\\textsuperscript\{1\} Department.*?approved\n\\end\{quote\}',
              r'\\begin{center}\n\\fontsize{12pt}{14.4pt}\\selectfont \\color{red}\n\\textsuperscript{1} Department/Unit (if applicable), Organization, City, Brazil, author1@email.com.br*\n\n\\textsuperscript{2} Department/Unit (if applicable), Organization, City, Brazil, \\{author2, author3\\}@email.com.br *\n\n*Those information should be filled only after the work has been approved\n\\end{center}', body, flags=re.DOTALL)

# Fix Abstract text alignment
body = re.sub(r'\\textbf\{Abstract\}', r'\\noindent\\textbf{Abstract}', body)

# Fix Keyword line
body = re.sub(r'\\textbf\{Keywords:\}', r'\\noindent\\textbf{Keywords:}', body)

new_content = preamble + body + "\n\\end{document}\n"

with open('transformed.tex', 'w') as f:
    f.write(new_content)
