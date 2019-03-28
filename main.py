from uuid import getnode as get_mac
import requests
import json
import hashlib
import sys
import os

def activate_license(license_key):
  machine_fingerprint = hashlib.sha256(str(get_mac()).encode('utf-8')).hexdigest()
  validation = requests.post(
    "https://api.keygen.sh/v1/accounts/{}/licenses/actions/validate-key".format(os.environ['KEYGEN_ACCOUNT_ID']),
    headers={
      "Content-Type": "application/vnd.api+json",
      "Accept": "application/vnd.api+json"
    },
    data=json.dumps({
      "meta": {
        "scope": { "fingerprint": machine_fingerprint },
        "key": license_key
      }
    })
  ).json()

  if "errors" in validation:
    errs = validation["errors"]

    return False, "license validation failed: {}".format(
      map(lambda e: "{} - {}".format(e["title"], e["detail"]).lower(), errs)
    )

  # If the license is valid for the current machine, that means it has
  # already been activated. We can return early.
  if validation["meta"]["valid"]:
    return True, "license has already been activated on this machine"

  # Otherwise, we need to determine why the current license is not valid,
  # because in our case it may be invalid because another machine has
  # already been activated, or it may be invalid because it doesn't
  # have any activated machines associated with it yet and in that case
  # we'll need to activate one.
  #
  # NOTE: the "NO_MACHINE" status is unique to *node-locked* licenses. If
  #       you need to implement a floating license, you may also need to
  #       check for the "NO_MACHINES" status (note: plural) and also the
  #       "FINGERPRINT_SCOPE_MISMATCH" status.
  if validation["meta"]["constant"] != "NO_MACHINE":
    return False, "license {}".format(validation["meta"]["detail"])

  # If we've gotten this far, then our license has not been activated yet,
  # so we should go ahead and activate the current machine.
  activation = requests.post(
    "https://api.keygen.sh/v1/accounts/{}/machines".format(os.environ['KEYGEN_ACCOUNT_ID']),
    headers={
      "Authorization": "Bearer {}".format(os.environ['KEYGEN_ACTIVATION_TOKEN']),
      "Content-Type": "application/vnd.api+json",
      "Accept": "application/vnd.api+json"
    },
    data=json.dumps({
      "data": {
        "type": "machines",
        "attributes": {
          "fingerprint": machine_fingerprint
        },
        "relationships": {
          "license": {
            "data": { "type": "licenses", "id": validation["data"]["id"] }
          }
        }
      }
    })
  ).json()

  # If we get back an error, our activation failed.
  if "errors" in activation:
    errs = activation["errors"]

    return False, "license activation failed: {}".format(
      map(lambda e: "{} - {}".format(e["title"], e["detail"]).lower(), errs)
    )

  return True, "license activated"

# Run from the command line:
#   python main.py some_license_key
status, msg = activate_license(sys.argv[1])

print(status, msg)
