import subprocess


def _cyan(message):
    return "\033[96m {}\033[00m".format(message)


def _red(message):
    return "\033[91m {}\033[00m".format(message)


def _green(message):
    return "\033[92m {}\033[00m".format(message)


def _run_command(command):
    arguments = command.split()
    result = subprocess.call(arguments)

    msg = f"{command}: "
    if result == 0:
        msg += _green("passed")
    else:
        msg += _red("failed")

    return msg


def run_tests():
    """ Runs all the tests. """
    print(_cyan("Running tests:"))

    results = []

    commands = [
        "cargo test",
        "cargo run -p exonum --example explorer",
        "cargo run -p exonum-testkit --example timestamping",
        "cargo run -p exonum-time --example simple_service"
    ]

    return [_run_command(command) for command in commands]


def run_lints():
    """ Runs all the lints. """
    print(_cyan("Running lints:"))

    results = []

    results.append(_run_command("npm run cspell"))
    results.append(_run_command("npm run md"))

    # Clippy lints.
    results.append(_run_command('cargo clippy --all --benches --features "long_benchmarks"'))

    # Other cargo lints.
    results.append(_run_command("cargo fmt --all -- --check"))
    subprocess.call("cargo clean --doc".split())
    results.append(_run_command("cargo doc --no-deps"))

    # Temporary hack to ignore warnings about missing pages.
    subprocess.call("mkdir -p target/doc/exonum_configuration".split())
    subprocess.call("mkdir -p target/std/string".split())
    subprocess.call("touch target/std/string/struct.String.html".split())
    subprocess.call("touch target/std/primitive.usize.html".split())
    subprocess.call("touch target/doc/enum.HashTag.html".split())

    results.append(_run_command("cargo deadlinks --dir target/doc"))

    return results


def run_check():
    """ Runs the tests and lints. """
    print(_cyan("Exonum precheck"))

    test_results = run_tests()
    lints_results = run_lints()

    print(_cyan("Overall results:"))

    print(_cyan("Test:"))
    for result in test_results:
        print(result)

    print(_cyan("Lints:"))
    for result in lints_results:
        print(result)
