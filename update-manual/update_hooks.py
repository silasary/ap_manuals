import glob
import ast
import argparse


parser = argparse.ArgumentParser(description="Update manual with latest hooks.")
parser.add_argument("base_version", help="Base version to compare hooks against.")
parser.add_argument("manual_path", help="Path to the manual to update.")

args = parser.parse_args()

base_path = args.base_version
manual_path = args.manual_path

# def parse_function_tokens(tokens):
#     functions = []
#     current_function = None
#     function_indent = None
#     for token in tokens:
#         if token.type == tokenize.NAME and token.string == "def":
#             if current_function is not None:
#                 functions.append(current_function)
#             current_function = [token]
#             function_indent = 0
#         elif current_function is not None:
#             if token.line.startswith("#"):  # skip comments outside functions
#                 continue
#             current_function.append(token)
#             if token.type == tokenize.INDENT:
#                 function_indent += 1
#             elif token.type == tokenize.DEDENT:
#                 function_indent -= 1
#                 if function_indent == 0:
#                     last = current_function[-2]
#                     functions.append(current_function)
#                     current_function = None
#                     function_indent = None
#             elif token.type == tokenize.NEWLINE and function_indent == 0 and current_function[-2].string != ":":
#                 functions.append(current_function)
#                 current_function = None
#                 function_indent = None
#             elif token.type == tokenize.NEWLINE and function_indent == 0 and current_function[-2].string != ":":
#                 functions.append(current_function)
#                 current_function = None
#                 function_indent = None

#     return functions

for hook_file in glob.glob("hooks/*.py", root_dir=base_path):
    if hook_file.lower() == 'rules.py':
        continue
    print(f"Processing {hook_file}...")
    with open(f"{base_path}/{hook_file}", "r") as f:
        tree = ast.parse(f.read())
    expected_functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}

    with open(f"{manual_path}/{hook_file}", "r") as f:
        manual_code = f.read()
    tree = ast.parse(manual_code)
    found_functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}


    to_add = []
    to_update = []
    for func_name, expected_node in expected_functions.items():
        if func_name not in found_functions:
            print(f"Adding missing function {func_name} in {hook_file}...")
            to_add.append(expected_node)
        else:
            expected_args = [arg.arg for arg in expected_node.args.args]
            found_args = [arg.arg for arg in found_functions[func_name].args.args]
            if expected_args != found_args:
                print(f"Warning: function {func_name} in {hook_file} has different arguments.")
                print(f"  Expected: {expected_args}")
                print(f"  Found:    {found_args}")
                to_update.append(expected_node)
            pass

    if not to_add and not to_update:
        print(f"No changes needed for {hook_file}.")
        continue

    for new_func in to_add:
        manual_code += "\n\n" + ast.unparse(new_func) + "\n"

    for updated_func in to_update:
        pass
    pass
    with open(f"{manual_path}/{hook_file}", "w") as f:
        f.write(manual_code)
