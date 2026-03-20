from typing import List, Optional

from src.connection.infra.http import get_token
from src.connection.extraction.on_demand_extractor.on_demand_extractor import OnDemandExtractor
from src.multi_thread.implement.multi_threads_imp import MultiThreadsImp


class ExtractionImp(MultiThreadsImp):

    """Represents extraction imp."""
    def __init__(self, extractioners: List[OnDemandExtractor], nums_of_threads: Optional[int] = None):
        """Initialize the instance.

        Args:
            extractioners (List[OnDemandExtractor]): Input value for extractioners.
            nums_of_threads (Optional[int]): Input value for max thread count.

        Returns:
            None: No value is returned.
        """
        self.extractioners = extractioners
        self.nums_of_threads = self._resolve_nums_of_threads(
            total_tasks=len(extractioners),
            nums_of_threads=nums_of_threads,
        )

    def get_locations(self, token=None):
        """Return locations.

        Args:
            token (object): Authentication token used for API requests.

        Returns:
            object: Requested value for the lookup.
        """
        token = get_token() if token is None else token

        funcs = [extractioner.get_location for extractioner in self.extractioners]
        self._run_chunked_threads(funcs=funcs, shared_input=(token,))
        locations = [ele.location for ele in self.extractioners]

        return locations

    def get_job_ids(self, token=None):
        """Return job ids.

        Args:
            token (object): Authentication token used for API requests.

        Returns:
            object: Requested value for the lookup.
        """
        token = get_token() if token is None else token

        funcs = [extractioner.get_job_id for extractioner in self.extractioners]
        self._run_chunked_threads(funcs=funcs, shared_input=(token,))
        job_ids = [ele.job_id for ele in self.extractioners]
        return job_ids

    def get_bodys(self, token=None):
        """Return bodys.

        Args:
            token (object): Authentication token used for API requests.

        Returns:
            object: Requested value for the lookup.
        """
        funcs = [extractioner.get_body for extractioner in self.extractioners]
        self._run_chunked_threads(funcs=funcs)
        bodys = [ele.body for ele in self.extractioners]

        return bodys

    def save_files(self, output_file_names: List[str], token=None):
        """Save files.

        Args:
            output_file_names (List[str]): Input value for output file names.
            token (object): Authentication token used for API requests.

        Returns:
            object: Computed result of the operation.
        """
        if len(output_file_names) != len(self.extractioners):
            raise ValueError(
                f'Length mismatch, output_file_names [{len(output_file_names)}], '
                f'extractioners [{len(self.extractioners)}]'
            )

        token = get_token() if token is None else token
        funcs = [extractioner.save_output_file for extractioner in self.extractioners]
        funcs_inputs = [(name, token) for name in output_file_names]
        self._run_chunked_threads(funcs=funcs, funcs_inputs=funcs_inputs)
        files_dir = [extractioner.output_file_path for extractioner in self.extractioners]

        return files_dir
