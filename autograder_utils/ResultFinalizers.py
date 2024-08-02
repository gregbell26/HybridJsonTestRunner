def gradescopeResultFinalizer(json_data):
    total_score = 0
    for test in json_data["tests"]:
        total_score += test.get("score", 0.0)
    json_data["score"] = total_score

def prairieLearnResultFinalizer(json_data):
    json_data["gradable"] = True

    total_score = 0
    for test in json_data["tests"]:
        total_score += test.get("points", 0.0)

    json_data["score"] = total_score
