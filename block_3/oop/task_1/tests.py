import json
from unittest import TestCase

from block_3.oop.task_1.implementation import Table


class Test(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.table = Table()
        with open('data/data.json', 'r') as f:
            self.table.load_data(f.read())

    def test_plain(self):
        result = self.table.export()
        with open('data/test_plain.json', 'r') as f:
            self.assertEqual(json.loads(result), json.loads(f.read()))
    def test_hide_column(self):
        self.table.setHidden('id', True)
        self.table.setHidden('group_id', True)

        self.assertEqual(self.table.isVisible('id'), False)
        self.assertEqual(self.table.isVisible('group_id'), False)
        self.assertEqual(self.table.isVisible('fifa_code'), True)

    def test_select_delete_row(self):

        self.table.selectRow(0)
        self.table.selectRow(1)

        self.assertEqual(self.table.isSelected(0), False)
        self.assertEqual(self.table.isSelected(1), True)

        self.assertEqual(self.table.rowCount, 24)
        self.table.deleteSelectedRow()
        self.assertEqual(self.table.rowCount, 23)

    def test_change_columns_position(self):
        self.table.changeColumnsPosition('alternate_name', 'id')
        self.assertEqual(self.table.getColumnPosition('id'), 0)

    def test_filter_rows(self):
        self.assertEqual(self.table.rowCount, 24)
        self.table.setFilter('id', lambda value: value > 15)
        self.table.filterTable()
        self.assertEqual(self.table.rowCount, 9)

        self.table.resetFilter()
        self.assertEqual(self.table.rowCount, 24)

        self.table.setHidden('group_id', True)

        with self.assertRaises(ValueError):
            self.table.setFilter('group_id', lambda value: value == 3)

    def test_sorted_rows(self):
        self.table.printTable()
        print()
        self.table.setSort('id', True)
        self.table.printTable()
        print()
        self.table.setSort('country', True)
        self.table.printTable()
        print()

        self.table.setSort('fifa_code', False)
        self.table.printTable()
        print()

        self.table.setHidden('fifa_code', True)

        with self.assertRaises(ValueError):
            self.table.setSort('fifa_code', False)

        self.table.printTable()

    def test_sorted_filtered_hidden_rows(self):

        self.table.setSort('country', False)
        self.table.setHidden('alternate_name', True)
        self.table.setHidden('group_id', True)
        self.table.setHidden('group_letter', True)
        self.table.changeColumnsPosition('country', 'id')
        self.table.setFilter('country', lambda value: value in ('Italy', 'Japan', 'Thailand', 'France'))

        self.table.printTable()
