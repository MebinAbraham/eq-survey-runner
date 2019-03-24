from werkzeug.datastructures import MultiDict
from tests.app.app_context_test_case import AppContextTestCase

from app.helpers.form_helper import get_form_for_location, post_form_for_block
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.utilities.schema import load_schema_from_params
from app.data_model.answer_store import AnswerStore
from app.validation.validators import DateRequired, OptionalForm


class TestFormHelper(AppContextTestCase):

    def test_get_form_for_block_location(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_range')

            block_json = schema.get_block('date-block')
            location = Location(block_id='date-block')

            form = get_form_for_location(schema, block_json, location, AnswerStore(), metadata=None)

            self.assertTrue(hasattr(form, 'date-range-from-answer'))
            self.assertTrue(hasattr(form, 'date-range-to-answer'))

            period_from_field = getattr(form, 'date-range-from-answer')
            period_to_field = getattr(form, 'date-range-to-answer')

            self.assertIsInstance(period_from_field.month.validators[0], DateRequired)
            self.assertIsInstance(period_to_field.month.validators[0], DateRequired)

    def test_get_form_and_disable_mandatory_answers(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_range')

            block_json = schema.get_block('date-block')
            location = Location(block_id='date-block')

            form = get_form_for_location(schema, block_json, location,
                                         AnswerStore(), metadata=None, disable_mandatory=True)

            period_from_field = getattr(form, 'date-range-from-answer', None)
            period_to_field = getattr(form, 'date-range-to-answer', None)

            assert period_from_field
            assert period_to_field

            self.assertIsInstance(period_from_field.month.validators[0], OptionalForm)
            self.assertIsInstance(period_to_field.month.validators[0], OptionalForm)

    def test_get_form_and_disable_mandatory_answers_with_variants(self):
        with self.app_request_context():
            schema_input = {
                'sections': [{
                    'id': 'section1',
                    'groups': [{
                        'id': 'group1',
                        'title': 'Group 1',
                        'blocks': [
                            {
                                'id': 'block1',
                                'type': 'Question',
                                'title': 'Block 1',
                                'question_variants': [
                                    {
                                        'when': [{
                                            'id': 'when-answer',
                                            'condition': 'equals',
                                            'value': 'yes'
                                        }],
                                        'question': {
                                            'id': 'question1',
                                            'title': 'Question 1, Yes',
                                            'mandatory': True,
                                            'answers': [
                                                {
                                                    'id': 'answer1',
                                                    'label': 'Answer 1 Variant 1',
                                                    'type': 'TextField',
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'when': [{
                                            'id': 'when-answer',
                                            'condition': 'not equals',
                                            'value': 'yes'
                                        }],
                                        'question': {
                                            'id': 'question1',
                                            'title': 'Question 1, No',
                                            'mandatory': True,
                                            'answers': [
                                                {
                                                    'id': 'answer1',
                                                    'label': 'Answer 1 Variant 2',
                                                    'type': 'TextField',
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        ]
                    }]
                }]
            }

            schema = QuestionnaireSchema(schema_input)

            block_json = schema.get_block('block1')
            location = Location(block_id='block1')

            form = get_form_for_location(schema, block_json, location,
                                         AnswerStore(), metadata=None, disable_mandatory=True)

            form_answer = getattr(form, 'answer1', None)

            assert form_answer

            assert 'optional' in form_answer.validators[0].field_flags

    def test_post_form_for_block_location(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_range')

            block_json = schema.get_block('date-block')

            form = post_form_for_block(schema, block_json, AnswerStore(), metadata=None, request_form={
                'date-range-from-answer-day': '1',
                'date-range-from-answer-month': '05',
                'date-range-from-answer-year': '2015',
                'date-range-to-answer-day': '1',
                'date-range-to-answer-month': '09',
                'date-range-to-answer-year': '2017',
            })

            self.assertTrue(hasattr(form, 'date-range-from-answer'))
            self.assertTrue(hasattr(form, 'date-range-to-answer'))

            period_from_field = getattr(form, 'date-range-from-answer')
            period_to_field = getattr(form, 'date-range-to-answer')

            self.assertIsInstance(period_from_field.month.validators[0], DateRequired)
            self.assertIsInstance(period_to_field.month.validators[0], DateRequired)

            self.assertEqual(period_from_field.data, '2015-05-01')
            self.assertEqual(period_to_field.data, '2017-09-01')

    def test_post_form_and_disable_mandatory(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'date_range')

            block_json = schema.get_block('date-block')

            form = post_form_for_block(schema, block_json, AnswerStore(), metadata=None, request_form={
            }, disable_mandatory=True)

            self.assertTrue(hasattr(form, 'date-range-from-answer'))
            self.assertTrue(hasattr(form, 'date-range-to-answer'))

            period_from_field = getattr(form, 'date-range-from-answer')
            period_to_field = getattr(form, 'date-range-to-answer')

            self.assertIsInstance(period_from_field.month.validators[0], OptionalForm)
            self.assertIsInstance(period_to_field.month.validators[0], OptionalForm)

    def test_post_form_for_radio_other_not_selected(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'radio_mandatory_with_mandatory_other')

            block_json = schema.get_block('radio-mandatory')

            answer_store = AnswerStore([
                {
                    'answer_id': 'radio-mandatory-answer',
                    'value': 'Other',
                },
                {
                    'answer_id': 'other-answer-mandatory',
                    'value': 'Other text field value',
                }
            ])

            form = post_form_for_block(schema, block_json, answer_store, metadata=None,
                                       request_form=MultiDict({'radio-mandatory-answer': 'Bacon',
                                                               'other-answer-mandatory': 'Old other text'}))

            self.assertTrue(hasattr(form, 'radio-mandatory-answer'))

            other_text_field = getattr(form, 'other-answer-mandatory')
            self.assertEqual(other_text_field.data, '')

    def test_post_form_for_radio_other_selected(self):
        with self.app_request_context():
            schema = load_schema_from_params('test', 'radio_mandatory_with_mandatory_other')

            block_json = schema.get_block('radio-mandatory')

            answer_store = AnswerStore([
                {
                    'answer_id': 'radio-mandatory-answer',
                    'value': 'Other',
                },
                {
                    'answer_id': 'other-answer-mandatory',
                    'value': 'Other text field value',
                }
            ])

            request_form = MultiDict({
                'radio-mandatory-answer': 'Other',
                'other-answer-mandatory': 'Other text field value',
            })
            form = post_form_for_block(schema, block_json, answer_store, metadata=None, request_form=request_form)

            other_text_field = getattr(form, 'other-answer-mandatory')
            self.assertEqual(other_text_field.data, 'Other text field value')
