import re

with open('transformed.tex', 'r') as f:
    content = f.read()

# Add necessary packages and settings
preamble = r"""\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{mathptmx} % Times New Roman
\usepackage[margin=2cm]{geometry}
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

# Extract body content (between \begin{document} and \end{document})
body_match = re.search(r'\\begin\{document\}(.*?)\\end\{document\}', content, re.DOTALL)
if body_match:
    body = body_match.group(1)
else:
    body = content

# Perform some basic cleanups for Pandoc artifacts
# Remove hypertarget / label around sections
body = re.sub(r'\\hypertarget\{[^}]*\}\{%\n', '', body)
body = re.sub(r'\\label\{[^}]*\}\}', '', body)
# Fix section headings wrapped in \texorpdfstring
body = re.sub(r'\\section\{\\texorpdfstring\{(.*?)\s*\}\{.*\}\}', r'\\section{\1}', body)
body = re.sub(r'\\subsection\{\\texorpdfstring\{(.*?)\s*\}\{.*\}\}', r'\\subsection{\1}', body)
body = re.sub(r'\\subsubsection\{\\texorpdfstring\{(.*?)\s*\}\{.*\}\}', r'\\subsubsection{\1}', body)
# Clean up remaining trailing bracket
body = re.sub(r'\\section\{([^}]*)\}\}', r'\\section{\1}', body)
body = re.sub(r'\\subsection\{([^}]*)\}\}', r'\\subsection{\1}', body)
body = re.sub(r'\\subsubsection\{([^}]*)\}\}', r'\\subsubsection{\1}', body)

# Replace the beginning with our custom preamble
# We reconstruct the document
new_content = preamble + body + "\n\\end{document}\n"

with open('transformed.tex', 'w') as f:
    f.write(new_content)
