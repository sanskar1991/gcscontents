import pytest
from mock import patch
from api.weather_restfulapi import app

class TestWeatherRestfulAPI():
    @pytest.fixture()
    def before(self):
        print("-------------------------")
    
    @patch("api.weather_restfulapi.WeatherById")
    def test_WeatherById(self, mock):
        fake_json = {"weather": "cloudy"}
        obj = mock()
        obj.get.return_value.status_code = 200
        obj.get.return_value.data = fake_json
        obj.get.return_value.content_type = "application/json"
        response = obj.get(1)
        assert response.status_code == 200
        print("working")
        # assert response.content_type == "application/json"
    def test_WeatherList(self):
        pass
    tester = app.test_client()
    response = tester.get('/')
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main()