from flask import render_template, session
from flask_login import login_required, current_user
from .. import main_blueprint
import logging
from app.submitter.converter import SubmitterConstants
from app.main.views.root import load_and_parse_schema
from app.main import errors
from app.main.views.root import redirect_to_location
from app.utilities.factory import factory

logger = logging.getLogger(__name__)


@main_blueprint.route('/thank-you', methods=['GET'])
@login_required
def thank_you():
    logger.debug("Requesting thank you page")

    # Redirect to questionnaire page if submission has been skipped
    if SubmitterConstants.SUBMITTED_AT_KEY not in session:
        return redirect_to_location('questionnaire')

    metadata = factory.create("metadata-store")

    # load the schema
    schema = load_and_parse_schema(metadata.get_eq_id(), metadata.get_form_type())

    if not schema:
        return errors.page_not_found()

    # TODO this should be part of the navigation store really
    submitted_at = session[SubmitterConstants.SUBMITTED_AT_KEY]

    # finally delete all their data
    current_user.delete_questionnaire_data()

    return render_template('thank-you.html', data={
        "survey_code": schema.survey_id,
        "period_str": metadata.get_period_str(),
        "respondent_id": metadata.get_ru_ref(),
        "submitted_at": submitted_at,
        "title": schema.title
    }, bar_title=schema.title)
