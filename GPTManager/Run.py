
from dataclasses import dataclass, field
from typing import Any, Optional

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from GPTManager.Client import Client

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
    object: str
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
    file_ids: list[Any]
    metadata: dict[str, Any]

    def __init__(self, **kwargs) -> None:
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

        self.id = kwargs.get("id", None)
        self.object = kwargs.get("object", None)
        self.created_at = kwargs.get("created_at", None)
        self.assistant_id = kwargs.get("assistant_id", None)
        self.thread_id = kwargs.get("thread_id", None)
        self.status = kwargs.get("status", None)
        self.started_at = kwargs.get("started_at", None)
        self.expires_at = kwargs.get("expires_at", None)
        self.cancelled_at = kwargs.get("cancelled_at", None)
        self.failed_at = kwargs.get("failed_at", None)
        self.completed_at = kwargs.get("completed_at", None)
        self.last_error = kwargs.get("last_error", None)
        self.model = kwargs.get("model", None)
        self.instructions = kwargs.get("instructions", None)
        self.tools = kwargs.get("tools", None)
        self.file_ids = kwargs.get("file_ids", None)
        self.metadata = kwargs.get("metadata", None)

        if (
            self.id != None and
            self.object != None and
            self.created_at != None and
            self.assistant_id != None and
            self.thread_id != None and
            self.status != None and
            self.started_at != None and
            self.completed_at != None and
            self.model != None and
            self.tools != None and
            self.file_ids != None and
            self.metadata != None
        ): return
           
        if self.id is not None and self.thread_id is not None:
            self.retrieve_run()
        elif self.thread_id is not None and self.assistant_id is not None:
            self.create_run()
        

    def create_run(self) -> None:
        """
        Creates a new thread run.

        Returns:
            None

        Raises:
            ValueError: If the thread_id or assistant_id is not set.
        """
        client = Client.get_instance()

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
            raise ValueError("Failed to create run") from e
        

    def retrieve_run(self):
        """
        Retrieves a thread run.

        Returns:
            None

        Raises:
            ValueError: If the thread_id or assistant_id is not set.
        """
        client = Client.get_instance()

        try:
            run = client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=self.id,
            )

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
        client = Client.get_instance()

        try:
            run = client.beta.threads.runs.update(
                thread_id=self.thread_id,
                run_id=self.id,
                metadata=metadata
            )

            self.metadata = run.metadata

        except Exception as e:
            raise ValueError("Failed to modify run") from e
        
      
    def submit_tool_outputs(self, tool_outputs: list[dict]) -> None:
        """
        Submits tool outputs for a thread run.

        Returns:
            None

        Raises:
            ValueError: If the thread_id or assistant_id is not set.
        """
        client = Client.get_instance()

        try:
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=self.thread_id,
                run_id=self.id,
                tool_outputs=tool_outputs
            )

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
            raise ValueError("Failed to submit tool outputs") from e


    def cancel_run(self) -> None:
        """
        Cancels a thread run.

        Returns:
            None

        Raises:
            ValueError: If the thread_id or assistant_id is not set.
        """
        client = Client.get_instance()

        try:
            run = client.beta.threads.runs.cancel(
                thread_id=self.thread_id,
                run_id=self.id,
            )

            self.object = run.object
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
            raise ValueError("Failed to cancel run") from e

       
    def create_thread_and_run(self, messages: list[dict]):
        """
        Creates a thread and run.

        Returns:
            None

        Raises:
            ValueError: If the thread_id or assistant_id is not set.
        """
        client = Client.get_instance()

        try:
            run = client.beta.threads.create_and_run(
                assistant_id=self.assistant_id,
                thread={
                    "messages": messages
                }
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
            raise ValueError("Failed to create thread and run") from e


    def retrieve_run_step(self, step_id: str) -> RunStep:
        client = Client.get_instance()

        try:
            run_step = client.beta.threads.runs.steps.retrieve(
                thread_id=self.thread_id,
                run_id=self.id,
                step_id=step_id
            )
            return RunStep(
                id = run_step.id,
                object = run_step.object,
                created_at = run_step.created_at,
                run_id = run_step.run_id,
                assistant_id = run_step.assistant_id,
                thread_id = run_step.thread_id,
                type = run_step.type,
                status = run_step.status,
                cancelled_at = run_step.cancelled_at,
                completed_at = run_step.completed_at,
                expired_at = run_step.expired_at,
                failed_at = run_step.failed_at,
                last_error = run_step.last_error,
                step_details = run_step.step_details
            )

        except Exception as e:
            raise ValueError("Failed to retrive run step.") from e


    def list_run_steps(self):
        client = Client.get_instance()

        try:
            run_steps = client.beta.threads.runs.steps.list(
                thread_id=self.thread_id,
                run_id=self.id
            )
        
            return [
                RunStep(
                    id = run_step.id,
                    object = run_step.object,
                    created_at = run_step.created_at,
                    run_id = run_step.run_id,
                    assistant_id = run_step.assistant_id,
                    thread_id = run_step.thread_id,
                    type = run_step.type,
                    status = run_step.status,
                    cancelled_at = run_step.cancelled_at,
                    completed_at = run_step.completed_at,
                    expired_at = run_step.expired_at,
                    failed_at = run_step.failed_at,
                    last_error = run_step.last_error,
                    step_details = run_step.step_details
                ) 
                for run_step 
                in run_steps.data
            ]
    
        except Exception as e:
            raise ValueError("Failed to list run steps") from e
        

