def gradescopeResultBuilder(name, failure_prefix, err, hide_errors_message, weight, tags, number, visibility, score, output):
    failed = err is not None

    if err:
        if hide_errors_message:
            output += hide_errors_message
        else:
            if output:
                # Create a double newline if output is not empty
                if output.endswith('\n'):
                    output += '\n'
                else:
                    output += '\n\n'
            output += "{0}{1}\n".format(failure_prefix, err[1])
    result = {
        "name": name
    }
    if score is not None or weight is not None:
        if weight is None:
            weight = 0.0
        if score is None:
            score = 0.0 if failed else weight
        result["score"] = score
        result["max_score"] = weight
        # Also mark failure if points are lost
        failed |= score < weight

    result["status"] = "failed" if failed else "passed"

    if tags:
        result["tags"] = tags
    if output:
        result["output"] = output
    if visibility:
        result["visibility"] = visibility
    if number:
        result["number"] = number
    return result
