import re

with open('transformed.tex', 'r') as f:
    content = f.read()

# Fix \arraybackslash missing requirement: \usepackage{array}
if r'\usepackage{array}' not in content:
    content = content.replace(r'\usepackage{calc}', r'\usepackage{calc}' + '\n' + r'\usepackage{array}')

# \real{} is missing? \usepackage{calc} is included. Ah, arraybackslash is from array package
# Pandoc also uses \ul for underlines, so include soul package
if r'\usepackage{soul}' not in content:
    content = content.replace(r'\usepackage{array}', r'\usepackage{array}' + '\n' + r'\usepackage{soul}')

with open('transformed.tex', 'w') as f:
    f.write(content)
