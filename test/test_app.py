def test_app_is_created(app):
    assert app.name == 'padaria.app'

def test_config_is_loaded(config):
    assert config['DEBUG'] is False

def test_request_return_404(client):
    assert client.get("/url_que_nao_existe").status_code == 404