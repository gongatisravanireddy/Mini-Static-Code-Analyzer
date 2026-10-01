import ast
from .models import Issue


class DuplicateDeclarationChecker:

    def check(self, tree):

        issues = []

        issues.extend(
            self._check_duplicate_functions_classes(tree)
        )

        issues.extend(
            self._check_duplicate_imports(tree)
        )

        issues.extend(
            self._check_duplicate_variable_decls(tree)
        )

        return issues

    def _iter_scopes(self, tree):

        yield tree.body

        for node in ast.walk(tree):

            if isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                    ast.ClassDef
                )
            ):

                yield node.body

    def _check_duplicate_functions_classes(self, tree):

        issues = []

        for body in self._iter_scopes(tree):

            seen = {}

            for stmt in body:

                if isinstance(
                    stmt,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                        ast.ClassDef
                    )
                ):

                    kind = (
                        "Function"
                        if isinstance(
                            stmt,
                            (
                                ast.FunctionDef,
                                ast.AsyncFunctionDef
                            )
                        )
                        else "Class"
                    )

                    key = stmt.name

                    if key in seen:

                        issues.append(
                            Issue(
                                line=stmt.lineno,
                                category="Duplicate Declaration",
                                severity="Info",
                                message=(
                                    f"{kind} '{stmt.name}' "
                                    f"is declared again here; "
                                    f"previous declaration was at "
                                    f"line {seen[key]}."
                                ),
                            )
                        )

                    seen[key] = stmt.lineno

        return issues

    def _check_duplicate_imports(self, tree):

        issues = []

        seen = {}

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:

                    name = alias.asname or alias.name

                    if name in seen:

                        issues.append(
                            Issue(
                                line=node.lineno,
                                category="Duplicate Declaration",
                                severity="Info",
                                message=(
                                    f"Module '{name}' was already "
                                    f"imported at line {seen[name]}."
                                ),
                            )
                        )

                    seen[name] = node.lineno

            elif isinstance(node, ast.ImportFrom):

                for alias in node.names:

                    name = alias.asname or alias.name

                    full = f"{node.module}.{name}"

                    if full in seen:

                        issues.append(
                            Issue(
                                line=node.lineno,
                                category="Duplicate Declaration",
                                severity="Info",
                                message=(
                                    f"'{full}' was already imported "
                                    f"at line {seen[full]}."
                                ),
                            )
                        )

                    seen[full] = node.lineno

        return issues

    def _check_duplicate_variable_decls(self, tree):

        issues = []

        for body in self._iter_scopes(tree):

            last_assign_line = {}
            last_assign_idx = {}

            for idx, stmt in enumerate(body):

                if (
                    isinstance(stmt, ast.Assign)
                    and len(stmt.targets) == 1
                    and isinstance(
                        stmt.targets[0],
                        ast.Name
                    )
                ):

                    name = stmt.targets[0].id

                    if (
                        name in last_assign_idx
                        and last_assign_idx[name] == idx - 1
                    ):

                        issues.append(
                            Issue(
                                line=stmt.lineno,
                                category="Duplicate Declaration",
                                severity="Info",
                                message=(
                                    f"Variable '{name}' is "
                                    f"re-declared immediately "
                                    f"after its declaration at "
                                    f"line {last_assign_line[name]}."
                                ),
                            )
                        )

                    last_assign_line[name] = stmt.lineno
                    last_assign_idx[name] = idx

        return issues