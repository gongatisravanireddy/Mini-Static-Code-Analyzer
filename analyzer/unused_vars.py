import ast
from .models import Issue


class ScopeCollector(ast.NodeVisitor):

    def __init__(self):
        self.assigned = {}
        self.used = set()
        self.augmented = set()

    def visit_FunctionDef(self, node):
        pass

    def visit_AsyncFunctionDef(self, node):
        pass

    def visit_ClassDef(self, node):
        pass

    def visit_Name(self, node):

        if isinstance(node.ctx, ast.Store):

            if node.id not in self.assigned:
                self.assigned[node.id] = node.lineno

        elif isinstance(node.ctx, ast.Load):

            self.used.add(node.id)

        self.generic_visit(node)

    def visit_AugAssign(self, node):

        if isinstance(node.target, ast.Name):

            self.used.add(node.target.id)

            if node.target.id not in self.assigned:
                self.assigned[node.target.id] = node.lineno

        self.generic_visit(node)

    def visit_Global(self, node):

        for name in node.names:
            self.used.add(name)

        self.generic_visit(node)

    def visit_Nonlocal(self, node):

        for name in node.names:
            self.used.add(name)

        self.generic_visit(node)


IGNORED_NAMES = {"_", "self", "cls"}


class UnusedVariableChecker:

    def check(self, tree):

        issues = []

        scopes = self._collect_scopes(tree)

        for scope_node, body_owner in scopes:

            collector = ScopeCollector()

            for stmt in scope_node:
                collector.visit(stmt)

            for name, lineno in collector.assigned.items():

                if name in IGNORED_NAMES:
                    continue

                if name.startswith("_"):
                    continue

                if name not in collector.used:

                    issues.append(
                        Issue(
                            line=lineno,
                            category="Unused Variable",
                            severity="Warning",
                            message=(
                                f"Variable '{name}' is assigned "
                                f"but never used "
                                f"(in {body_owner})."
                            ),
                        )
                    )

        return issues

    def _collect_scopes(self, tree):

        scopes = [
            (tree.body, "module scope")
        ]

        for node in ast.walk(tree):

            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            ):

                scopes.append(
                    (
                        node.body,
                        f"function '{node.name}'"
                    )
                )

        return scopes