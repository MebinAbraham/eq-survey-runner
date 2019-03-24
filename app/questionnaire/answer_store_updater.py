from app.data_model.answer_store import Answer
from app.forms.questionnaire_form import QuestionnaireForm


class AnswerStoreUpdater:
    """Component responsible for any actions that need to happen as a result of updating the answer store
    """

    def __init__(self, current_location, schema, questionnaire_store, metadata):
        self._current_location = current_location
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._answer_store = self._questionnaire_store.answer_store
        self._metadata = metadata

    def save_answers(self, form):
        if isinstance(form, QuestionnaireForm):
            self._update_questionnaire_store_with_form_data(form.data)
        else:
            self._update_questionnaire_store_with_answer_data(form.serialise())

        if self._current_location not in self._questionnaire_store.completed_blocks:
            self._questionnaire_store.completed_blocks.append(self._current_location)

        self._questionnaire_store.add_or_update()

    def _update_questionnaire_store_with_answer_data(self, answers):
        survey_answer_ids = self._schema.get_answer_ids_for_block(self._current_location.block_id)

        valid_answers = (
            answer for answer in answers
            if answer.answer_id in survey_answer_ids
        )

        for answer in valid_answers:
            self._answer_store.add_or_update(answer)

    def _update_questionnaire_store_with_form_data(self, answers):
        survey_answer_ids = self._schema.get_answer_ids_for_block(self._current_location.block_id)

        for answer_id, answer_value in answers.items():

            # If answer is not answered then check for a schema specified default
            if answer_value is None:
                answer_value = self._schema.get_answer_with_context(answer_id, self._metadata, self._answer_store).get('default')

            if answer_id in survey_answer_ids:
                if answer_value is not None:
                    answer = Answer(answer_id=answer_id,
                                    value=answer_value)

                    self._answer_store.add_or_update(answer)
                else:
                    self._remove_answer_from_questionnaire_store(answer_id)

    def _remove_answer_from_questionnaire_store(self, answer_id):
        self._answer_store.remove(answer_ids=[answer_id])
