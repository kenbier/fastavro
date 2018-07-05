import pytest
import fastavro
from fastavro.schema import SchemaParseException, UnknownType, parse_schema

pytestmark = pytest.mark.usefixtures("clean_schemas")


def test_named_types_have_names():
    record_schema = {
        "type": "record",
        "fields": [{
            "name": "field",
            "type": "string",
        }],
    }

    with pytest.raises(SchemaParseException):
        fastavro.parse_schema(record_schema)

    error_schema = {
        "type": "error",
        "fields": [{
            "name": "field",
            "type": "string",
        }],
    }

    with pytest.raises(SchemaParseException):
        fastavro.parse_schema(error_schema)

    fixed_schema = {
        "type": "fixed",
        "size": 1,
    }

    with pytest.raises(SchemaParseException):
        fastavro.parse_schema(fixed_schema)

    enum_schema = {
        "type": "enum",
        "symbols": ["FOO"],
    }

    with pytest.raises(SchemaParseException):
        fastavro.parse_schema(enum_schema)

    # Should parse with name
    for schema in (record_schema, error_schema, fixed_schema, enum_schema):
        schema["name"] = "test_named_types_have_names"
        fastavro.parse_schema(schema)


def test_parse_schema():
    schema = {
        "type": "record",
        "name": "test_parse_schema",
        "fields": [{
            "name": "field",
            "type": "string",
        }],
    }

    parsed_schema = parse_schema(schema)
    assert "__fastavro_parsed" in parsed_schema

    parsed_schema_again = parse_schema(parsed_schema)
    assert parsed_schema_again == parsed_schema


def test_unknown_type():
    schema = {
        "type": "unknown",
    }

    with pytest.raises(UnknownType):
        parse_schema(schema)
