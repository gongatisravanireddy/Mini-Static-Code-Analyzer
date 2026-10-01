import sys

from analyzer.core import Analyzer
from report_generator import generate_text_report


def main():

    if len(sys.argv) != 2:

        print(
            "Usage: python cli.py <python_file>"
        )

        return

    filepath = sys.argv[1]

    analyzer = Analyzer(filepath)

    result = analyzer.run()

    print(
        generate_text_report(result)
    )


if __name__ == "__main__":
    main()