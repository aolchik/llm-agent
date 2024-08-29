import unittest
import os
from unittest.mock import patch
from pydantic import ValidationError

from helpers.tracer import \
    LLMProxyConfig, \
    Tracer, \
    TracerAnnotation, \
    TracerFactory, \
    AGENTOPS_API_KEY, \
    LANGTRACE_API_KEY


class TestTracer(unittest.TestCase):

    def setUp(self):
        self.tracer = TracerFactory.get_tracer()

    @patch('agentops.init')
    @patch('langtrace_python_sdk.langtrace.init')
    def test_init_agentops(self, mock_langtrace_init, mock_agentops_init):
        tracer_annotation = TracerAnnotation(app="TestApp")
        self.tracer.provider = 'agentops'
        self.tracer.annotation = tracer_annotation

        self.tracer.init()

        mock_agentops_init.assert_called_once_with(
            AGENTOPS_API_KEY,
            default_tags=[[tracer_annotation.app]]
        )
        mock_langtrace_init.assert_not_called()

    @patch('agentops.init')
    @patch('langtrace_python_sdk.langtrace.init')
    def test_init_langtrace(self, mock_langtrace_init, mock_agentops_init):
        tracer_annotation = TracerAnnotation(app="TestApp")
        self.tracer.provider = 'langtrace'
        self.tracer.annotation = tracer_annotation

        self.tracer.init()

        mock_langtrace_init.assert_called_once_with(api_key=LANGTRACE_API_KEY)
        mock_agentops_init.assert_not_called()

    @patch('agentops.end_session')
    def test_end_session(self, mock_agentops_end_session):
        self.tracer.provider = 'agentops'
        self.tracer.annotation = None

        self.tracer.end()

        mock_agentops_end_session.assert_called_once_with("Success")

    @patch('os.getenv', return_value='hak-123')
    def test_get_proxy_config_no_annotation(self, mock_os_getenv):
        self.tracer.provider = 'helicone'
        self.tracer.annotation = None

        expected_headers = {
            "Helicone-Auth": f"Bearer {os.getenv('HELICONE_API_KEY')}",
            "Helicone-Cache-Enabled": "true",
        }

        self.assertEqual(
            self.tracer.get_proxy_config(),
            LLMProxyConfig(url="https://oai.helicone.ai/v1",
                           headers=expected_headers)
        )

        self.tracer.provider = 'agentops'
        self.assertIsNone(self.tracer.get_proxy_config())

        self.tracer.provider = 'langtrace'
        self.assertIsNone(self.tracer.get_proxy_config())

        self.tracer.provider = 'invalid_provider'
        self.assertIsNone(self.tracer.get_proxy_config())

    @patch('os.getenv', return_value='hak-123')
    def test_get_proxy_config_with_annotation(self, mock_os_getenv):
        tracer_annotation = TracerAnnotation(app="TestApp")
        self.tracer.provider = 'helicone'
        self.tracer.annotation = tracer_annotation

        expected_headers = {
            "Helicone-Auth": f"Bearer {os.getenv('HELICONE_API_KEY')}",
            "Helicone-Cache-Enabled": "true",
            "Helicone-Session-Id": tracer_annotation.session,
            "Helicone-Property-App": tracer_annotation.app
        }

        self.assertEqual(
            self.tracer.get_proxy_config(),
            LLMProxyConfig(url="https://oai.helicone.ai/v1",
                           headers=expected_headers)
        )

    def test_get_tracer_annotation(self):
        tracer_annotation = TracerAnnotation(app="TestApp")
        self.tracer.provider = 'agentops'
        self.tracer.annotation = tracer_annotation

        self.assertEqual(self.tracer.get_tracer_annotation(),
                         tracer_annotation)

    def test_invalid_provider(self):
        with self.assertRaises(ValidationError):
            Tracer(provider='invalid_provider')


if __name__ == '__main__':
    unittest.main()
