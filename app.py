from flask import Flask, render_template, request
from typing import List, Tuple

app = Flask(__name__)


def global_alignment(str1: str, str2: str) -> List[List[int]]:
    """
    Computes the global alignment and shortest edit distance between two strings using a dynamic programming approach.

    Args:
        str1 (str): The first string to align.
        str2 (str): The second string to align.

    Returns:
        List[List[int]]: A 2D list (matrix) containing the edit distances between substrings of str1 and str2.
    """
    rows, cols = len(str1) + 1, len(str2) + 1
    graph = [[float('inf') for _ in range(cols)] for _ in range(rows)]
    graph[0][0] = 0

    # Initialize the first column (deletions)
    for i in range(1, rows):
        graph[i][0] = graph[i-1][0] + 1

    # Initialize the first row (insertions)
    for j in range(1, cols):
        graph[0][j] = graph[0][j-1] + 1

    # Fill in the rest of the graph using dynamic programming
    for i in range(1, rows):
        for j in range(1, cols):
            match = graph[i-1][j-1] + (0 if str1[i-1] == str2[j-1] else 1)
            delete = graph[i-1][j] + 1
            insert = graph[i][j-1] + 1
            graph[i][j] = min(match, delete, insert)

    return graph


def get_alignment(str1: str, str2: str, graph: List[List[int]]) -> Tuple[str, str]:
    """
    Constructs the optimal alignment of two strings based on the edit distance graph.

    Args:
        str1 (str): The first string to align.
        str2 (str): The second string to align.
        graph (List[List[int]]): A 2D list (matrix) containing the edit distances between substrings of str1 and str2.

    Returns:
        Tuple[str, str]: A tuple containing two aligned strings.
    """
    aligned_str1, aligned_str2 = [], []  # Initialize lists to hold the aligned characters
    # Start from the bottom-right corner of the graph
    i, j = len(str1), len(str2)

    # Backtrack through the graph to find the optimal alignment
    while i > 0 or j > 0:
        current_cost = graph[i][j]  # Get the current cost from the graph
        # Check for a match or mismatch
        if i > 0 and j > 0 and current_cost == graph[i-1][j-1] + (0 if str1[i-1] == str2[j-1] else 1):
            aligned_str1.append(str1[i-1])  # Add character from str1
            aligned_str2.append(str2[j-1])  # Add character from str2
            i -= 1  # Move diagonally up-left in the graph
            j -= 1
        # Check for a deletion in str1
        elif i > 0 and current_cost == graph[i-1][j] + 1:
            aligned_str1.append(str1[i-1])  # Add character from str1
            aligned_str2.append('_')  # Add a gap for str2
            i -= 1  # Move up in the graph
        # Check for an insertion in str1
        else:
            aligned_str1.append('_')  # Add a gap for str1
            aligned_str2.append(str2[j-1])  # Add character from str2
            j -= 1  # Move left in the graph

    # Reverse the aligned strings as they were constructed backwards
    return ''.join(reversed(aligned_str1)), ''.join(reversed(aligned_str2))


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the main page of the web application, processing user input and displaying results.

    Returns:
        Rendered HTML template with results or the input form.
    """
    edit_distance = None  # Initialize the edit distance
    alignment_str1 = ""  # Initialize the first aligned string
    alignment_str2 = ""  # Initialize the second aligned string
    graph = []  # Initialize the alignment graph

    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        str1 = request.form['str1']  # Get the first string from the form
        str2 = request.form['str2']  # Get the second string from the form
        graph = global_alignment(str1, str2)  # Compute the alignment graph
        edit_distance = graph[-1][-1]  # Get the edit distance from the graph
        alignment_str1, alignment_str2 = get_alignment(
            str1, str2, graph)  # Compute the aligned strings

    # Render the HTML template with the results or the input form
    return render_template('index.html', edit_distance=edit_distance,
                           alignment_str1=alignment_str1,
                           alignment_str2=alignment_str2,
                           graph=graph,
                           str1=str1,
                           str2=str2)


if __name__ == "__main__":
    app.run(debug=True)
