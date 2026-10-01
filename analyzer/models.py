from dataclasses import dataclass, field
from typing import List


@dataclass
class Issue:
    line: int
    category: str
    severity: str
    message: str

    def __str__(self):
        return (
            f"[Line {self.line:>4}] "
            f"({self.severity}) "
            f"{self.category}: {self.message}"
        )


@dataclass
class AnalysisResult:
    filename: str
    issues: List[Issue] = field(default_factory=list)

    def by_category(self, category: str) -> List[Issue]:
        return [
            issue for issue in self.issues
            if issue.category == category
        ]

    def summary(self) -> dict:
        return {
            "Unused Variable": len(
                self.by_category("Unused Variable")
            ),
            "Dead Code": len(
                self.by_category("Dead Code")
            ),
            "Duplicate Declaration": len(
                self.by_category("Duplicate Declaration")
            ),
            "Total": len(self.issues),
        }