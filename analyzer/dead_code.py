import ast
from .models import Issue


TERMINATORS = (
    ast.Return,
    ast.Raise,
    ast.Break,
    ast.Continue
)


class DeadCodeChecker(ast.NodeVisitor):

    def __init__(self):
        self.issues = []

    def check(self, tree):

        self.issues = []

        self.visit(tree)

        return self.issues

    def _scan_block(self, body):

        terminated_at = None

        for stmt in body:

            if terminated_at is not None:

                self.issues.append(
                    Issue(
                        line=stmt.lineno,
                        category="Dead Code",
                        severity="Warning",
                        message=(
                            f"Unreachable code detected — "
                            f"this statement can never execute "
                            f"because line {terminated_at} "
                            f"always exits the block."
                        ),
                    )
                )

                break

            if isinstance(stmt, TERMINATORS):
                terminated_at = stmt.lineno

            self.visit(stmt)

    def _check_constant_condition(self, node):

        test = node.test

        if isinstance(test, ast.Constant):

            if test.value is False or test.value == 0:

                if node.body:

                    self.issues.append(
                        Issue(
                            line=node.body[0].lineno,
                            category="Dead Code",
                            severity="Warning",
                            message=(
                                "Code inside 'if False:' "
                                "block is never executed."
                            ),
                        )
                    )

            elif test.value is True or test.value == 1:

                if node.orelse:

                    self.issues.append(
                        Issue(
                            line=node.orelse[0].lineno,
                            category="Dead Code",
                            severity="Warning",
                            message=(
                                "'else' block is unreachable "
                                "because condition is always True."
                            ),
                        )
                    )

    def visit_FunctionDef(self, node):
        self._scan_block(node.body)

    def visit_AsyncFunctionDef(self, node):
        self._scan_block(node.body)

    def visit_If(self, node):

        self._check_constant_condition(node)

        self._scan_block(node.body)

        if node.orelse:
            self._scan_block(node.orelse)

    def visit_For(self, node):

        self._scan_block(node.body)

        if node.orelse:
            self._scan_block(node.orelse)

    def visit_While(self, node):

        self._scan_block(node.body)

        if node.orelse:
            self._scan_block(node.orelse)

    def visit_Try(self, node):

        self._scan_block(node.body)

        for handler in node.handlers:
            self._scan_block(handler.body)

        if node.orelse:
            self._scan_block(node.orelse)

        if node.finalbody:
            self._scan_block(node.finalbody)

    def visit_With(self, node):
        self._scan_block(node.body)

    def visit_Module(self, node):
        self._scan_block(node.body)