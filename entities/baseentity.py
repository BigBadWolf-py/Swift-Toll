from dao.basedao import BaseDAO


class BaseEntity:
    def __init__(self):
        pass

    def get_item(self):
        return self.__dict__

    def insert(self, uuid=""):
        id = ""
        if uuid:
            id = BaseDAO.insert(self.get_item(), self.get_table(), uuid=uuid)
        else:
            id = BaseDAO.insert(self.get_item(), self.get_table())
            if not id:
                raise Exception('Insertion to DB failed')
        return id

    def update(self, keys):
        BaseDAO.update(self.get_item(), self.get_table(), keys)

