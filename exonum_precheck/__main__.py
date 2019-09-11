import argparse

from exonum_precheck import run_check

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="exonum_precheck", description="Exonum deployment precheck script")
    parser.add_argument('--jobs', nargs='*', default=['unit-test', 'lints'])
    args = parser.parse_args()
    run_check(args)
