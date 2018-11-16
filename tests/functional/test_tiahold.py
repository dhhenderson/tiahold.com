def test_home(app):
    res = app.get('/')
    assert res.status_code == 200
    assert b'This Is A House Of Learned Doctors' in res.data


def test_favs(app):
    """Test favs iot confirm db settings."""
    res = app.get('/favs')
    assert res.status_code == 200
    assert b'bloom' in res.data
