def formatErrors(failure_prefix, output, err):
    if output:
        # Create a double newline if output is not empty
        if output.endswith('\n'):
            output += '\n'
        else:
            output += '\n\n'
    output += "{0}{1}\n".format(failure_prefix, err[1])

    return output

def encodeHTML(data_to_encode):
    lines = data_to_encode.splitlines(keepends=False)

    output = [f"<p>{line}</p>" for line in lines]

    return "\n".join(output)


def gradescopeResultBuilder(name, failure_prefix, err, hide_errors_message, weight, tags, number, visibility, score,
                            output, image_data):
    failed = err is not None

    if err:
        if hide_errors_message:
            output += hide_errors_message
        else:
            output += formatErrors(failure_prefix, output, err)

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

    if image_data:
        output = encodeHTML(output)

        output += f"\n<figure><img src='data:image/{image_data['image_type']};base64,{image_data['data']}'/><figcaption>{image_data['label']}</figcaption></figure>"
    if tags:
        result["tags"] = tags
    if output:
        result["output"] = output
    if visibility:
        result["visibility"] = visibility
    if number:
        result["number"] = number

    return result


def prairieLearnResultBuilder(name, failure_prefix, err, hide_errors_message, weight, tags, number, visibility, score,
                              output, image_data):
    failed = err is not None
    if err:
        if hide_errors_message:
            output += hide_errors_message
        else:
            output += formatErrors(failure_prefix, output, err)

    result = {
        "name": name,
        "description": "",
    }
    if score is not None or weight is not None:
        if weight is None:
            weight = 0.0
        if score is None:
            score = 0.0 if failed else weight
        result["points"] = score
        result["max_points"] = weight
        # Also mark failure if points are lost
        failed |= score < weight

    result["message"] = "Test Failed!" if failed else "Test Succeeded"


    if output:
        result["output"] = output
    if number:
        result["number"] = number

    # we can actually show and image here
    # we need to set {images: {label: ..., url: ...}} to a b64 encoded string

    # url: The source of the image, typically formatted as standard HTML base64 image like "data:[mimetype];base64,[contents]";
    # label: An optional label for the image (defaults to "Figure").

    if image_data:
        result["images"] = {
            "label": image_data["label"],
            "url": f"data:image/{image_data['image_type']};base64,{image_data['data']}"
        }

    return result
