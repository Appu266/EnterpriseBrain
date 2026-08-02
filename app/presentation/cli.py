class CLI:

    @staticmethod
    def title(
        text: str
    ) -> None:
        print(f"\n{text}\n")

    @staticmethod
    def info(
        text: str
    ) -> None:
        print(text)

    @staticmethod
    def success(
        text: str
    ) -> None:
        print(f"✓ {text}")

    @staticmethod
    def warning(
        text: str
    ) -> None:
        print(f"Warning: {text}")

    @staticmethod
    def error(
        text: str
    ) -> None:
        print(f"Error: {text}")

    @staticmethod
    def separator() -> None:
        print("-" * 70)

    @staticmethod
    def blank_line() -> None:
        print()