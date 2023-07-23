from __future__ import annotations

WHERE_CLAUSE = 'WHERE {conditions}'
CREATE_TABLE_BASE_STMT = (
    'CREATE TABLE [IF NOT EXISTS] {table_name} ({column_definitions});'
)
INSERT_BASE_STMT = 'INSERT INTO {table_name} ({columns}) VALUES ({values});'
SELECT_BASE_STMT = 'SELECT {columns} FROM {table_name}'
DELETE_BASE_STMT = 'DELETE FROM {table_name}'
UPDATE_BASE_STMT = 'UPDATE {table_name} SET {set_columns}' + WHERE_CLAUSE
GROUP_BY_CLAUSE = 'GROUP BY {columns}'
ORDER_BY_CLAUSE = 'ORDER BY {columns}'
ASCENDING_ORDER = 'ASC'
DESCENDING_ORDER = 'DESC'
AND = 'AND'
