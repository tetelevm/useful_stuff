"""
A collection of several functions that describe the database structure
of a django application.
(there are probably a lot of undeveloped places here)
"""


def list_of_models(app_name: str):
    from django.apps import apps
    direct_models = list(apps.get_app_config(app_name).get_models())
    hidden_m2m_models = [
        getattr(m2m.model, m2m.name).through
        for model in direct_models
        for m2m in model._meta.local_many_to_many
    ]

    return direct_models + hidden_m2m_models


def get_field_info(field):
    column = field.column
    name = field.verbose_name or ""

    if field.primary_key:
        description = "PK"
    elif field.is_relation:
        description = f"FK к {field.related_model._meta.db_table}"
    else:
        description = f"{field.get_internal_type()}"
        if field.unique:
            description += " / уникальное"

    return [
        column,
        name,
        description,
    ]


def get_model_info(model):
    name = model.__name__
    db_name = model._meta.db_table
    doc = model._meta.verbose_name
    list_of_fields = [
        get_field_info(field)
        for field in model._meta.fields
    ]
    return [
        name,
        db_name,
        doc,
        list_of_fields,
    ]


def to_csv(all_models_info):
    import io
    import csv
    rows = [[
        "Название модели",
        "Таблица в бд",
        "Объект",
        "Столбец",
        "Название атрибута",
        "Описание",
    ]]
    for (n, dbn, d, lf) in all_models_info:
        for (c, cn, cd) in lf:
            rows.append([n, dbn, d, c, cn, cd])

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(rows)
    return output.getvalue()


