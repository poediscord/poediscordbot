import abc
import logging
import typing
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

class Handler(abc.ABC):
    """Class that handles the execution of a Job"""

    def __init__(self, core, job):
        super().__init__()

        self.log = logging.getLogger(f"{type(self).__qualname__}.{self.id}")
        self.core = core
        self.job = job

    async def execute(self):
        self.started = datetime.utcnow()
        try:
            self.log.debug(f"Starting {self.job.id}")
            while isinstance(self.job.stage, str): #TODO: make cancelable
                self.log.debug(f"Running {self.job.id} stage: {self.job.stage}")
                self.stage = await getattr(self, f"stage_{self.job.stage}")()
                yield self.stage
        except Exception as e:
            self.log.error(f"Error handling {self.job.id}: {e}")
            raise e
        finally:
            self.ended = datetime.utcnow()
            self.log.debug(f"Completed {self.job.id} in {self.ended-self.started} seconds")

    @abc.abstractmethod
    async def stage_begin(self):
        pass

@dataclass
class StageResult:
    next_stage: typing.Optional[typing.Callable] = None
    delay_until: typing.Optional[datetime] = None
    complete_job: typing.Optional[bool] = False
    on_event: typing.Optional[DiscordEvent] = None

    @classmethod
    def next(cls, func):
        return StageResult(next_stage=func)

    @classmethod
    def delay(cls, func, until):
        return StageResult(delay_until=until)

    @classmethod
    def retry(cls, func, event):
        return StageResult(next_stage=func, on_event=event)

    @classmethod
    def complete(cls):
        return StageResult(complete_job=True)