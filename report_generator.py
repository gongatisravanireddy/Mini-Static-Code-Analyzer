from datetime import datetime


def generate_text_report(result):

    summary = result.summary()

    lines = []

    lines.append("MINI STATIC CODE ANALYZER REPORT")
    lines.append("=" * 60)

    lines.append(f"File: {result.filename}")
    lines.append(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    lines.append("")

    lines.append("SUMMARY")
    lines.append("-" * 60)

    for key, value in summary.items():
        lines.append(f"{key}: {value}")

    lines.append("")

    lines.append("ISSUES")
    lines.append("-" * 60)

    if not result.issues:

        lines.append("No issues found.")

    else:

        for issue in result.issues:
            lines.append(str(issue))

    return "\n".join(lines)


def generate_html_report(result):

    summary = result.summary()

    html = f"""
<!DOCTYPE html>

<html>

<head>

<title>Static Code Analysis Report</title>

<style>

body {{
    font-family: Arial;
    margin: 40px;
}}

h1 {{
    color: #333;
}}

.card {{
    display: inline-block;
    padding: 15px;
    margin: 10px;
    border: 1px solid #ccc;
}}

.warning {{
    color: orange;
}}

.info {{
    color: blue;
}}

.error {{
    color: red;
}}

</style>

</head>

<body>

<h1>Mini Static Code Analyzer Report</h1>

<p>
<b>File:</b> {result.filename}
</p>

<h2>Summary</h2>

<div class="card">
Unused Variables:
{summary["Unused Variable"]}
</div>

<div class="card">
Dead Code:
{summary["Dead Code"]}
</div>

<div class="card">
Duplicate Declarations:
{summary["Duplicate Declaration"]}
</div>

<div class="card">
Total:
{summary["Total"]}
</div>

<h2>Issues</h2>

"""

    if not result.issues:

        html += "<p>No issues found.</p>"

    else:

        html += "<ul>"

        for issue in result.issues:

            css_class = issue.severity.lower()

            html += f"""
<li class="{css_class}">
<b>Line {issue.line}</b>
({issue.severity})
{issue.category}: {issue.message}
</li>
"""

        html += "</ul>"

    html += """
</body>
</html>
"""

    return html