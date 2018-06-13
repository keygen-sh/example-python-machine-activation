# Example Machine Activation

This is an example of a typical machine activation flow written in Python.
You may of course choose to implement a different flow if required - this
only serves as an example implementation.

## Running the example

First up, configure a few environment variables:

```bash
# A Keygen activation token for the given license. You can generate an
# activation token per-license via the API or your admin dashboard.
export KEYGEN_ACTIVATION_TOKEN="A_KEYGEN_ACTIVATION_TOKEN"

# Your Keygen account ID. Find yours at https://app.keygen.sh/settings.
export KEYGEN_ACCOUNT_ID="YOUR_KEYGEN_ACCOUNT_ID"
```

You can either run each line above within your terminal session before
starting the app, or you can add the above contents to your `~/.bashrc`
file and then run `source ~/.bashrc` after saving the file.

Next, install dependencies with [`pip`](https://packaging.python.org/):

```
pip install -r requirements.txt
```

## Configuring a license policy

Visit [your dashboard](https://app.keygen.sh/policies) and create a new
policy with the following attributes:

```javascript
{
  requireFingerprintScope: true,
  maxMachines: 1,
  concurrent: false,
  floating: false,
  strict: true
}
```

## Creating an activation token

In order to allow the license to perform a machine activation, you will
need to create a new [activation token](https://keygen.sh/docs/api/#licenses-relationships-activation-tokens).
Activation tokens allow a limited number of machine activations for a
single license, which make them ideal for performing activations from
a client-side environment.

Alternatively, you could use authenticate as a user and use that token
to perform the activation, given the user has permission to manage the
current license.

And lastly, in server-side environments, you could utilize a product
token to authenticate API requests. Note: admin and product tokens
should never be used within client-side code, as they allow full
management of your Keygen account.

## Activating a machine

To perform a machine activation, run the script and supply a license key:

```
python main.py some-license-key-here
```

The script will use a SHA256 hash of your device's MAC address for the
machine's fingerprint.

## Questions?

Reach out at [support@keygen.sh](mailto:support@keygen.sh) if you have any
questions or concerns!
