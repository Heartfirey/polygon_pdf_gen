import os
import re
import shutil
import argparse
import subprocess

POLYGON_PACKAGE_PATH_CFG = {
    'problem_tex': ['files', 'problem.tex'],
    'statements_ftl': ['files', 'statements.ftl'],
    'olymp_style_path': ['files','olymp.sty']
}

def read_ftl_file(ftl_path):
    ftl_file_lines = list()
    with open(ftl_path, "r", encoding="utf-8") as f:
        for line in f:
            ftl_file_lines.append(line)
    return ftl_file_lines

def parse_ftl_and_convert(ftl_file_lines, problem_index, contest_name, contest_location, contest_date):
    convert_tex_lines = list()
    replace_map = {
        "<#if contest.language\?\? &&.*<\/#if>" : "<del>",
        "\$\{contest.name!\}": f"{contest_name}",
        "\$\{contest.location!\}": f"{contest_location}",
        "\$\{contest.date!\}": f"{contest_date}"
    }
    for line_id in range(len(ftl_file_lines)):
        current_line = ftl_file_lines[line_id]
        # Replace ftl options and add ctex(for chinese statements)
        for pattern in replace_map.keys():
            if re.search(pattern, current_line) != None:
                replace_str = replace_map[pattern]
                if replace_map[pattern] == "<del>":
                    convert_tex_lines.append(f"\\usepackage {{ctex}}\n")
                    replace_str = ""
                current_line = re.sub(pattern, replace_str, current_line)
        # Detect the shortProblemTitle options
        if re.search('<#if shortProblemTitle\?\? && shortProblemTitle>', current_line) != None:
            if problem_index == "":
                convert_tex_lines.append(f"\\def\\ShortProblemTitle{{}}\n")
            else:
                convert_tex_lines.append(f"\\def\\ProblemIndex{{{problem_index}}}\n")
            convert_tex_lines.append(f"\\input problem.tex\n")
            convert_tex_lines.append(f"\\end {{document}}\n")
            break
        convert_tex_lines.append(current_line)

    result = ""
    for each_line in convert_tex_lines:
        result += each_line
    return result

def create_temp_dir(base_dir, lang='english'):
    print('Creating temp directory and prepare files for compile...', end='')
    statements_tex_dir = os.path.join(base_dir, 'statements', lang)
    temp_directory = os.path.join(base_dir, 'temp')
    if os.path.exists(temp_directory):
        shutil.rmtree(temp_directory)
    shutil.copytree(statements_tex_dir, temp_directory)
    style_source = os.path.join(base_dir, *POLYGON_PACKAGE_PATH_CFG['olymp_style_path'])
    style_target = os.path.join(base_dir, 'temp', 'olymp.sty')
    shutil.copyfile(style_source, style_target)
    print('OK')

def write_tex_template(base_dir, file_content):
    print("Write tex template to build directory...", end='')
    target_file_dir = os.path.join(base_dir, 'temp', 'statement.tex')
    with open(target_file_dir, "w+", encoding="utf-8") as f:
        f.write(file_content)
    print('OK')

def build_tex_document(base_dir):
    print("Start build statement PDF...", end="")
    try:
        result = subprocess.Popen("pdflatex.exe -synctex=1 -interaction=nonstopmode \"statement\".tex -shell-escape", cwd=os.path.join(base_dir, 'temp'))
    except Exception as failure:
        print(f"Failed! Info: {failure}")
    if result == 0:
        print('OK')

def move_file(base_dir, output_dir):
    file_source = os.path.join(base_dir, 'temp', 'statement.pdf')
    print(f'Moving statement file from {file_source} to {output_dir}...', end='')
    shutil.copyfile(file_source, output_dir)
    print('OK')
        
def clean(base_dir):
    print(f'Cleaning...', end='')
    shutil.rmtree(os.path.join(base_dir, 'temp'))
    print('OK')

def make_pipeline(args):
    base_dir = args.package_dir
    output_dir = args.output
    origin_ftl_content = read_ftl_file(os.path.join(base_dir, *POLYGON_PACKAGE_PATH_CFG['statements_ftl']))
    convert_ftl_content = parse_ftl_and_convert(ftl_file_lines=origin_ftl_content,
                                                problem_index=args.problem_index,
                                                contest_name=args.contest_name,
                                                contest_location=args.contest_location,
                                                contest_date=args.contest_date)
    create_temp_dir(base_dir=base_dir, lang=args.statement_lang)
    write_tex_template(base_dir=base_dir, file_content=convert_ftl_content)
    build_tex_document(base_dir=base_dir)
    move_file(base_dir=base_dir, output_dir=output_dir)
    clean(base_dir=base_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Polygon Package and Build Statement PDF.')
    parser.add_argument('package_dir', type=str, help='The problem package directory')
    parser.add_argument('--output', type=str, help='Output file directory(with filename)')
    parser.add_argument('--contest_name', type=str, default="", help='The name of contest(which is this problem belongs), default set to none.')
    parser.add_argument('--contest_location', type=str, default="", help='The location of the contest.')
    parser.add_argument('--contest_date', type=str, default="", help='The date of the contest.')
    parser.add_argument('--problem_index', type=str, default="",help='The index of this problem.')
    parser.add_argument('--statement_lang', type=str, default="english",help='must set as same as in polygon.')
    args = parser.parse_args()
    make_pipeline(args=args)