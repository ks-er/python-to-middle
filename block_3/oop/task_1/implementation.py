import json
from operator import attrgetter

class Table:

    def __init__(self) -> None:
        self._sort_by = { 'title': 'id', 'reverse': False }
        self._columns = {}
        self._column_positions = []
        self._rows: list[Row] = []
        self._filtered_rows: []
        self.filtered = False

    @property
    def _sorted_rows(self):
        return sorted(
            self._rows,
            key=attrgetter(self._sort_by['title']),
            reverse=self._sort_by['reverse']
        )

    @property
    def _filteded_rows(self):
        if self.filtered:
            return self._filtered_rows
        else:
            return self._sorted_rows

    @property
    def _visible_columns(self):
        return filter(
            lambda name: not self._columns[name].hidden,
            self._column_positions,
        )

    @property
    def rowCount(self):
        if self.filtered:
            return len(self._filtered_rows)
        else:
            return len(self._rows)

    def load_data(self, data):
        json_data = json.loads(data)

        for row in json_data:
            self._rows.append(Row(row))
            for name in row:
                if name not in self._columns:
                    col = Column(name)
                    self._columns[name] = col
                    self._column_positions.append(col.title)
                    column_name_length = len(name)
                    self._columns[name].max_length = column_name_length

                column_max_length = len(
                    str(row[name]) if row[name] is not None else 'None'
                )

                if column_max_length > self._columns[name].max_length:
                    self._columns[name].max_length = column_max_length

    def export(self):
        export_data = self.filterRows(True)
        return json.dumps(export_data)

    def selectRow(self, row_index):
        for row in self._rows:
            if row.selected:
                row.selectRow(False)

        self._rows[row_index].selectRow(True)

    def isSelected(self, row_index) -> None:
        return self._rows[row_index].selected

    def setFilter(self, column_title, filter_fn=None) -> None:
        column = self._columns[column_title]
        if not column.hidden:
            self._columns[column_title].setFilter(filter_fn)
            self.filtered = True
        else:
            raise ValueError('Скрытый столбец нельзя фильтровать')

    def resetFilter(self):
        self.filtered = False
        self._filtered_rows = []
        for title in self._columns:
            self._columns[title].setFilter(None)


    def filterTable(self):
        if self.filtered:
            self._filtered_rows = self.filterRows()
        else:
            self._filtered_rows = []

    def filterRows(self, needNullValues: bool = False):
        export_data = []
        for row in self._sorted_rows:
            obj = {}
            filtered_row = False
            for column_title in self._visible_columns:
                column = self._columns[column_title]
                cell_value = getattr(row, column.title)
                if cell_value is None and needNullValues:
                    cell_value = None
                if column.filter and not column.filter(cell_value):
                    filtered_row = True
                    break
                obj[column_title] = cell_value
            if not filtered_row:
                export_data.append(obj)

        return export_data

    def deleteSelectedRow(self):
        self._rows = list(filter(lambda row: not row.selected, self._rows))

    def changeColumnsPosition(self, title1, title2) -> None:
        col1_index = self._column_positions.index(title1)
        col2_index = self._column_positions.index(title2)
        self._column_positions[col1_index] = title2
        self._column_positions[col2_index] = title1

    def setSort(self, column_title, reverse):
        column = self._columns[column_title]
        if not column.hidden:
            self._sort_by['title'] = column_title
            self._sort_by['reverse'] = reverse
        else:
            raise ValueError('Скрытый столбец нельзя сортировать')

    def setHidden(self, column_title, isNeedHidden) -> None:
        self._columns[column_title].setHidden(isNeedHidden)

    def isVisible(self, column_title):
        return not self._columns[column_title].hidden

    def getColumnPosition(self, column_title):
        return self._column_positions.index(column_title)

    def printTable(self):

        data = self.filterRows()

        # печать таблицы с колонками максимальной длинны строки
        # печать шапки таблицы
        tt = 0
        for column in self._visible_columns:
            max_len = self._columns[column].max_length
            print(f'{column:{max_len + 2}}', end='')
            tt = tt + max_len + 2
        print()
        # печать разделителя шапки
        print(f'{"=" * tt }')
        # печать тела таблицы
        for row in data:
            for col_name in self._visible_columns:
                cell_value = str(row[col_name])

                max_len = self._columns[col_name].max_length
                if cell_value is None:
                    cell_value = 'None'
                print(f'{cell_value:{max_len + 1}}', end=' ')
            print()


class Column:
    def __init__(self, title) -> None:
        self.title = title
        self.filter = None
        self.hidden = False
        self.max_length = 0

    def setHidden(self, is_need_hide):
        self.hidden = is_need_hide

    def setFilter(self, filter_function):
        self.filter = filter_function


class Row:

    def __init__(self, data) -> None:
        self.selected = False
        self.__dict__.update(data)

    def selectRow(self, is_selected):
        self.selected = is_selected
