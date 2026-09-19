from types import SimpleNamespace

from auth import user_context
from engine.tools.sql_tools import get_usuario_id_by_nome
from models.finance_models import AuthUser, Usuario


class _Query:
    def __init__(self, model, auth_user):
        self.model = model
        self.auth_user = auth_user

    def filter(self, *_args, **_kwargs):
        return self

    def first(self):
        if self.model is AuthUser:
            return self.auth_user
        return None


class _Database:
    def __init__(self, auth_user):
        self.auth_user = auth_user
        self.added = []

    def query(self, model):
        return _Query(model, self.auth_user)

    def add(self, value):
        self.added.append(value)

    def flush(self):
        self.added[-1].id = 99


def test_default_financial_profile_is_created_for_authenticated_user():
    db = _Database(SimpleNamespace(id=7, name="Dev"))

    with user_context(7):
        user_id = get_usuario_id_by_nome(db, None)

    assert user_id == 99
    assert isinstance(db.added[0], Usuario)
    assert db.added[0].nome == "Dev"


def test_unknown_explicit_financial_user_is_not_replaced_by_user_one():
    db = _Database(SimpleNamespace(id=7, name="Dev"))

    with user_context(7):
        user_id = get_usuario_id_by_nome(db, "Outra pessoa")

    assert user_id is None
    assert db.added == []
