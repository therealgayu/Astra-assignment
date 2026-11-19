import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, Mock
from enumeration.rest_api import enumerate_via_rest_api


def test_rest_api_parses_valid_response():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"slug": "testadmin", "name": "Test Admin"}
    ]

    with patch("enumeration.rest_api.requests.get", return_value=mock_response):
        results = enumerate_via_rest_api("http://fake-target.local")

    assert len(results) == 1
    assert results[0]["username"] == "testadmin"


def test_rest_api_handles_empty_list():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []

    with patch("enumeration.rest_api.requests.get", return_value=mock_response):
        results = enumerate_via_rest_api("http://fake-target.local")

    assert results == []


def test_rest_api_handles_non_200_status():
    mock_response = Mock()
    mock_response.status_code = 404

    with patch("enumeration.rest_api.requests.get", return_value=mock_response):
        results = enumerate_via_rest_api("http://fake-target.local")

    assert results == []


def test_rest_api_handles_malformed_json():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("bad json")

    with patch("enumeration.rest_api.requests.get", return_value=mock_response):
        results = enumerate_via_rest_api("http://fake-target.local")

    assert results == []