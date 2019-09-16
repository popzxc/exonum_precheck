import subprocess
import os
import yaml
import sys


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


def run_check(args):
    scheduled_jobs = args.jobs
    config = load_travis_config()
    expected_rust_version = config["rust"][0]

    if not verify_rustc_version(expected_rust_version):
        print(_warning("Local ruscts differs from one in .travis.yml"))

    jobs = config["jobs"]["include"]

    # Initialize jobs to run.
    commands = dict()
    for scheduled_job in scheduled_jobs:
        commands[scheduled_job] = []

    for job in jobs:
        if job["name"] in scheduled_jobs:
            commands[job["name"]] = job["script"]

    # Run everything and collect results.
    results = dict()
    overall_success = True

    for scheduled_job in scheduled_jobs:
        results[scheduled_job] = [_run_command(command) for command in commands[scheduled_job]]

        overall_success = overall_success and all(map(lambda x: x[0] == 0, results[scheduled_job]))

    # Print output for every job.
    for scheduled_job in scheduled_jobs:
        print(_info(f"{scheduled_job} results:"))
        for _, result in results[scheduled_job]:
            print(result)

        print("")

    if overall_success:
        # Success exit code.
        print(_ok("Exiting successfully"))
        sys.exit(0)
    else:
        # Error exit code.
        print(_err("Exiting with an error"))
        sys.exit(1)


def load_travis_config():
    try:
        with open(".travis.yml", "r") as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    except FileNotFoundError:
        print(_red("Not an exonum root directory, aborting"))
