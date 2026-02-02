"""
Grid Visualization Helper
This script helps visualize the grid structure and understand node numbering.
"""

def visualize_grid(n, marked_nodes=None):
    """
    Visualize an N×N grid with numbered nodes.
    
    Args:
        n: Grid size
        marked_nodes: Dictionary of {node: label} to mark special nodes
    """
    if marked_nodes is None:
        marked_nodes = {}
    
    print(f"\n{n}×{n} Grid Visualization")
    print("=" * (n * 8))
    print()
    
    # Print column numbers
    print("     ", end="")
    for col in range(n):
        print(f"Col{col:2d}  ", end="")
    print("\n")
    
    for row in range(n):
        print(f"Row {row}: ", end="")
        for col in range(n):
            node = row * n + col + 1
            if node in marked_nodes:
                print(f"[{node:2d}]*  ", end="")
            else:
                print(f" {node:2d}    ", end="")
        print()
    
    print("\n" + "=" * (n * 8))
    
    if marked_nodes:
        print("\nMarked Nodes:")
        for node, label in marked_nodes.items():
            row = (node - 1) // n
            col = (node - 1) % n
            print(f"  Node {node:2d} ({label}): Row {row}, Col {col}")


def calculate_manhattan_distance(node1, node2, n):
    """Calculate Manhattan distance between two nodes in the grid."""
    row1, col1 = (node1 - 1) // n, (node1 - 1) % n
    row2, col2 = (node2 - 1) // n, (node2 - 1) % n
    return abs(row1 - row2) + abs(col1 - col2)


if __name__ == "__main__":
    # Visualize the 5×5 grid from Test Case 1
    print("\n" + "="*60)
    print("Test Case 1: Grid City (5×5)")
    print("="*60)
    
    marked = {
        10: "BurgerPalace",
        7: "Beef",
        15: "Zinger",
        18: "PizzaPlanet",
        21: "Tikka"
    }
    
    visualize_grid(5, marked)
    
    print("\n\nDistance Calculations:")
    print("-" * 60)
    print(f"BurgerPalace (10) → Beef (7): {calculate_manhattan_distance(10, 7, 5)} units")
    print(f"BurgerPalace (10) → Zinger (15): {calculate_manhattan_distance(10, 15, 5)} units")
    print(f"Zinger (15) → Beef (7): {calculate_manhattan_distance(15, 7, 5)} units")
    print(f"PizzaPlanet (18) → Tikka (21): {calculate_manhattan_distance(18, 21, 5)} units")
    
    # Visualize a 3×3 grid
    print("\n\n" + "="*60)
    print("Test Case 3: Grid City (3×3)")
    print("="*60)
    
    marked_3x3 = {
        5: "FastFood",
        1: "Burger",
        9: "Fries",
        7: "PizzaShop",
        3: "Pizza"
    }
    
    visualize_grid(3, marked_3x3)
    
    print("\n\nDistance Calculations:")
    print("-" * 60)
    print(f"FastFood (5) → Burger (1): {calculate_manhattan_distance(5, 1, 3)} units")
    print(f"Burger (1) → Fries (9): {calculate_manhattan_distance(1, 9, 3)} units")
    print(f"PizzaShop (7) → Pizza (3): {calculate_manhattan_distance(7, 3, 3)} units")
