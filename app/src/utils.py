def to_schema(db_object, schema_class):
    return schema_class(**db_object.__dict__)


def to_schemas(db_objects, schema_class):
    return [to_schema(o, schema_class) for o in db_objects]
