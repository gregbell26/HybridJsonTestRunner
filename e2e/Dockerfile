FROM gradescope/autograder-base:ubuntu-22.04

RUN apt install -y python3 python3-pip
RUN pip3 install --upgrade pip
ADD autograder_utils /tmp/autograder_utils/autograder_utils
ADD pyproject.toml /tmp/autograder_utils/pyproject.toml

RUN pip3 install /tmp/autograder_utils

ADD e2e/source/run_autograder /autograder/run_autograder
RUN chmod +x /autograder/run_autograder
ADD e2e/source /autograder/source

WORKDIR /autograder

ENTRYPOINT [ "/autograder/run_autograder" ]
