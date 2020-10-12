from texttable import Texttable

from pySprida.data.dataContainer import DataContainer


class ConsolePrinter:

    @staticmethod
    def printTeachers(container: DataContainer):
        table = Texttable()
        table.header(["ID", "Name", ">=3 Subjects"])
        for i, teacher in enumerate(container.teachers):
            important_subjects = [sub.name for sub in teacher.get_subject_preferences(3)]
            table.add_row([i, teacher.name, str(important_subjects)])
        print(table.draw())

    @staticmethod
    def printGroups(container: DataContainer):
        table = Texttable()
        table.header(["ID", "Type", "Groupname"])
        for i, group in enumerate(container.groups):
            table.add_row([i, group.group_type.name, group.name])
        print(table.draw())
