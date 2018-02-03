import concurrent.futures
import logging
from ..job import Job
from ..exceptions import *

class JobPool:
    """
    The job pool runs jobs as parallell process
    """
    def __init__(self, nb_core: int):
        self.nb_core = nb_core
        self.available = []
        self.enabled = []
        self.completed = []

    def job_run(self, job: Job) -> bool:
        job.run()
        job.postprocessing()
        return True

    def run_enabled(self) -> bool:
        if len(self.enabled) == 0:
            raise JobPoolDependencyTreeException(f"Jobs dependency not resolvable: {self.available!r} completed :{self.completed!r}")
        if(len(self.enabled) == 1):#avoid multiple processes
            self.job_run(self.enabled[0])
        else:
            with concurrent.futures.ProcessPoolExecutor(self.nb_core) as executor:
                executor.map(self.job_run, self.enabled)
        self.enabled_to_completed()
        return True

    def available_to_enabled(self) -> bool:
        for job in list(self.available):# case there is jobs that need a thread safe pool -> one by one
            if not job.is_thread_safe and self.a_issubset_b(job.depends, self.completed):
                self.enabled.append(job)
                self.available.remove(job)
                return True

        for job in list(self.available):
            if self.a_issubset_b(job.depends, self.completed):
                self.enabled.append(job)
                self.available.remove(job)
        return True

    def a_issubset_b(self, a:list, b:list)-> bool:
        for val in a:
            if val not in b:
                return False
        return True

    def enabled_to_completed(self) -> bool:
        for job in list(self.enabled):
            self.completed += job.release()
        self.enabled = []
        return True

    def run_all(self) -> bool:
        while len(self.available):
            logging.debug(self)
            self.available_to_enabled()
            self.run_enabled()
            self.enabled_to_completed()

    def __str__(self) -> str:
        return f"Jobs available: {self.available!r}\nJobs enabled: {self.enabled!r}\nJobs completed: {self.completed!r}"
