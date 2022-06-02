from opendlp.sensitive_analyze.entity_recognize.conf import config

def get_threshold(thresholds, name):

    if type(thresholds)==dict and name in thresholds.keys():
        threshold = thresholds[name]
        if threshold < 0:
            threshold = 0
        elif threshold > 1:
            threshold = 1
    else:
        threshold = config.THRESHOLD_PREDEFINED.get(name, config.THRESHOLD_USERDEFINED)

    return threshold