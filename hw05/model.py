from markupsafe import escape
from pydantic import BaseModel


class Tasks(BaseModel):
    """
    Tasks model
    """
    task_text: str

    def __setattr__(self, key, value):
        if key == 'task_text':
            object.__setattr__(self, key, escape(value))
