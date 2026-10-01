# Mini Static Code Analyzer

## Project Overview

Mini Static Code Analyzer is a Python-based tool that analyzes source code without executing it.

It helps identify common code quality issues such as:

- Duplicate code
- Dead code
- Unused variables
- Syntax errors
- Basic code structure issues

The project provides both **CLI and GUI interfaces** and can generate analysis reports.

## Features

- Static code analysis
- Duplicate code detection
- Dead code detection
- Unused variable detection
- Syntax error detection
- Code structure analysis
- CLI interface
- GUI interface
- HTML report generation

## Project Structure

```text
Mini-Static-Code-Analyzer/
│
├── analyzer/
│   ├── core.py
│   ├── duplicates.py
│   ├── dead_code.py
│   ├── unused_vars.py
│   ├── models.py
│   └── __init__.py
│
├── sample_tests/
│   ├── test1.py
│   ├── test2_clean.py
│   └── test3_syntax_error.py
│
├── reports/
│   └── test1_report.html
│
├── gui.py
├── cli.py
├── report_generator.py
├── requirements.txt
└── README.md


## How It Works

```text
Python Source Code
        ↓
Code Parsing
        ↓
Static Analysis
        ↓
Issue Detection
        ↓
Report Generation
        ↓
Analysis Results

##Technologies Used

'''text
- Python
- Python AST
- Static Code Analysis
- HTML
- Tkinter / GUI
- CLI
How to Run
Install Dependencies
pip install -r requirements.txt

Run CLI
python cli.py

Run GUI
python gui.py

Sample Tests
The project includes sample Python files for testing:
- test1.py
- test2_clean.py
- test3_syntax_error.py
These files are used to demonstrate different code analysis cases.
Report Generation
The analyzer can generate an HTML report containing the detected code issues.
Example:
reports/
└── test1_report.html

Future Scope
- Add more static analysis rules.
- Support additional programming languages.
- Add code complexity analysis.
- Improve the graphical interface.
- Add automated code quality suggestions.
Conclusion
Mini Static Code Analyzer provides a simple way to analyze Python source code without executing it.
The project demonstrates the practical use of Python, static code analysis, AST-based parsing, CLI development, GUI development, and report generation.
