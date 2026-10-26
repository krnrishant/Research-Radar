import requests

ENDPOINT = 'http://127.0.0.1:5000/api/v1/papers?search=transformer'

# responce = requests.get(ENDPOINT)
# data = responce.json()
# print(type(data))

def test_can_call_endpoint():
    responce = requests.get(ENDPOINT)
    assert responce.status_code == 200
    pass

def test_response_contains_json():
    response = requests.get(ENDPOINT, timeout=15)
    data = response.json()
    assert isinstance(data, dict)
    pass

def test_result_exists_in_data():
    response = requests.get(ENDPOINT, timeout=15)
    data = response.json()
    assert 'results' in data
    pass

def test_result_is_list():
    response = requests.get(ENDPOINT, timeout=15)
    data = response.json()
    assert isinstance(data['results'], list)
    pass

def test_every_paper_have_title():
    response = requests.get(ENDPOINT, timeout=15)
    data = response.json()
    for item in data["results"]:
        assert 'title' in item
        pass

def test_does_very_title_has_a_useful_value():
    response = requests.get(ENDPOINT, timeout=15)
    data = response.json()
    for item in data["results"]:
        assert isinstance(item['title'], str)
        pass


