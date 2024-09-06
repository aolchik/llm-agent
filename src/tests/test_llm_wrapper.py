import unittest
from unittest.mock import patch
from helpers.llm_wrapper import get_llm


class TestLLMWrapper(unittest.TestCase):

    @patch('helpers.llm_wrapper.ChatGoogleGenerativeAI')
    @patch('os.getenv', return_value='google_service_account.json')
    @patch('google.oauth2.service_account.Credentials.'
           'from_service_account_file')
    def test_get_llm_google(self,
                            mock_credentials,
                            mock_os_getenv,
                            mock_chat_google_generative_ai):
        model_provider = 'google'
        model_name = 'gemini-1.5-flash'

        get_llm(model_provider, model_name)

        mock_os_getenv.assert_called_once_with("GOOGLE_SERVICE_ACCOUNT_FILE")
        mock_credentials.assert_called_once_with(mock_os_getenv.return_value)
        mock_chat_google_generative_ai.assert_called_once_with(
            model=model_name,
            verbose=True,
            temperature=0,
            credentials=mock_credentials.return_value
        )

    @patch('helpers.llm_wrapper.Ollama')
    def test_get_llm_ollama(self, mock_ollama):
        model_provider = 'ollama'
        model_name = 'openhermes'

        get_llm(model_provider, model_name)

        mock_ollama.assert_called_once_with(model=model_name)

    @patch('helpers.llm_wrapper.ChatOpenAI')
    def test_get_llm_openai(self, mock_chat_openai):
        model_provider = 'openai'
        model_name = 'gpt-4o'

        get_llm(model_provider, model_name)

        mock_chat_openai.assert_called_once_with(model=model_name,
                                                 temperature=0,
                                                 verbose=True,
                                                 stream_usage=True)

    def test_raise_exception_on_invalid_provider(self):
        model_provider = 'invalid_provider'
        model_name = 'invalid_model'

        with self.assertRaises(Exception):
            get_llm(model_provider, model_name)

    def test_raise_exception_on_invalid_model_from_google(self):
        model_provider = 'google'
        model_name = 'invalid_model'

        with self.assertRaises(Exception):
            get_llm(model_provider, model_name)

    def test_raise_exception_on_invalid_model_from_openai(self):
        model_provider = 'openai'
        model_name = 'invalid_model'

        with self.assertRaises(Exception):
            get_llm(model_provider, model_name)

    def test_raise_exception_on_invalid_model_from_ollama(self):
        model_provider = 'ollama'
        model_name = 'invalid_model'

        with self.assertRaises(Exception):
            get_llm(model_provider, model_name)


if __name__ == '__main__':
    unittest.main()
