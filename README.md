# Example Machine Activation

This is an example of a typical machine activation flow written in Python.
You may of course choose to implement a different flow if required - this
only serves as an example implementation.

## Running the example

First up, configure a few environment variables:

```bash
# Your Keygen account ID. Find yours at https://app.keygen.sh/settings.
export KEYGEN_ACCOUNT_ID="YOUR_KEYGEN_ACCOUNT_ID"
```

You can either run each line above within your terminal session before
starting the app, or you can add the above contents to your `~/.bashrc`
file and then run `source ~/.bashrc` after saving the file.

Next, install dependencies with [`pip`](https://packaging.python.org/):

```
python3 -m pip install -r requirements.txt
```

## Activating a machine

To perform a machine activation, run the script and supply a license key:

```
python3 main.py some-license-key-here
```

The script will use a SHA256 hash of your device's MAC address for the
machine's fingerprint.

## Questions?

Reach out at [support@keygen.sh](mailto:support@keygen.sh) if you have any
questions or concerns!
