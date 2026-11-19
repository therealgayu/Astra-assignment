import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, Mock
from bruteforce.login_attempt import attempt_login


def test_login_success_detected():
    mock_get_response = Mock()
    mock_post_response = Mock()
    mock_post_response.status_code = 302
    mock_post_response.headers = {"Location": "http://fake-target.local/wp-admin/"}

    mock_session = Mock()
    mock_session.get.return_value = mock_get_response
    mock_session.post.return_value = mock_post_response
    mock_session.cookies.get_dict.return_value = {
        "wordpress_logged_in_abc123": "testadmin|..."
    }

    with patch("bruteforce.login_attempt.requests.Session", return_value=mock_session):
        result = attempt_login("http://fake-target.local", "testadmin", "password123")

    assert result is True


def test_login_failure_detected():
    mock_get_response = Mock()
    mock_post_response = Mock()
    mock_post_response.status_code = 200
    mock_post_response.headers = {}

    mock_session = Mock()
    mock_session.get.return_value = mock_get_response
    mock_session.post.return_value = mock_post_response
    mock_session.cookies.get_dict.return_value = {
        "wordpress_test_cookie": "WP Cookie check"
    }

    with patch("bruteforce.login_attempt.requests.Session", return_value=mock_session):
        result = attempt_login("http://fake-target.local", "testadmin", "wrongpassword")

    assert result is False