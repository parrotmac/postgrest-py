import pytest

from postgrest_py import SyncFilterRequestBuilder
from postgrest_py.utils import SyncClient


@pytest.fixture
def filter_request_builder():
    with SyncClient() as client:
        yield SyncFilterRequestBuilder(client, "/example_table", "GET", {})


def test_constructor(filter_request_builder):
    builder = filter_request_builder

    assert builder.path == "/example_table"
    assert builder.http_method == "GET"
    assert builder.json == {}
    assert not builder.negate_next


def test_not_(filter_request_builder):
    builder = filter_request_builder.not_

    assert builder.negate_next


def test_filter(filter_request_builder):
    builder = filter_request_builder.filter(":col.name", "eq", "val")

    assert builder.session.params['":col.name"'] == "eq.val"


def test_multivalued_param(filter_request_builder):
    builder = filter_request_builder.lte("x", "a").gte("x", "b")

    assert str(builder.session.params) == "x=lte.a&x=gte.b"


def test_match(filter_request_builder):
    builder = filter_request_builder.match({"id": "1", "done": "false"})
    assert str(builder.session.params) == "id=eq.1&done=eq.false"
