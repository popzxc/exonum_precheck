# Exonum deployment precheck script

`exonum_precheck` is a script which verifies that all the expected checks are OK for code you're about to push.
It is supposed that you'll run this script before every push at the [Exonum](https://github.com/exonum/exonum) repository.

This command loads `.travis.yml` and performs all the checks (tests and lints) exactly as they will be performed on the CI server.
Also if installed rustc version doesn't match the one in the travis config, a warning will be shown.

## Prerequirements

You should have `clippy`, `rustfmt`, `deadlinks`, `cspell` and `md` installed:

```sh
cargo install cargo-deadlinks
rustup component add rustfmt
rustup component add clippy
npm install cspell
npm install md
```

## Example

```sh
cd exonum_folder
python3 -m exonum_precheck
```

Example output (actually it's colored):
```sh
 Tests results:
 Error: cargo test --all
 Success: cargo run -p exonum --example explorer
 Success: cargo run -p exonum-testkit --example timestamping
 Success: cargo run -p exonum-time --example simple_service
 Lints results:
 Success: npm run cspell
 Success: npm run md
 Success: cargo clippy --all --benches --features "long_benchmarks"
 Success: cargo fmt --all -- --check
 Success: cargo clean --doc
 Success: cargo doc --no-deps
 Success: mkdir -p target/doc/exonum_configuration
 Success: mkdir -p target/std/string
 Success: touch target/std/string/struct.String.html
 Success: touch target/std/primitive.usize.html
 Success: touch target/doc/enum.HashTag.html
 Success: cargo deadlinks --dir target/doc
```

You can also specify jobs to run manually.

```sh
python3 -m exonum_precheck --jobs linux-tests sample-job lints tests
```

Those jobs will be executed instead of default ones ("unit-test", "lints") in the provided order.

This maybe helpful if you want to use this script on another repository.

## Using as a git hook

This script can be also used as a prepush hook:
```sh
echo '#!/bin/sh\npython3 -m exonum_precheck || exit 1\n' > ./exonum_folder/.git/hooks/pre-push
chmod +x ./exonum_folder/.git/hooks/pre-push
```

With that hook you won't be able to push unless all the expected CI checks are passed.
However, be careful: if you're going to work on a work-in-progress branch which'll have broken tests, you'll have to temporary remove the hook.

Example of more advanced hook:

```sh
#!/bin/sh
npm install && git checkout package-lock.json package.json

export RUST_BACKTRACE=0
export RUST_LOG=off
export RUST_TEST_THREADS=4
export CARGO_BUILD_JOBS=4
ulimit -n 2048

python3 -m exonum_precheck || exit 1
```

## Installing

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

```
pip install -U exonum_precheck
```

## LICENSE

`exonum_precheck` is licensed under the MIT License.
See [LICENSE](LICENSE) for details.
