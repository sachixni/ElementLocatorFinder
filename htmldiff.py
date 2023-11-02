import difflib
from functools import wraps


def create_html_diff(file1_path, file2_path, output_html_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        file1_lines = file1.readlines()
        file2_lines = file2.readlines()

    # Compute the difference between the lines and generate HTML diff
    differ = difflib.HtmlDiff()
    html_diff = differ.make_file(file1_lines, file2_lines)

    # Save the HTML diff to the output file
    with open(output_html_path, 'w') as output_file:
        output_file.write(html_diff)

    # Paths to the two text files you want to compare


file1_path = 'xpath_1.txt'
file2_path = 'xpath_2.txt'

# Path to the output HTML file
output_html_path = 'diff.html'

# Create an HTML page highlighting the differences if there are any
with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
    file1_contents = file1.read()
    file2_contents = file2.read()

if file1_contents == file2_contents:
    # If there are no differences, show a success HTML page
    success_html = '<html><body><h1>No differences found.</h1></body></html>'
    with open(output_html_path, 'w') as output_file:
        output_file.write(success_html)
    print("No differences found.")
else:
    # If there are differences, create an HTML page highlighting them
    create_html_diff(file1_path, file2_path, output_html_path)
    print(f"Differences highlighted in '{output_html_path}'")

def html_diff_decorator(file1_path, file2_path, output_html_path):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Call the decorated function
            result = func(*args, **kwargs)

            # Check for differences and create HTML diff if necessary
            with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
                file1_contents = file1.read()
                file2_contents = file2.read()

            if file1_contents == file2_contents:
                success_html = '<html><body><h1>No differences found.</h1></body></html>'
                with open(output_html_path, 'w') as output_file:
                    output_file.write(success_html)
                print("No differences found.")
            else:
                create_html_diff(file1_path, file2_path, output_html_path)
                print(f"Differences highlighted in '{output_html_path}'")

            return result  # Return the result of the decorated function

        return wrapper

    return decorator

@html_diff_decorator('xpath_1.txt', 'xpath_2.txt', 'diff.html')
def process_files():
    # Optionally, any other processing logic you need can go here
    pass  # This is a no-operation statement, and can be removed if you have other code here

# Call the function
process_files()
