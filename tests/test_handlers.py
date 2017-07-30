def test_check_400(app):
    """
    """
    url = '/api/v1/thandler?iteration_id=%s&link=%s' % (
        'sss',
        'ya.ru'
    )
    req, resp = app.test_client.get(url)

    assert resp.status == 400
