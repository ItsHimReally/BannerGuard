from typing import Any, Optional
import pathlib
import shutil

import cv2

import app.tois_aggregation as tois_aggregation
import app.types as stypes


class Program:
    def __init__(self, base_path: pathlib.Path) -> None:
        self.toia = tois_aggregation.ToisAggregation(base_path)

    def run(self) -> None:
        export_path = pathlib.Path("./contents")
        export_path.mkdir(parents=True, exist_ok=True)
        
        for toi in self.toia.tois:
            # num = toi.num
            # num_path = export_path / str(num)
            # toi_path = num_path / "toi"
            # toi_path.mkdir(parents=True, exist_ok=True)
            # content_path = num_path / "content"
            # content_path.mkdir(parents=True, exist_ok=True)
            
            # toi_files = self.toia.get_toi_files(toi.num)
            # for toi_file in toi_files:
            #     shutil.copy(toi_file, toi_path / toi_file.name)
            #     # toi_file.rename(toi_path / toi_file.name)
            
            content_ids = toi.ids
            
            for content_id in content_ids:
                part_content_files = self.toia.get_content_files(content_id, toi.size)
                for part_content_file in part_content_files:
                    # part_content_file.rename(curr_content_path / part_content_file.name)
                    new_path = export_path / part_content_file.name
                    shutil.copy(part_content_file, new_path)


    # def run(self) -> None:
    #     export_path = pathlib.Path("./export")
    #     export_path.mkdir(parents=True, exist_ok=True)
        
    #     for toi in self.toia.tois:
    #         num = toi.num
    #         num_path = export_path / str(num)
    #         toi_path = num_path / "toi"
    #         toi_path.mkdir(parents=True, exist_ok=True)
    #         content_path = num_path / "content"
    #         content_path.mkdir(parents=True, exist_ok=True)
            
    #         toi_files = self.toia.get_toi_files(toi.num)
    #         for toi_file in toi_files:
    #             shutil.copy(toi_file, toi_path / toi_file.name)
    #             # toi_file.rename(toi_path / toi_file.name)
            
    #         content_ids = toi.ids
            
    #         for content_id in content_ids:
    #             part_content_files = self.toia.get_content_files(content_id, toi.size)
    #             curr_content_path = content_path / str(content_id)
    #             curr_content_path.mkdir(parents=True, exist_ok=True)
    #             for part_content_file in part_content_files:
    #                 # part_content_file.rename(curr_content_path / part_content_file.name)
    #                 shutil.copy(part_content_file, curr_content_path / part_content_file.name)



def main() -> None:
    base_path = pathlib.Path("./data/")

    program = Program(base_path)
    program.run()


if __name__ == "__main__":
    main()
