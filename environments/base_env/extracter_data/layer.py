from extract_data_file.data_extracter import DataExtracter
from dataclasses import dataclass


@dataclass(frozen=True)
class LayerParams:
    width: int
    height: int

    gates: list[list[int, int]]
    shelves: list[list[int, int]]


class LayersParamsExtracter(DataExtracter):

    @staticmethod
    def extract(data) -> LayerParams:
        env = data['base_env']

        return LayerParams(
            width=env['width'],
            height=env['height'],

            gates=env['gates'],
            shelves=env['shelves'],
        )