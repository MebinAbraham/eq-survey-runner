from functools import wraps

from app.globals import get_session_store
from app.utilities.schema import load_schema_from_session_data
from app.questionnaire.rules import evaluate_when_rules


def with_schema(function):
    """Adds the survey schema as the first argument to the function being wrapped.
    Use on flask request handlers or methods called by flask request handlers.

    May error unless there is a `current_user`, so should be used as follows e.g.

    ```python
    @login_required
    @with_schema
    @full_routing_path_required
    def get_block(routing_path, schema, *args):
        ...
    ```
    """

    @wraps(function)
    def wrapped_function(*args, **kwargs):
        session_data = get_session_store().session_data
        schema = load_schema_from_session_data(session_data)
        return function(schema, *args, **kwargs)

    return wrapped_function


def choose_question_to_display(block, schema, metadata, answer_store):
    if block.get('question'):
        return block['question']

    for question_variant in block.get('question_variants'):
        when_rules = question_variant.get('when', [])
        if evaluate_when_rules(when_rules, schema, metadata, answer_store):
            return question_variant['question']
