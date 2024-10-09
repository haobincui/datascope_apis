from typing import List

from src.connection.client import _get_token
from src.connection.features.extraction.on_demand_extractioner.on_demand_extractioner import OnDemandExtractioner
from src.multi_thread.implement.multi_threads_imp import MultiThreadsImp
from src.multi_thread.multi_threads import MultiThreads


class ExtractionImp(MultiThreadsImp):

    def __init__(self, extractioners: List[OnDemandExtractioner]):
        self.extractioners = extractioners
        self.nums_of_threads = len(extractioners)

    def get_locations(self, token=None):
        token = token if token else _get_token()

        funcs = [extractioner.get_location for extractioner in self.extractioners]
        threads = MultiThreads(funcs=funcs, nums_of_thread=self.nums_of_threads)
        threads.allocate_input_to_threads((token,))
        threads.start_calc()
        locations = [ele.location for ele in self.extractioners]

        return locations

    def get_job_ids(self, token=None):
        token = token if token else _get_token()

        funcs = [extractioner.get_job_id for extractioner in self.extractioners]
        threads = MultiThreads(funcs=funcs, nums_of_thread=self.nums_of_threads)
        threads.allocate_input_to_threads((token,))
        threads.start_calc()
        job_ids = [ele.job_id for ele in self.extractioners]
        return job_ids

    def get_bodys(self, token=None):
        token = token if token else _get_token()

        funcs = [extractioner.get_body for extractioner in self.extractioners]
        threads = MultiThreads(funcs=funcs, nums_of_thread=self.nums_of_threads)
        threads.allocate_input_to_threads((token,))
        threads.start_calc()
        bodys = [ele.body for ele in self.extractioners]

        return bodys

    def save_files(self, output_file_names: List[str], token=None):
        token = token if token else _get_token()
        funcs = [extractioner.save_output_file for extractioner in self.extractioners]
        threads = MultiThreads(funcs=funcs, nums_of_thread=self.nums_of_threads)
        funcs_inputs = [(name, token) for name in output_file_names]
        threads.allocate_input_to_threads(funcs_inputs)
        threads.start_calc()
        files_dir = [extractioner.output_file_path for extractioner in self.extractioners]

        return files_dir



