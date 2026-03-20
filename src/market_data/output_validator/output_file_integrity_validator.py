import os
from typing import Iterable, List, Union

from src.error.error import InputDataError


class OutputFileIntegrityValidator:
    """Validate expected output files and return missing file paths."""

    @classmethod
    def get_missed_files_list(
        cls,
        target_output_path: Union[str, os.PathLike, List[Union[str, os.PathLike, List[str]]]],
        min_file_size_bytes: int = 1,
    ) -> List[str]:
        """Return missing or incomplete files from target output paths.

        Args:
            target_output_path (Union[str, os.PathLike, List[Union[str, os.PathLike, List[str]]]]):
                Target output file path(s).
                Supports a single path, a list of paths, or nested path lists.
            min_file_size_bytes (int): Minimum valid file size in bytes.

        Returns:
            List[str]: Missing file list.
        """
        if min_file_size_bytes < 0:
            raise InputDataError(
                message=f'min_file_size_bytes must be non-negative, got [{min_file_size_bytes}]'
            )

        target_files = cls._flatten_target_output_path(target_output_path)
        if not target_files:
            return []

        missed_files = []
        for file_path in target_files:
            normalized_path = os.path.abspath(file_path)
            if not os.path.exists(normalized_path):
                missed_files.append(normalized_path)
                continue
            if not os.path.isfile(normalized_path):
                missed_files.append(normalized_path)
                continue
            if os.path.getsize(normalized_path) < min_file_size_bytes:
                missed_files.append(normalized_path)

        # Keep order while removing duplicates.
        return list(dict.fromkeys(missed_files))

    @classmethod
    def _flatten_target_output_path(
        cls,
        target_output_path: Union[str, os.PathLike, Iterable],
    ) -> List[str]:
        """Flatten target output paths into a single string path list.

        Args:
            target_output_path (Union[str, os.PathLike, Iterable]): Nested target output path structure.

        Returns:
            List[str]: Flattened path list.
        """
        if isinstance(target_output_path, os.PathLike):
            return [os.fspath(target_output_path)]

        if isinstance(target_output_path, str):
            return [target_output_path]

        if not isinstance(target_output_path, Iterable):
            raise InputDataError(
                message=f'Unsupported target_output_path type: [{type(target_output_path)}]'
            )

        output_paths = []
        for value in target_output_path:
            if isinstance(value, os.PathLike):
                output_paths.append(os.fspath(value))
            elif isinstance(value, str):
                output_paths.append(value)
            elif isinstance(value, Iterable):
                output_paths.extend(cls._flatten_target_output_path(value))
            else:
                raise InputDataError(
                    message=f'Unsupported target_output_path item type: [{type(value)}]'
                )
        return output_paths
