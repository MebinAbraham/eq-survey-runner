import logging
import json
from app import settings
from datetime import datetime

logger = logging.getLogger(__name__)


class SubmitterConstants(object):

    PARADATA_KEY = "paradata"

    METADATA_KEY = "metadata"

    RU_REF_KEY = "ru_ref"

    USER_ID_KEY = "user_id"

    SUBMITTED_AT_KEY = "submitted_at"

    COLLECTION_KEY = "collection"

    PERIOD_KEY = "period"

    EXERCISE_SID_KEY = "exercise_sid"

    INSTRUMENT_KEY = "instrument_id"

    SURVEY_ID_KEY = "survey_id"

    ORIGIN_KEY = "origin"

    VERSION_KEY = "version"

    TYPE_KEY = "type"

    DATA_KEY = "data"

    TYPE = "uk.gov.ons.edc.eq:surveyresponse"

    VERSION = "0.0.1"

    ORIGIN = "uk.gov.ons.edc.eq"


class Converter(object):

    @staticmethod
    def prepare_responses(user, metadata_store, questionnaire, responses):
        """
        Create the JSON response format for down stream processing

        :param questionnaire: the questionnaire model
        :param responses: the users responses
        :return: a JSON object in the following format:
          {
            "type" : "uk.gov.ons.edc.eq:surveyresponse",
            "version" : "0.0.1",
            "origin" : "uk.gov.ons.edc.eq",
            "survey_id": "021",
            "collection":{
              "exercise_sid": "hfjdskf",
              "instrument_id": "yui789",
              "period": "2016-02-01"
            },
            "submitted_at": "2016-03-07T15:28:05Z",
            "metadata": {
              "user_id": "789473423",
              "ru_ref": "432423423423"
            },
            "paradata": {},
            "data": {
              "001": "2016-01-01",
              "002": "2016-03-30"
            }
          }
        """
        survey_id = questionnaire.survey_id
        data = {}

        for key in responses.keys():
            item = questionnaire.get_item_by_id(key)
            if item is not None:
                value = responses[key]
                if value:
                    data[item.code] = value

        metadata = {SubmitterConstants.USER_ID_KEY: metadata_store.get_user_id(),
                    SubmitterConstants.RU_REF_KEY: metadata_store.get_ru_ref()}

        collection = {SubmitterConstants.EXERCISE_SID_KEY: metadata_store.get_collection_exercise_sid(),
                      SubmitterConstants.INSTRUMENT_KEY: metadata_store.get_form_type(),
                      SubmitterConstants.PERIOD_KEY: metadata_store.get_period_id()}

        paradata = {}
        submitted_at = datetime.now(settings.EUROPE_LONDON)

        response = {SubmitterConstants.TYPE_KEY: SubmitterConstants.TYPE,
                    SubmitterConstants.VERSION_KEY: SubmitterConstants.VERSION,
                    SubmitterConstants.ORIGIN_KEY: SubmitterConstants.ORIGIN,
                    SubmitterConstants.SURVEY_ID_KEY: survey_id,
                    SubmitterConstants.SUBMITTED_AT_KEY: submitted_at.strftime(settings.DATETIME_FORMAT),
                    SubmitterConstants.COLLECTION_KEY: collection,
                    SubmitterConstants.METADATA_KEY: metadata,
                    SubmitterConstants.PARADATA_KEY: paradata,
                    SubmitterConstants.DATA_KEY: data}

        logging.debug("Converted response ready for submission %s", json.dumps(response))
        return response, submitted_at
