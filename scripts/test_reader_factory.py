from app.factories.reader_factory import ReaderFactory
from app.readers.txt_reader import TXTReader


def main() -> None:
    test_files = [
        "sample.txt",
        "package.sql",
        "package_spec.pks",
        "package_body.pkb",
        "procedure.pls",
        "document.pdf",
    ]

    print("\nReader Factory Test\n")

    for file_path in test_files:
        is_supported = ReaderFactory.supports(
            file_path
        )

        print(
            f"{file_path}: "
            f"{'supported' if is_supported else 'not supported'}"
        )

        if not is_supported:
            continue

        reader = ReaderFactory.create(
            file_path
        )

        print(
            f"  Reader: {type(reader).__name__}"
        )

        if not isinstance(
            reader,
            TXTReader
        ):
            raise AssertionError(
                f"Expected TXTReader for {file_path}"
            )

    print()
    print(
        "Supported extensions: "
        f"{sorted(ReaderFactory.supported_extensions())}"
    )

    print()
    print("Reader factory test completed successfully.")


if __name__ == "__main__":
    main()