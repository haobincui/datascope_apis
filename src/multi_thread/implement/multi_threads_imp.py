from abc import ABC
import multiprocessing
from typing import Callable, List, Optional, Tuple

from src.multi_thread.multi_threads import MultiThreads


class MultiThreadsImp(ABC):
    """Represents multi threads imp."""

    def _resolve_nums_of_threads(
        self,
        total_tasks: int,
        nums_of_threads: Optional[int] = None,
    ) -> int:
        """Resolve thread count from explicit input or local CPU core count.

        Args:
            total_tasks (int): Total number of runnable tasks.
            nums_of_threads (Optional[int]): Preferred upper bound for threads.

        Returns:
            int: Effective thread count bounded by total tasks.
        """
        if total_tasks <= 0:
            return 0

        if nums_of_threads is not None:
            if nums_of_threads <= 0:
                raise ValueError(f'nums_of_threads must be positive, got [{nums_of_threads}]')
            return min(total_tasks, nums_of_threads)

        cpu_cores = multiprocessing.cpu_count()
        return min(total_tasks, cpu_cores)

    def _iter_chunk_indices(self, total_size: int):
        """Yield [start, end) ranges for chunked execution.

        Args:
            total_size (int): Total number of tasks to run.

        Returns:
            generator: Start/end indices for each chunk.
        """
        if total_size <= 0:
            return

        chunk_size = self.nums_of_threads if self.nums_of_threads > 0 else 1
        for start in range(0, total_size, chunk_size):
            end = min(start + chunk_size, total_size)
            yield start, end

    def _run_chunked_threads(
        self,
        funcs: List[Callable],
        shared_input: Optional[Tuple] = None,
        funcs_inputs: Optional[List[Tuple]] = None,
    ) -> None:
        """Execute callables in chunked thread batches.

        Args:
            funcs (List[Callable]): Callables to execute.
            shared_input (Optional[Tuple]): Shared input tuple for every callable.
            funcs_inputs (Optional[List[Tuple]]): Per-callable input tuples.

        Returns:
            None: No value is returned.
        """
        total_tasks = len(funcs)
        if total_tasks == 0:
            return

        if funcs_inputs is not None and len(funcs_inputs) != total_tasks:
            raise ValueError(
                f'Input size mismatch, funcs [{total_tasks}], inputs [{len(funcs_inputs)}]'
            )

        shared_input = shared_input if shared_input is not None else tuple()
        for start, end in self._iter_chunk_indices(total_tasks):
            cur_funcs = funcs[start:end]
            cur_threads = MultiThreads(funcs=cur_funcs, nums_of_thread=len(cur_funcs))
            if funcs_inputs is not None:
                cur_threads.allocate_input_to_threads(funcs_inputs[start:end])
            else:
                cur_threads.allocate_input_to_threads(shared_input)
            cur_threads.start_calc()
