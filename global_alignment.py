# Create the function that uses a 2-Dimensional graph to find the global alignment and shortest edit distance between two strings
from typing import List


def global_alignment(str1: str, str2: str) -> List[List[int]]:
    """
    Computes the global alignment and shortest edit distance between two strings using a dynamic programming approach.

    Args:
        str1 (str): The first string to align.
        str2 (str): The second string to align.

    Returns:
        List[List[int]]: A 2D list (matrix) containing the edit distances between substrings of str1 and str2.
    """
    # Determine the number of rows and columns needed for the graph (matrix)
    # We add 1 to the lengths of the strings to account for the initial empty string row and column
    rows, cols = len(str1) + 1, len(str2) + 1

    # Initialize a 2-Dimensional graph (matrix) filled with infinity
    # This will hold the minimum edit distances between substrings of str1 and str2
    graph = [[float('inf') for _ in range(cols)] for _ in range(rows)]

    # Set the starting point of the graph
    # The distance to convert an empty string to an empty string is 0
    graph[0][0] = 0

    # Initialize the first column of the graph
    # This represents the cost of transforming str1 into an empty string (deletions)
    for i in range(1, rows):
        graph[i][0] = graph[i-1][0] + 1  # Each deletion costs 1

    # Initialize the first row of the graph
    # This represents the cost of transforming an empty string into str2 (insertions)
    for j in range(1, cols):
        graph[0][j] = graph[0][j-1] + 1  # Each insertion costs 1

    # Rest of the algorithm
    # Fill in the rest of the graph using dynamic programming
    # Iterate through each cell in the graph starting from (1, 1)
    for i in range(1, rows):
        for j in range(1, cols):
            # Calculate the cost for matching or mismatching characters
            # 0 for match, 1 for mismatch
            match = graph[i-1][j-1] + (0 if str1[i-1] == str2[j-1] else 1)

            # Calculate the cost for deletion
            delete = graph[i-1][j] + 1  # Deleting a character from str1

            # Calculate the cost for insertion
            insert = graph[i][j-1] + 1  # Inserting a character into str1

            # Store the minimum cost among match, delete, and insert in the current cell
            # Minimum of the three options
            graph[i][j] = min(match, delete, insert)

    # Return the completed graph, which includes the edit distances
    return graph  # or whatever your function needs to return


def get_alignment(str1: str, str2: str, graph: List[List[int]]) -> str:
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


if __name__ == "__main__":
    # Example strings for alignment
    str1 = "evaluation"
    str2 = "elution"

    # Call the global alignment function
    result = global_alignment(str1, str2)

    # Output the result
    # Print the edit distance from the bottom-right cell of the matrix
    print("Edit distance (global alignment):", result[-1][-1])
    print("Alignment matrix:")
    print(str2)  # Print the second string as a header for the matrix
    for row in result:
        print(row)  # Print the entire alignment matrix for visualization
