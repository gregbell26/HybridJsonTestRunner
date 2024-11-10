def gradescopeResultFinalizer(json_data):
    total_score = 0
    for test in json_data["tests"]:
        total_score += test.get("score", 0.0)
    json_data["score"] = total_score

def prairieLearnResultFinalizer(json_data):
    json_data["gradable"] = True
    # this is super hacky, but will work for now
    json_data.pop("leaderboard", None)
    json_data.pop("visibility", None)
    json_data.pop("stdout_visibility", None)
    json_data.pop("execution_time", None)

    total_score = 0
    for test in json_data["tests"]:
        total_score += test.get("points", 0.0)

    json_data["score"] = total_score
