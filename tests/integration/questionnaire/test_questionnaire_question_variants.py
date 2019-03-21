from tests.integration.integration_test_case import IntegrationTestCase

class TestQuestionnaireQuestionVariants(IntegrationTestCase):

    def test_non_proxy_answer_shows_non_proxy_title(self):
        self.launchSurvey('test', 'variants_question')

        self.assertInBody('Who is this questionnaire about')

        self.post({
            'first-name-answer': 'Linus',
            'last-name-answer': 'Torvalds'
        })
        self.assertInBody('Are you <em>Linus Torvalds</em>?')

        self.post({
            'proxy-answer': 'non-proxy'
        })

        self.assertInBody('What is your age?')

    def test_proxy_answer_shows_proxy_title(self):
        self.launchSurvey('test', 'variants_question')

        self.assertInBody('Who is this questionnaire about')

        self.post({
            'first-name-answer': 'Linus',
            'last-name-answer': 'Torvalds'
        })

        self.assertInBody('Are you <em>Linus Torvalds</em>?')

        self.post({
            'proxy-answer': 'proxy'
        })

        self.assertInBody('What age is <em>Linus Torvalds</em>?')

