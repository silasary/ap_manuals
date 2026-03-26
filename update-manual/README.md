# Update Manual Github Action

A simple GHA that updates the base manual version.

## Usage

Slap this file in your `.github/workflows/` folder as `update_manual.yaml`.  Change the name of the subdirectory in the Update Manual step to match your repo layout.

```yaml
on:
    workflow_dispatch:  # Gives you a button you can press
    schedule:
      - cron: 0 0 1 * * # Runs at 00:00 on the first day of every month


jobs:
  update:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Update manual
        uses: silasary/ap_manuals/update-manual@main
        with:
          allow_unstable: 'true'
          directory: <Name of the folder your manual lives in>

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v7
        with:
          title: Update manual to latest version
          branch: update-manual
          labels: automated-pr
```

Note:  To use "Create Pull Request", you mujst turn on "Allow GitHub Actions to create and approve pull requests" in your repo settings.  Settings -> Actions -> General -> Scroll all the way to the bottom.

## What does it do?

It does two things:
* Outright replaces all the python files in the root directory.  These are the core manual files that you should probably never be editing anyway.
* Goes through each python file in the hooks directory, and adds any functions in the latest manual that are not defined in your existing files.
  * It will not change existing hooks, even if the signatures do not match.  Always read the release notes.
* It will never touch json files.

