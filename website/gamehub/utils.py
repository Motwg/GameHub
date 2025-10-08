from datetime import datetime
from typing import Any
from flask import request


def convert_datatime(rows: dict[str, Any], field_name: str):
    if isinstance(rows[field_name], datetime):
        rows[field_name] = rows[field_name].strftime('%d/%m/%Y, %H:%M:%S')


def read_data_from_form() -> dict[Any, Any]:
    record: dict[str, Any] = {}
    for key in request.form:
        record[key] = request.form[key]
        if len(record[key]) == 0:
            record[key] = None
        elif record[key] == 'on':
            # checkbox selected!!!
            record[key] = True
    # NOTE: if a checkbox is not selected,
    #      it will NOT be part of the record dict!
    return record


def set_menu(section: str) -> dict[str, str]:
    menu_config: dict[str, str] = {}

    if len(section) > 0:
        menu_config[section] = 'active'

    return menu_config
