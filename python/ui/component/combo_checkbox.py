# coding=utf-8
import sys

from PyQt5 import QtWidgets


class ComboCheckBox(QtWidgets.QComboBox):
    ALL = r'全部'
    SELF_TRIGGER = 0
    PERSON_TRIGGER = 1

    def __init__(self, items, callback=None):  # items==[str,str...]
        """
        :type items: list
        """
        super(ComboCheckBox, self).__init__()
        self.event_reason = ComboCheckBox.PERSON_TRIGGER
        self.callback = callback
        self.items = items
        self.items.insert(0, ComboCheckBox.ALL)
        self.row_num = len(self.items)
        self.checkbox = []
        self.selected_items = []
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setReadOnly(True)
        self.setMinimumSize(425, 20)
        self.list_widget = QtWidgets.QListWidget()
        for index in range(0, len(self.items)):
            self.add2box_list(index)
        self.setModel(self.list_widget.model())
        self.setView(self.list_widget)
        self.setLineEdit(self.line_edit)
        self.__init_default()

    def __init_default(self):
        self.checkbox[0].setCheckState(2)

    def add2box_list(self, index):
        box = QtWidgets.QCheckBox()
        box.setText(self.items[index])
        box.stateChanged.connect(self.state_change if index != 0 else self.state_change_all)
        self.checkbox.append(box)
        item = QtWidgets.QListWidgetItem(self.list_widget)
        self.list_widget.setItemWidget(item, box)

    def state_change(self, status):
        if self.event_reason == ComboCheckBox.SELF_TRIGGER:
            return
        self.event_reason = ComboCheckBox.SELF_TRIGGER
        self.selected_items.clear()
        for box in self.checkbox:
            if isinstance(box, QtWidgets.QCheckBox):
                if box.isChecked() and box.text() != ComboCheckBox.ALL:
                    self.selected_items.append(box.text())
        if len(self.checkbox) - 1 != len(self.selected_items):
            self.checkbox[0].setCheckState(0)
            self.line_edit.setText(';'.join(self.selected_items))
        else:
            self.checkbox[0].setCheckState(2)
            self.line_edit.setText(ComboCheckBox.ALL)
        self.process()
        self.event_reason = ComboCheckBox.PERSON_TRIGGER

    def state_change_all(self, status):
        if self.event_reason == ComboCheckBox.SELF_TRIGGER:
            return
        self.event_reason = ComboCheckBox.SELF_TRIGGER
        if status == 2:
            for box in self.checkbox:
                if isinstance(box, QtWidgets.QCheckBox):
                    box.setCheckState(2)
                    self.selected_items = [box1.text() for box1 in self.checkbox]
                    self.selected_items = self.selected_items[1:]
                    self.line_edit.setText(ComboCheckBox.ALL)
        else:
            for box in self.checkbox:
                if isinstance(box, QtWidgets.QCheckBox):
                    box.setCheckState(0)
                    self.selected_items.clear()
                    self.line_edit.setText('')
        self.process()
        self.event_reason = ComboCheckBox.PERSON_TRIGGER

    def process(self):
        if self.callback is not None:
            self.callback(self.selected_items)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ComboCheckBox(['a', 'b', 'c'])
    window.show()
    sys.exit(app.exec_())
