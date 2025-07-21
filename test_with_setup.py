#!/usr/bin/env python3
"""
Test for the LaTeX fraction parsing fix with necessary setup.
"""
import sys
import os
import subprocess
import tempfile

def create_test_env():
    """Create an isolated test environment with the needed packages."""
    # Create a virtual environment
    venv_dir = tempfile.mkdtemp()
    print(f"Creating virtual environment in {venv_dir}")
    subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
    
    # Get path to pip in the virtual environment
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(venv_dir, 'Scripts', 'pip')
    else:  # Unix/Linux/Mac
        pip_path = os.path.join(venv_dir, 'bin', 'pip')
    
    # Install required packages
    print("Installing antlr4-python3-runtime")
    subprocess.run([pip_path, "install", "antlr4-python3-runtime"], check=True)
    
    # Get path to python in the virtual environment
    if os.name == 'nt':  # Windows
        python_path = os.path.join(venv_dir, 'Scripts', 'python')
    else:  # Unix/Linux/Mac
        python_path = os.path.join(venv_dir, 'bin', 'python')
    
    return python_path

def write_test_script(path):
    """Write test script to the specified path."""
    script_content = """
from sympy.parsing.latex import parse_latex
from sympy import symbols, init_printing

def test_latex_fraction():
    # Test the latex fraction parsing
    init_printing()
    
    # The problematic expression
    latex_expr = r"\\frac{\\frac{a^3+b}{c}}{\\frac{1}{c^2}}"
    
    # Parse the expression
    parsed = parse_latex(latex_expr)
    
    # Display the parsed expression
    print("Parsed expression:")
    print(parsed)
    print(f"String representation: {str(parsed)}")
    
    # Expected string representation
    expected = "((a**3 + b)/c)/(1/(c**2))"
    print(f"Expected: {expected}")
    
    # Check if the structure matches
    match = str(parsed) == expected
    print(f"Match: {match}")
    
    return match

if __name__ == "__main__":
    try:
        result = test_latex_fraction()
        exit(0 if result else 1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
"""
    
    with open(path, 'w') as f:
        f.write(script_content)

def main():
    """Main function."""
    print("Setting up test environment...")
    python_path = create_test_env()
    
    # Write test script
    test_script_path = "test_script.py"
    write_test_script(test_script_path)
    
    # Run the test
    print("Running test...")
    subprocess.run([python_path, test_script_path], check=True)

if __name__ == "__main__":
    main()