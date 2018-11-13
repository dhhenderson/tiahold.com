def test_home(app):
    res = app.get('/')
    assert res.status_code == 200
    assert b'This Is A House Of Learned Doctors' in res.data

# test favs - confirm db settings
def test_favs(app):
    res = app.get('/favs')
    assert res.status_code == 200
    assert b'bloom' in res.data
