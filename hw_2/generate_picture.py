import subprocess

from ast_visualizer.main import print_ast

from generate_table import check_dimensions, generate_latex_table


def generate_latex_doc_with_table_and_picture(table: list[list[any]], picture_path: str) -> str:
    if not check_dimensions(table):
        raise ValueError("Table should be correct rectangle")

    table_str = generate_latex_table(table)

    return f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[russian]{{babel}}
\\usepackage{{tabularx}}
\\usepackage{{graphicx}}

\\begin{{document}}

\\begin{{tabularx}}{{\\textwidth}}{table_str}
\\end{{tabularx}}

\\includegraphics[width=\\linewidth]{{{picture_path}}}

\\end{{document}}
"""


def main():
    """
        Content should not be empty and should be a correct rectangle.
        According to this constraints, you can fill it how you want
        """
    content = [['afdfdhhhhhhhhhhh fhaaaaaaaaaaaaa afhhhhhhhhhhhhhh afhhhhhhhhhhhhhhh fhdaaaaaaaaaaaaaaa', 2, 3],
               [1, 2, 3]]
    picture_path = "artifacts/ast.png"
    with open("artifacts/picture.tex", 'w') as table:
        table.write(generate_latex_doc_with_table_and_picture(content, picture_path))
    print_ast(picture_path)
    subprocess.run(["pdflatex", "-output-directory", "artifacts", "artifacts/picture.tex"])


if __name__ == "__main__":
    main()
