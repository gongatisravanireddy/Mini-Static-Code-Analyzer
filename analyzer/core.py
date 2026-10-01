import ast

from .models import Issue, AnalysisResult
from .unused_vars import UnusedVariableChecker
from .dead_code import DeadCodeChecker
from .duplicates import DuplicateDeclarationChecker


class Analyzer:

    def __init__(self, filepath: str):

        self.filepath = filepath

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as f:

            self.source = f.read()

    def run(self):

        result = AnalysisResult(
            filename=self.filepath
        )

        # ==========================================
        # STEP 1: Parse Python source code
        # ==========================================

        try:

            tree = ast.parse(
                self.source,
                filename=self.filepath
            )

        except SyntaxError as e:

            result.issues.append(
                Issue(
                    line=e.lineno or 0,
                    category="Syntax Error",
                    severity="Error",
                    message=(
                        f"Invalid Python syntax: {e.msg}"
                    )
                )
            )

            return result

        # ==========================================
        # STEP 2: Run static analysis checkers
        # ==========================================

        checkers = [

            UnusedVariableChecker(),

            DeadCodeChecker(),

            DuplicateDeclarationChecker()

        ]

        for checker in checkers:

            result.issues.extend(
                checker.check(tree)
            )

        # ==========================================
        # STEP 3: Sort issues by line number
        # ==========================================

        result.issues.sort(
            key=lambda issue: issue.line
        )

        return result