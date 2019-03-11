from app.questionnaire.rules import evaluate_when_rules


def get_question_to_display(block, metadata, answer_store, schema):
    if block.get('question'):
        return block['question']

    for question_variant in block.get('question_variants', []):
        when_rules = question_variant.get('when', [])
        if evaluate_when_rules(when_rules, schema, metadata, answer_store):
            return question_variant['question']
