# robo-advisor/test/robo_advisor_test.py

import json

from app.robo_advisor import to_usd, to_one_decimal_perc, get_response

def test_to_usd():
    result = to_usd(1500)
    assert result == "$1,500.00"
    
    result = to_usd(98.78384)
    assert result == "$98.78"

    result = to_usd(2.5)
    assert result == "$2.50"

def test_to_one_decimal_perc():
    result = to_one_decimal_perc(0.83724)
    assert result == "0.8%"

    result = to_one_decimal_perc(1.5)
    assert result == "1.5%"

def test_get_response():
    t = "MSFT"
    response = get_response(t)
    parsed_response = json.loads(response.text)

    assert isinstance(parsed_response, dict)
    assert "Meta Data" in parsed_response.keys()
    assert "Time Series (Daily)" in parsed_response.keys()
    assert parsed_response["Meta Data"]["2. Symbol"] == t
