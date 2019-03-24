from app.questionnaire.rules import evaluate_when_rules


def _choose_variant(block, schema, metadata, answer_store, variants_key, single_key):
    print('block', block, single_key, variants_key)
    if block.get(single_key):
        return block[single_key]

    for question_variant in block.get(variants_key):
        when_rules = question_variant.get('when', [])
        if evaluate_when_rules(when_rules, schema, metadata, answer_store):
            return question_variant[single_key]


def choose_question_to_display(block, schema, metadata, answer_store):
    return _choose_variant(block, schema, metadata, answer_store, variants_key='question_variants', single_key='question')


def choose_content_to_display(block, schema, metadata, answer_store):
    return _choose_variant(block, schema, metadata, answer_store, variants_key='content_variants', single_key='content')


def transform_variants(block, schema, metadata, answer_store):
    if 'question_variants' in block:
        question = choose_question_to_display(block, schema, metadata, answer_store)
        block.pop('question_variants', None)
        block.pop('question', None)

        block['question'] = question

    if 'content_variants' in block:
        content = choose_content_to_display(block, schema, metadata, answer_store)
        block.pop('content_variants', None)
        block.pop('content', None)

        block['content'] = content

    return block


def get_answer_ids_in_block(block):
    question = block['question']
    answer_ids = []
    for answer in question['answers']:
        answer_ids.append(answer['id'])

    return answer_ids

