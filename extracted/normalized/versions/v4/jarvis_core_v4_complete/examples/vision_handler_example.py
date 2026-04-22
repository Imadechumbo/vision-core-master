def vision_handler(payload):
    uploaded_file = payload.get('file')
    if uploaded_file is None:
        return {'ok': False, 'error': 'missing_file'}, 400
    mimetype = getattr(uploaded_file, 'mimetype', None)
    if not mimetype:
        return {'ok': False, 'error': 'missing_mimetype'}, 400
    return {'ok': True, 'message': 'vision ok'}, 200
