from abc import ABC, abstractmethod

class ContactData(ABC):

    @abstractmethod
    def contact_data_output(self):
        pass
