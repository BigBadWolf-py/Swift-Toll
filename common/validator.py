def validate_json(json, param_keys):
    if json is None:
        raise Exception('Invalid JSON')

    if param_keys is None:
        return json
    else:
        for key in param_keys:
            try:
                if len(str(json[key]).strip()) == 0:
                    raise Exception('Missing field value: ' + key)
            except KeyError as e:
                    raise Exception('Missing field: ' + e.args[0])
        return json