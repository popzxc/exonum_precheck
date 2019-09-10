import subprocess
import os
import yaml


def _cyan(message):
    return "\033[96m {}\033[00m".format(message)


def _red(message):
    return "\033[91m {}\033[00m".format(message)


def _green(message):
    return "\033[92m {}\033[00m".format(message)


def _yellow(message):
    return "\033[93m {}\033[00m" .format(message)


def _warning(message):
    return _yellow("Warning: ") + message


def _ok(message):
    return _green("Success: ") + message


def _err(message):
    return _red("Error: ") + message


def _info(message):
    return _cyan(message)


def _run_command(command):
    arguments = command.split()
    result = subprocess.call(arguments)

    if result == 0:
        msg = _ok(command)
    else:
        msg = _err(command)

    return (result, msg)


def verify_rustc_version(expected):
    proc = subprocess.Popen(["rustc", "--version"], stdout=subprocess.PIPE)
    outs, errs = proc.communicate()
    # Expected output format is "rustc 1.37.0 (eae3437df 2019-08-13)"
    return str(outs, 'utf-8').split()[1] == expected


def run_check():
    config = load_travis_config()
    expected_rust_version = config["rust"][0]

    if not verify_rustc_version(expected_rust_version):
        print(_warning("Local ruscts differs from one in .travis.yml"))

    jobs = config["jobs"]["include"]
    test_commands = []
    lints_commands = []
    for job in jobs:
        if job["name"] == "unit-test":
            test_commands = job["script"]
        elif job["name"] == "lints":
            lints_commands = job["script"]

    test_results = [_run_command(command) for command in test_commands]
    lints_results = [_run_command(command) for command in lints_commands]

    print(_info("Tests results:"))
    for _, result in test_results:
        print(result)

    print(_info("Lints results:"))
    for _, result in lints_results:
        print(result)

    overall_success = all([lambda x: x[0] == 0 for x in test_results + lints_results])
    if overall_success:
        # Success exit code.
        exit(0)
    else:
        # Error exit code.
        exit(1)


def load_travis_config():
    try:
        with open(".travis.yml", "r") as file:
            return yaml.load(file)
    except FileNotFoundError:
        print(_red("Not an exonum root directory, aborting"))
