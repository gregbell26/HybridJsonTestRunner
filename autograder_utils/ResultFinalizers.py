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
    total_test_cases = 0
    # get each test percentage
    for test in json_data["tests"]:
        if test.get("max_points", None) is None:
            # invalid test, don't count in total
            continue

        total_test_cases += 1
        points = test.get("points", 0.0)
        max_points = test.get("max_points")

        if points > max_points:
            points = max_points

        score = points / max_points

        total_score += score

    if total_test_cases == 0:
        json_data["gradable"] = False
        return

    # Convert that percentage to a global percentage
    json_data["score"] = total_score / total_test_cases
