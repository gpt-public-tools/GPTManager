
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from openai import OpenAI

@dataclass
class Tool:
    type: str
    function: object = None
    
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
        metadata (Dict[str, Any]): The metadata for the run.
    """
    id: str
    object: str
    created_at: int
    assistant_id: str
    thread_id: str
    status: str
    started_at: int
    expires_at: Optional[int]
    cancelled_at: Optional[int]
    failed_at: Optional[int]
    completed_at: Optional[int]
    last_error: Optional[str]
    model: str
    instructions: Optional[str]
    tools: list[Tool]
    file_ids: list[Any] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, thread_id: str|None = None, assistant_id: str|None = None, run_id: str|None = None) -> None:
        """
        Creates a new thread run or retrieves an existing one.
        Args:
            thread_id (str): The thread id.
            assistant_id (str): The assistant id.
            run_id (str): The run id.
        Returns:
            None
        Raises:
            ValueError: If the thread_id or assistant_id is not set.
        """
        if run_id is not None and thread_id is not None:
            self.id = run_id
            self.thread_id = thread_id
            self.retrieve_run()
        elif thread_id is not None and assistant_id is not None:
            self.assistant_id = assistant_id
            self.thread_id = thread_id
            self.create_run()
        
        pass

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
                thread_id=self.thread_id,
                assistant_id=self.assistant_id,
            )

            self.id = run.id
            self.object = run.object
            self.created_at = run.created_at
            self.status = run.status
            self.started_at = run.started_at
            self.expires_at = run.expires_at
            self.cancelled_at = run.cancelled_at
            self.failed_at = run.failed_at
            self.completed_at = run.completed_at
            self.last_error = run.last_error
            self.model = run.model
            self.instructions = run.instructions
            self.tools = run.tools
            self.file_ids = run.file_ids
            self.metadata = run.metadata
            
        except Exception as e:
            raise ValueError(e)
        
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
                thread_id=self.thread_id,
                run_id=self.id,
            )

            self.id = run.id
            self.object = run.object
            self.created_at = run.created_at
            self.status = run.status
            self.started_at = run.started_at
            self.expires_at = run.expires_at
            self.cancelled_at = run.cancelled_at
            self.failed_at = run.failed_at
            self.completed_at = run.completed_at
            self.last_error = run.last_error
            self.model = run.model
            self.instructions = run.instructions
            self.tools = run.tools
            self.file_ids = run.file_ids
            self.metadata = run.metadata

        except Exception as e:
            raise ValueError(e)

    def modify_run(self, metadata) -> None:
        """
        Modifies a thread run.
        Args:
            **kwargs: The attributes to modify.
        Returns:
            None
        Raises:
            ValueError: If the thread_id or assistant_id is not set.
        """
        client = OpenAI()

        try:
            run = client.beta.threads.runs.update(
                thread_id=self.thread_id,
                run_id=self.id,
                metadata=metadata
            )

            self.id = run.id
            self.object = run.object
            self.created_at = run.created_at
            self.status = run.status
            self.started_at = run.started_at
            self.expires_at = run.expires_at
            self.cancelled_at = run.cancelled_at
            self.failed_at = run.failed_at
            self.completed_at = run.completed_at
            self.last_error = run.last_error
            self.model = run.model
            self.instructions = run.instructions
            self.tools = run.tools
            self.file_ids = run.file_ids
            self.metadata = run.metadata

        except Exception as e:
            raise ValueError(e)
        
    def list_runs(self) -> list[Run]:
        """
        Lists all thread runs.
        Returns:
            None
        Raises:
            ValueError: If the thread_id or assistant_id is not set.
        """
        client = OpenAI()

        try:
            runs = client.beta.threads.runs.list(
                thread_id=self.thread_id
            )

            return runs

        except Exception as e:
            raise ValueError(e)