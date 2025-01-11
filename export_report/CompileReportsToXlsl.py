from __future__ import annotations
import os
import pandas as pd
import numpy as np

class CompileReportsToXlsl:
    """Class CompileReportsToXlsl

    A class instance may read reports formated as followed:

    <Specifier 1 1> : <Specifier 2 1> : ... : <Specifier N 1> -> <Value 1>
    <Specifier 1 2> : <Specifier 2 2> : ... : <Specifier N 2> -> <Value 2>
    ...
    <Specifier 1 M> : <Specifier 2 M> : ... : <Specifier N M> -> <Value M>

    Any of specifiers may be used for a sheet name, a row name or a column name.

    By default '<Specifier 1 x> : <Specifier 2 x> : ...' stands for a row name, and <Specifier N x> stands for a column name, while a filename is to be used for a sheet name.

    If no dfdict passed CompileReportsToXlsl is to save data frames to internal _dfdict in order to write it to xlsl file further.
    One may both save externally compiled data frames and data frames read earlier to internal _dfdict. 
    To write internal _dfdict to xlsl file do not pass the second parameter dfdict to the method writeDataFramesToXlsx.
    """

    _default_row_and_col_names_mask = ((0, -1), (-1, None))

    def __init__(
            self, 
            row_and_col_names_mask = None, 
            sheetname_mask = None,
            row_name_specifiers_separator = ' : ',
            col_name_specifiers_separator = ' : ',
            sheetname_specifiers_separator = ' : '
        ):
        self._dfdict = None
        self._row_and_col_names_mask = row_and_col_names_mask if CompileReportsToXlsl.__is_correct_row_and_col_name_mask(row_and_col_names_mask) else CompileReportsToXlsl._default_row_and_col_names_mask
        self._sheetname_mask = sheetname_mask if CompileReportsToXlsl.__is_correct_specifiers_to_name_mask(sheetname_mask) else None
        self._row_name_specifiers_separator = row_name_specifiers_separator
        self._col_name_specifiers_separator = col_name_specifiers_separator
        self._sheetname_specifiers_separator = sheetname_specifiers_separator

    def __writeValueToDataFrame(self, line: str, dfdict: dict, default_sheetname: str):
        sheet_name, row_name, col_name, value = self.__parse_record_line(line, default_sheetname)

        # print('\n-------------')
        # print('row_name, sheet_name, col_name, value')
        # print(row_name, sheet_name, col_name, value)

        df = dfdict.setdefault(sheet_name, pd.DataFrame(dtype=pd.StringDtype()))
        # V1: df may be changed in __set_record_value_to_dataframe_or_append_to_a_copy
        # dfdict[sheet_name] = CompileReportsToXlsl.__set_record_value_to_dataframe_or_append_to_a_copy(df, row_name, col_name, value)

        # V2
        # __append_record_to_dataframe will modify an existing data frame
        CompileReportsToXlsl.__append_record_to_dataframe(df, row_name, col_name, value)

    def readReport(self, path: str, dfdict: dict = None) -> dict:
        save_to_self = False
        if dfdict is None:
            dfdict = {}
            save_to_self = True

        default_sheetname = self.__get_sheetname_from_path(path)

        with open(path, 'r') as f:

            lines = f.readlines()

            for s in lines:
                s = s.strip()
                if len(s) < 1:
                    continue
                self.__writeValueToDataFrame(s, dfdict, default_sheetname)

        if save_to_self:
            self._dfdict = dfdict

        return dfdict
    
    def readReports(self, path_list: list, dfdict: dict = None) -> dict:
        save_to_self = False
        if dfdict is None:
            dfdict = {}
            save_to_self = True

        for path in path_list:
            self.readReport(path, dfdict)

        if save_to_self:
            self._dfdict = dfdict

        return dfdict
    
    def clear(self):
        self._dfdict = None

    def writeDataFramesToXlsx(self, path: str, dfdict:dict = None):
        if dfdict is None:
            dfdict = self._dfdict
        if dfdict is None:
            print('WARNING! No data frame dictionary to write found.')
            print('Read a report or pass a data frame dictionary.')

            return

        with pd.ExcelWriter(path) as writer:
            for name, df in dfdict.items():
                # print(name, len(name))
                df.to_excel(writer, sheet_name=name)

    def __get_sheetname_from_path(self, path: str) -> str:
        _, tail = os.path.split(path)

        return tail
    
    def __parse_record_line(self, line: str, default_sheetname: str) -> tuple:
        specifiers_str, value = tuple(map(lambda s: s.strip(), line.split('->')))
        specifiers = list(map(lambda s: s.strip(), specifiers_str.split(':')))

        sheet_name = self.__get_record_sheetname(specifiers, default_sheetname)
        row_name, col_name = self.__get_record_row_and_column_name(specifiers)

        return sheet_name, row_name, col_name, value

    def __get_record_sheetname(self, specifiers: list, default_sheetname: str) -> str:
        return self.__get_masked_name_from_list(specifiers, self._sheetname_mask, self._sheetname_specifiers_separator) if self._sheetname_mask is not None else default_sheetname
    
    def __get_record_row_and_column_name(self, specifiers: list) -> tuple:
        return (
            self.__get_masked_name_from_list(specifiers, self._row_and_col_names_mask[0], self._row_name_specifiers_separator),
            self.__get_masked_name_from_list(specifiers, self._row_and_col_names_mask[1], self._col_name_specifiers_separator)
        )
    
    @staticmethod
    def __set_record_value_to_dataframe_or_append_to_a_copy(source_df, row_name: str, col_name: str, value: str):

        index = source_df.index
        columns = source_df.columns

        if not row_name in index:
            index = index.insert(index.size, row_name)

        if not col_name in columns:
            columns = columns.insert(columns.size, col_name)

        # print('index', index, type(index), index.array, bool(arrayType in index))
        # print('columns', columns, type(columns), columns.array)

        df = pd.DataFrame(source_df, index=index, columns=columns)

        df.at[row_name, col_name] = value

        return df
    
    @staticmethod
    def __append_record_to_dataframe(source_df, row_name: str, col_name: str, value: str):
        if source_df.empty:
            source_df.insert(0, col_name, [value])
            source_df.set_index(pd.Series([row_name]), inplace=True)

            return source_df

        source_index = source_df.index
        source_columns = source_df.columns

        index_size = source_index.size

        if not row_name in source_index:
            index = source_index.copy().insert(index_size, row_name)
            index_size = index.size
            source_df.reindex(index)

        if not col_name in source_columns:
            source_df.insert(source_columns.size, col_name, np.full(index_size, ''))

        # print('source_index', source_index, source_index.size)
        # print('index', index, index_size)
        # print('source_df.index', source_df.index, source_df.index.size)
        # print('source_df.columns', source_df.columns)
        source_df.at[row_name, col_name] = value

        return source_df
    
    # TODO: Add warnings
    @staticmethod
    def __is_correct_specifiers_to_name_mask(mask: list) -> bool:
        if (not isinstance(mask, list) and not isinstance(mask, tuple)) or len(mask) < 1:
            return False
        
        return all(list(map(lambda mask_item: isinstance(mask_item, int) or mask_item is None, mask)))
    
    @staticmethod
    def __is_correct_row_and_col_name_mask(mask: list) -> bool:
        if (not isinstance(mask, list) and not isinstance(mask, tuple)) or len(mask) < 2:
            return False
        
        return all(list(map(lambda inner_mask: CompileReportsToXlsl.__is_correct_specifiers_to_name_mask(inner_mask), mask)))

    @staticmethod
    def __get_masked_name_from_list(specifiers: list, mask: list | tuple, join_separator: str = '') -> str:
        # One int in a mask means an index of a single specifier
        if len(mask) == 1:
            mask = list(mask)
            mask.push(mask[0] + 1)

        mask_defaults = [0, 0, 1]
        complete_mask = map(lambda a_enum:  mask[int(a_enum[0])] if int(a_enum[0]) < len(mask) else int(a_enum[1]), enumerate(mask_defaults))
        start, end, step = complete_mask

        return join_separator.join(specifiers[start:end:step])
