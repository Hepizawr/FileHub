import datetime as dt
import os
import re
import traceback
import typing as t

import flask
from pydantic import BaseModel
from werkzeug.datastructures import FileStorage

import app.models as db_model
import app.schemas as net_model
from app import db

JsonResponse = t.Tuple[flask.Response, int]


def make_dir_if_does_not_exist(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path)


def get_file_format(filename: str) -> str:
    pattern = r"\.(?:[a-zA-Z0-9]+\.?)+$"
    match = re.search(pattern, filename)
    return match.group(0) if match else ""


def get_file_name(filename: str) -> str:
    file_format = get_file_format(filename)
    return filename.replace(file_format, "")


def save_file(
    file: FileStorage,
    directory: str,
    name: t.Optional[str] = None,
    filename: t.Optional[str] = None,
) -> str:
    make_dir_if_does_not_exist(directory)
    if not filename:
        file_format = get_file_format(file.filename)
        filename = f"{name}{file_format}" if name else file.filename
    file_path = os.path.join(directory, filename)
    file.save(file_path)
    return file_path


def convert_db_type_to_net_type(db_type: t.Type[db.Model]) -> t.Type[BaseModel]:
    assert hasattr(net_model, db_type.__name__)
    return getattr(net_model, db_type.__name__)


def convert_net_type_to_db_type(net_type: t.Type[BaseModel]) -> t.Type[db.Model]:
    assert hasattr(db_model, net_type.__name__)
    return getattr(db_model, net_type.__name__)


def convert_db_model_to_net_model(db_model: db.Model, net_type: t.Type[BaseModel]) -> BaseModel:
    return net_type.model_validate(db_model, from_attributes=True)


def convert_db_models_to_response(db_models: t.Sequence[db.Model], net_type: t.Type[BaseModel]) -> t.List[t.Dict]:
    net_models = [convert_db_model_to_net_model(db_model, net_type).dict() for db_model in db_models]
    return net_models


def convert_db_model_to_dict(db_model: db.Model) -> t.Dict:
    db_type = type(db_model)
    net_type = convert_db_type_to_net_type(db_type)
    net_model = convert_db_model_to_net_model(db_model, net_type)
    return net_model.model_dump(mode="json")


def prepare_data_for_db_type(db_type: t.Type[db.Model], data: t.Dict) -> t.Dict:
    prepared_data = {}
    for key, value in data.items():
        if hasattr(db_type, key):
            if value is not None:
                attr_type = getattr(db_type, key)
                if not isinstance(attr_type, property):
                    attr_py_type = attr_type.type.python_type
                    if not isinstance(value, attr_py_type):
                        if attr_py_type is dt.datetime:
                            value = dt.datetime.strptime(value, "%Y-%m-%d")
                        else:
                            value = attr_py_type(value)
            prepared_data[key] = value
    return prepared_data


def create_db_record_as_response(db_type: t.Type[db.Model], data: t.Dict) -> JsonResponse:
    prepared_data = prepare_data_for_db_type(db_type, data)
    new_db_item = db_type(**prepared_data)

    try:
        db.session.add(new_db_item)
        db.session.commit()
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        flask.abort(code=500)

    response_data = convert_db_model_to_dict(db_model=new_db_item)
    return flask.jsonify(response_data), 201


def update_db_record_as_response(db_model: db.Model, new_data: t.Optional[t.Dict]) -> JsonResponse:
    if new_data is not None:
        db_type = type(db_model)
        prepared_data = prepare_data_for_db_type(db_type, new_data)
        [setattr(db_model, key, value) for key, value in prepared_data.items()]

        try:
            db.session.commit()
        except Exception as e:
            traceback.print_exc()
            db.session.rollback()
            flask.abort(code=500)

        response_data = convert_db_model_to_dict(db_model=db_model)
        return flask.jsonify(response_data), 201


def delete_db_record_as_response(db_model: db.Model) -> JsonResponse:
    try:
        db.session.delete(db_model)
        db.session.commit()
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        flask.abort(code=500)

    response_data = {}
    return flask.jsonify(response_data), 204
