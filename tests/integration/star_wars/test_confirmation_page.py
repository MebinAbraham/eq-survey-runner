from werkzeug.datastructures import MultiDict

from tests.integration.star_wars import star_wars_test_urls
from tests.integration.star_wars.star_wars_tests import StarWarsTestCase


class TestConfirmationPage(StarWarsTestCase):

    def test_confirmation_page(self):
        self.rogue_one_login_and_check_introduction_text()
        post_data = {
            'action[start_questionnaire]': 'Start Questionnaire'
        }
        response = self.client.post(star_wars_test_urls.ROGUE_ONE_INTRODUCTION, data=post_data, follow_redirects=False)
        self.assertEqual(response.status_code, 302)

        character_page = response.headers['Location']

        self.rogue_one_check_character_page(character_page)

        # Our answers
        form_data = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "Cassian Andor",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # Form submission with no errors
        resp = self.submit_page(character_page, form_data)
        self.assertNotEqual(resp.location, character_page)

        # Like page
        description_page = resp.location

        self.rogue_one_check_description_page(description_page)

        # Our answers
        form_data = {
            "3f1f1bb7-2452-4f8d-ac7a-735ea5d4517f": "Yes",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # Form submission with no errors
        resp = self.submit_page(description_page, form_data)
        self.assertNotEqual(resp.location, description_page)

        # Takings page
        takings_page = resp.location

        self.rogue_one_check_takings_page(takings_page)

        # Our answers
        form_data = {
            "a04a516d-502d-4068-bbed-a43427c68cd9": "900",
            # User Action
            "action[save_continue]": "Save &amp; Continue"
        }

        # Form submission with no errors
        resp = self.submit_page(takings_page, form_data)
        self.assertNotEqual(resp.location, takings_page)

        # Confirmation page
        confirmation_page = resp.location

        self.rogue_one_check_confirmation_page(confirmation_page)

        # User Action
        form_data["action[save_continue]"] = "Save &amp; Continue"

        # Form submission with no errors
        resp = self.submit_page(confirmation_page, form_data)
        self.assertNotEqual(resp.location, confirmation_page)

        self.complete_survey(confirmation_page, 'rogue_one')
