#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1.1
# Copyright (C) 2018-2020 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: idrac_reset
short_description: Reset iDRAC.
version_added: "2.9.11"
description:
    - This module resets iDRAC.
    - "iDRAC is not accessible for some time after running this module. It is recommended to wait for some time,
    before trying to connect to iDRAC."
options:
    idrac_ip:
        required: True
        type: str
        description: iDRAC IP Address.
    idrac_user:
        required: True
        type: str
        description: iDRAC username.
    idrac_password:
        required: True
        type: str
        description: iDRAC user password.
        aliases: ['idrac_pwd']
    idrac_port:
        required: False
        type: int
        description: iDRAC port.
        default: 443

requirements:
    - "omsdk"
    - "python >= 2.7.5"
author:
  - "Felix Stephen (@felixs88)"
  - "Anooja Vardhineni (@anooja-vardhineni)"
"""

EXAMPLES = """
---
- name: Reset iDRAC
  idrac_reset:
       idrac_ip: "192.168.0.1"
       idrac_user: "user_name"
       idrac_password: "user_password"
       idrac_port: 443
"""

RETURNS = """
msg:
    description: iDRAC reset operation status.
    returned: always
    type: dict
    sample: {
        "idracreset": {
            "Data": {
                "StatusCode": 204
            },
            "Message": "none",
            "Status": "Success",
            "StatusCode": 204,
            "retval": true
        }
    }
error_info:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
      "code": "Base.1.0.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information.",
      "@Message.ExtendedInfo": [
        {
          "MessageId": "GEN1234",
          "RelatedProperties": [],
          "Message": "Unable to process the request because an error occurred.",
          "MessageArgs": [],
          "Severity": "Critical",
          "Resolution": "Retry the operation. If the issue persists, contact your system administrator."
        }
      ]
    }
  }
"""


import json
from ansible.module_utils.remote_management.dellemc.dellemc_idrac import iDRACConnection
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import open_url, ConnectionError, SSLValidationError


def run_idrac_reset(idrac, module):
    if module.check_mode:
        msg = {'Status': 'Success', 'Message': 'Changes found to commit!', 'changes_applicable': True}
    else:
        idrac.use_redfish = True
        msg = idrac.config_mgr.reset_idrac()
    return msg


def main():
    module = AnsibleModule(
        argument_spec={
            "idrac_ip": {"required": True, "type": 'str'},
            "idrac_user": {"required": True, "type": 'str'},
            "idrac_password": {"required": True, "type": 'str', "aliases": ['idrac_pwd'], "no_log": True},
            "idrac_port": {"required": False, "default": 443, "type": 'int'}
        },
        supports_check_mode=True)

    try:
        with iDRACConnection(module.params) as idrac:
            msg = run_idrac_reset(idrac, module)
    except HTTPError as err:
        module.fail_json(msg=str(err), error_info=json.load(err))
    except URLError as err:
        module.exit_json(msg=str(err), unreachable=True)
    except (RuntimeError, SSLValidationError, ConnectionError, KeyError,
            ImportError, ValueError, TypeError) as e:
        module.fail_json(msg=str(e))
    module.exit_json(msg=msg)


if __name__ == '__main__':
    main()
