from abc import ABC, abstractmethod

class NotesData(ABC):

    @abstractmethod
    def notes_data_output(self):
        pass
