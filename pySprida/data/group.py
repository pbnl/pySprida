from pySprida.data.groupType import GroupType


class Group:

    def __init__(self, container, group_type, name):
        self.container = container
        self.group_type: GroupType = group_type
        self.name: str = name