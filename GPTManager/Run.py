
from dataclasses import dataclass, field
from typing import Any, Optional
from openai import OpenAI

@dataclass
class Tool:
    type: str
    function: object = None
    
@dataclass
class RunStep:
    """
    A class representing a thread run step.
    
    Attributes:
        id (str): The run step id.
        object (str): The object type.
        created_at (int): The time the run step was created.
        run_id (str): The run id.
        assistant_id (str): The assistant id.
        thread_id (str): The thread id.
        type (str): The type of run step.
        status (str): The status of the run step.
        cancelled_at (int): The time the run step was cancelled.
        completed_at (int): The time the run step was completed.
        expired_at (int): The time the run step expired.
        failed_at (int): The time the run step failed.
        last_error (str): The last error message.
        step_details (dict): The details of the run step.
    """
    id: str
    object: str = "thread.run.step"
    created_at: int
    run_id: str
    assistant_id: str
    thread_id: str
    type: str
    status: str
    cancelled_at: Optional[int]
    completed_at: Optional[int]
    expired_at: Optional[int]
    failed_at: Optional[int]
    last_error: Optional[str]
    step_details: dict

    def retrieve_run_step(self):
        client = OpenAI()

        try:
            run_step = client.beta.threads.runs.steps.retrieve(
                thread_id=self.thread_id,
                run_id=self.run_id,
                step_id=self.id
            )
            
            self.object = run_step.object
            self.created_at = run_step.created_at
            self.run_id = run_step.run_id
            self.assistant_id = run_step.assistant_id
            self.thread_id = run_step.thread_id
            self.type = run_step.type
            self.status = run_step.status
            self.cancelled_at = run_step.cancelled_at
            self.completed_at = run_step.completed_at
            self.expired_at = run_step.expired_at
            self.failed_at = run_step.failed_at
            self.last_error = run_step.last_error
            self.step_details = run_step.step_details

        except Exception as e:
            raise ValueError("Failed to retrive run step.") from e



@dataclass
class Run:
    """
    A class representing a thread run.

    Attributes:
        id (str): The run id.
        object (str): The object type.
        created_at (int): The time the run was created.
        assistant_id (str): The assistant id.
        thread_id (str): The thread id.
        status (str): The status of the run.
        started_at (int): The time the run was started.
        expires_at (int): The time the run expires.
        cancelled_at (int): The time the run was cancelled.
        failed_at (int): The time the run failed.
        completed_at (int): The time the run completed.
        last_error (str): The last error message.
        model (str): The model used for the run.
        instructions (str): The instructions for the run.
        tools (list[Tool]): The tools used for the run.
        file_ids (list[Any]): The file ids used for the run.
        metadata (dict[str, Any]): The metadata for the run.
    """  
    __id: str
    __object: str = "thread.run"
    __created_at: int
    __assistant_id: str
    __thread_id: str
    __status: str
    __started_at: int
    __expires_at: Optional[int]
    __cancelled_at: Optional[int]
    __failed_at: Optional[int]
    __completed_at: Optional[int]
    __last_error: Optional[str]
    __model: str = "gpt-4-1106-preview"
    __instructions: Optional[str]
    __tools: list[Tool] = [{"type": "retrieval"}, {"type": "code_interpreter"}]
    __file_ids: list[Any] = field(default_factory=list)
    __metadata: dict[str, Any] = field(default_factory=dict)

    def __init__(self, thread_id: str|None = None, assistant_id: str|None = None, run_id: str|None = None) -> None:
        """
        Creates a new thread run or retrieves an existing one.

        Parameters:
            thread_id (str): The thread id.
            assistant_id (str): The assistant id.
            run_id (str): The run id.

        Returns:
            None

        Raises:
            ValueError: If the thread_id or assistant_id is not set.
        """
        if run_id is not None and thread_id is not None:
            self.__id = run_id
            self.__thread_id = thread_id
            self.retrieve_run()
        elif thread_id is not None and assistant_id is not None:
            self.__assistant_id = assistant_id
            self.__thread_id = thread_id
            self.create_run()
        

    def create_run(self) -> None:
        """
        Creates a new thread run.

        Returns:
            None

        Raises:
            ValueError: If the thread_id or assistant_id is not set.
        """
        client = OpenAI()

        try:
            run = client.beta.threads.runs.create(
                thread_id=self.__thread_id,
                assistant_id=self.__assistant_id,
            )

            self.__id = run.id
            self.__object = run.object
            self.__created_at = run.created_at
            self.__status = run.status
            self.__started_at = run.started_at
            self.__expires_at = run.expires_at
            self.__cancelled_at = run.cancelled_at
            self.__failed_at = run.failed_at
            self.__completed_at = run.completed_at
            self.__last_error = run.last_error
            self.__model = run.model
            self.__instructions = run.instructions
            self.__tools = run.tools
            self.__file_ids = run.file_ids
            self.__metadata = run.metadata
            
        except Exception as e:
            raise ValueError("Failed to create run") from e
        
    def retrieve_run(self):
        """
        Retrieves a thread run.

        Returns:
            None

        Raises:
            ValueError: If the thread_id or assistant_id is not set.
        """
        client = OpenAI()

        try:
            run = client.beta.threads.runs.retrieve(
                thread_id=self.__thread_id,
                run_id=self.__id,
            )

            self.__object = run.object
            self.__created_at = run.created_at
            self.__status = run.status
            self.__started_at = run.started_at
            self.__expires_at = run.expires_at
            self.__cancelled_at = run.cancelled_at
            self.__failed_at = run.failed_at
            self.__completed_at = run.completed_at
            self.__last_error = run.last_error
            self.__model = run.model
            self.__instructions = run.instructions
            self.__tools = run.tools
            self.__file_ids = run.file_ids
            self.__metadata = run.metadata

        except Exception as e:
            raise ValueError("Failed to retrieve run") from e

    def modify_run(self, metadata) -> None:
        """
        Modifies a thread run.

        Parameters:
            **kwargs: The attributes to modify.

        Returns:
            None

        Raises:
            ValueError: If the thread_id or assistant_id is not set.
        """
        client = OpenAI()

        try:
            run = client.beta.threads.runs.update(
                thread_id=self.__thread_id,
                run_id=self.__id,
                metadata=metadata
            )

            self.__metadata = run.metadata

        except Exception as e:
            raise ValueError("Failed to modify run") from e
        
    def list_runs(self) -> list['Run']:
        """
        Lists all thread runs.
        Returns:
            list[RunObject]: A list of RunObject instances representing each run.
        Raises:
            ValueError: If the thread_id or assistant_id is not set, or if the API call fails.
        """
        client = OpenAI()

        try:
            runs_data = client.beta.threads.runs.list(
                thread_id=self.__thread_id
            )
            runs = [Run(**run_data) for run_data in runs_data]  # Convert each dict to a RunObject
            return runs

        except Exception as e:
            raise ValueError("Failed to list runs") from e
        
    def submit_tool_outputs(self, tool_outputs: list[dict]) -> None:
        """
        Submits tool outputs for a thread run.

        Returns:
            None

        Raises:
            ValueError: If the thread_id or assistant_id is not set.
        """
        client = OpenAI()

        try:
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=self.__thread_id,
                run_id=self.__id,
                tool_outputs=tool_outputs
            )

            self.__status = run.status
            self.__started_at = run.started_at
            self.__expires_at = run.expires_at
            self.__cancelled_at = run.cancelled_at
            self.__failed_at = run.failed_at
            self.__completed_at = run.completed_at
            self.__last_error = run.last_error
            self.__model = run.model
            self.__instructions = run.instructions
            self.__tools = run.tools
            self.__file_ids = run.file_ids
            self.__metadata = run.metadata

        except Exception as e:
            raise ValueError("Failed to submit tool outputs") from e
        
    def cancel_run(self) -> None:
        """
        Cancels a thread run.

        Returns:
            None

        Raises:
            ValueError: If the thread_id or assistant_id is not set.
        """
        client = OpenAI()

        try:
            run = client.beta.threads.runs.cancel(
                thread_id=self.__thread_id,
                run_id=self.__id,
            )

            self.__status = run.status
            self.__started_at = run.started_at
            self.__expires_at = run.expires_at
            self.__cancelled_at = run.cancelled_at
            self.__failed_at = run.failed_at
            self.__completed_at = run.completed_at
            self.__last_error = run.last_error
            self.__model = run.model
            self.__instructions = run.instructions
            self.__tools = run.tools
            self.__file_ids = run.file_ids
            self.__metadata = run.metadata

        except Exception as e:
            raise ValueError("Failed to cancel run") from e
        
    def create_thread_and_run(self, assistant_id: str, thread: dict):
        """
        Creates a thread and run.

        Returns:
            None

        Raises:
            ValueError: If the thread_id or assistant_id is not set.
        """
        client = OpenAI()

        try:
            run = client.beta.threads.create(
                assistant_id=assistant_id,
                **thread
            )
            run = client.beta.threads.create_and_run(
                assistant_id=assistant_id,
                thread=thread)

            self.__id = run.id
            self.__object = run.object
            self.__created_at = run.created_at
            self.__status = run.status
            self.__started_at = run.started_at
            self.__expires_at = run.expires_at
            self.__cancelled_at = run.cancelled_at
            self.__failed_at = run.failed_at
            self.__completed_at = run.completed_at
            self.__last_error = run.last_error
            self.__model = run.model
            self.__instructions = run.instructions
            self.__tools = run.tools
            self.__file_ids = run.file_ids
            self.__metadata = run.metadata

        except Exception as e:
            raise ValueError("Failed to create thread and run") from e
        
    def list_run_steps(self):
        client = OpenAI()

        try:
            run_steps = client.beta.threads.runs.steps.list(
                thread_id=self.__thread_id,
                run_id=self.__id
            )

            return [RunStep(**run_step) for run_step in run_steps]
        except Exception as e:
            raise ValueError("Failed to list run steps") from e
        

