from app.readers.base_reader import BaseReader


class TXTReader(BaseReader):

    def read(
        self,
        file_path: str
    ) -> str:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()