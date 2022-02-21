from functools import reduce


def check_dimensions(table: list[list[any]]) -> bool:
    return \
        reduce(lambda x, y: (x[0] and (x[1] == len(y)), len(y)), table, (True, len(table[0])))[0]


def generate_latex_table(table: list[list[any]]) -> str:
    nl = '\n'
    nl_latex = '\\\\'
    return f"""{{{' '.join(map(lambda _: 'X', range(len(table[0]))))}}}
{nl.join(map(lambda x: f"{' & '.join(map(str, x))}{nl_latex}", table))}"""


def generate_latex_doc_with_table(table: list[list[any]]) -> str:
    if not check_dimensions(table):
        raise ValueError("Table should be correct rectangle")

    table_str = generate_latex_table(table)

    return f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[russian]{{babel}}
\\usepackage{{tabularx}}

\\begin{{document}}

\\begin{{tabularx}}{{\\textwidth}}{table_str}
\\end{{tabularx}}

\\end{{document}}
"""


def main():
    """
    Content should not be empty and should be a correct rectangle.
    According to this constraints, you can fill it how you want
    """
    content = [['afdfdhhhhhhhhhhh fhaaaaaaaaaaaaa afhhhhhhhhhhhhhh afhhhhhhhhhhhhhhh fhdaaaaaaaaaaaaaaa', 2, 3], [1, 2, 3]]
    with open("artifacts/table.tex", 'w') as table:
        table.write(generate_latex_doc_with_table(content))


if __name__ == "__main__":
    main()
