#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, Marco Noce <marco.X0178421@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: pkginfo_facts
author:
    - Marco Noce (@NomakCooper)
description:
    - Gathers facts about Solaris pkg info attributes for a specific pkg by "pkginfo" on Solaris 10 and "pkg info" on Solaris 11.
    - This module currently supports SunOS Family, Oracle Solaris 10/11.
requirements:
  - pkginfo
  - pkg
short_description: Gathers facts about Solaris pkg info attributes for a specific pkg.
notes:
  - |
    This module shows the list of attributes of Solaris pkg.
options:
    pkgname:
        description:
            - The pkg name.
        required: true
        type: str
    alias:
        description:
            - Pkg alias, a name of your choice which will then be automatically assigned to the dict object name.
        required: true
        type: str
'''

EXAMPLES = r'''
- name: gather facts of sendmail pkg on Solaris 11
  pkginfo_facts:
    pkgname: "service/network/smtp/sendmail"
    alias: sendmail

- name: set fact for print
  set_fact:
    sendmail_state: "{{ ansible_facts.sendmail_pkg| map(attribute='State') | first }}"
    sendmail_version: "{{ ansible_facts.sendmail_pkg| map(attribute='Version') | first }}"

- name: print sendmail pkg state and version
  debug:
    msg: "sendmail pkg is {{sendmail_state}}. Version : {{sendmail_version}} "

- name: gather facts of SUNWzoneu pkg on Solaris 10
  pkginfo_facts:
    pkgname: "SUNWzoneu"
    alias: zone

- name: set fact for print
  set_fact:
    zone_status: "{{ ansible_facts.zone_pkg| map(attribute='STATUS') | first }}"
    zone_version: "{{ ansible_facts.zone_pkg| map(attribute='VERSION') | first }}"

- name: print SUNWzoneu pkg status and version
  debug:
    msg: "zone pkg is {{zone_status}}. Version : {{zone_version}} "
'''

RETURN = r'''
ansible_facts:
  description: Dictionary containing the attribute of SMF service
  returned: always
  type: complex
  contains:
    alias_pkg:
      description: A list of attribute of specific Solaris pkg. ( the list name is created from the alias entered as a parameter )
      note: The List attributes depend on the Solaris Major Release.
      returned: always
      type: list
      contains:
        CATEGORY:
          description: The pkg category.
          returned: if Solaris 10.x
          type: str
          sample: "system"
        STATUS:
          description: The pkg installation status
          returned: if Solaris 10.x
          type: str
          sample: "completely installed"
        VENDOR:
          description: The pkg vendor
          returned: if Solaris 10.x
          type: str
          sample: "Oracle Corporation"
        NAME:
          description: The pkg extended name.
          returned: if Solaris 10.x
          type: str
          sample: "Solaris Zones (Usr)"
        PKGINST:
          description: The installed pkg name
          returned: if Solaris 10.x
          type: str
          sample: "SUNWzoneu"
        BASEDIR:
          description: The pkg base directory.
          returned: if Solaris 10.x
          type: str
          sample: "/"
        VERSION:
          description: The pkg version.
          returned: if Solaris 10.x
          type: str
          sample: "11.10.0,REV=2005.01.21.15.53"
        HOTLINE:
          description: The pkg hotline
          returned: if Solaris 10.x
          type: str
          sample: "Please contact your local service provider"
        INSTDATE:
          description: The pkg installation date and time.
          returned: if Solaris 10.x
          type: str
          sample: "Aug 05 2016 18:57"
        PSTAMP:
          description: The pkg production stamp.
          returned: if Solaris 10.x
          type: str
          sample: "on10-patch20131219093000"
        ARCH:
          description: The pkg architecture supported.
          returned: if Solaris 10.x
          type: str
          sample: "sparc"
        DESC:
          description: The pkg short description.
          returned: if Solaris 10.x
          type: str
          sample: "Solaris Zones Configuration and Administration"
        Name:
          description: The pkg name.
          returned: if Solaris 11.x
          type: str
          sample: "service/network/smtp/sendmail"
        Summary:
          description: The pkg summary.
          returned: if Solaris 11.x
          type: str
          sample: "Sendmail utilities"
        Category:
          description: The pkg category.
          returned: if Solaris 11.x
          type: str
          sample: "System/Core"
        State:
          description: The pkg installation state.
          returned: if Solaris 11.x
          type: str
          sample: "Installed"
        Publisher:
          description: The pkg publisher.
          returned: if Solaris 11.x
          type: str
          sample: "solaris"
        Version:
          description: The pkg version.
          returned: if Solaris 11.x
          type: str
          sample: "8.15.2"
        Branch:
          description: The pkg branch.
          returned: if Solaris 11.x
          type: str
          sample: "11.4.42.0.0.111.0"
        Packaging Date:
          description: The pkg Date.
          returned: if Solaris 11.x
          type: str
          sample: "December  3, 2021 at  8:56:48 PM"
        Last Install Time:
          description: The pkg last install date and time.
          returned: if Solaris 11.x
          type: str
          sample: "December  4, 2021 at  6:34:57 AM"
        Size:
          description: The pkg size.
          returned: if Solaris 11.x
          type: str
          sample: "2.93 MB"
        FMRI:
          description: The pkg FMRI.
          returned: if Solaris 11.x
          type: str
          sample: "pkg://solaris/service/network/smtp/sendmail@8.15.2-11.4.42.0.0.111.0:20211203T205648Z"
        Project Contact:
          description: The pkg project contact.
          returned: if Solaris 11.x
          type: str
          sample: "Sendmail community"
        Project URL:
          description: The pkg project url.
          returned: if Solaris 11.x
          type: str
          sample: "http://www.sendmail.org/"
'''

import platform
from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.basic import AnsibleModule


def pkg11_parse(raw):

    results = list()

    lines = raw.splitlines()
    for line in lines:
        cells = line.partition(":")
        param, dot, value = cells
        if param.strip().startswith("Description") or dot == "":
            result = {}
        else:
            result = {
                    param.strip(): value.strip(),
                }

        results.append(result)

    return results

def pkg10_parse(raw):

    results = list()

    lines = raw.splitlines()
    for line in lines:
        cells = line.partition(":")
        param, dot, value = cells
        if param.strip().startswith("FILES") or dot == "":
            result = {}
        else:
            result = {
                    param.strip(): value.strip(),
                }

        results.append(result)

    return results

def main():
    module = AnsibleModule(
        argument_spec=dict(
            pkgname=dict(type='str', required=True),
            alias=dict(type='str', required=True),
        ),
        supports_check_mode=True,
    )

    pkg = module.params['pkgname']
    dictname = module.params['alias']

    if platform.release() == '5.10':
        command_args = ['-l', pkg]
        commands_map = {
            'pkginfo': {
                'args': [],
                'parse_func': pkg10_parse
            },
        }
        commands_map['pkginfo']['args'] = command_args

    if platform.release() == '5.11':
        command_args = ['info', pkg]
        commands_map = {
            'pkg': {
                'args': [],
                'parse_func': pkg11_parse
            },
        }
        commands_map['pkg']['args'] = command_args

    if platform.system() != 'SunOS':
        module.fail_json(msg='This module requires SunOS.')

    result = {
        'changed': False,
        'ansible_facts': {
            dictname + '_pkg': [],
        },
    }

    try:
        command = None
        bin_path = None
        for c in sorted(commands_map):
            bin_path = module.get_bin_path(c, required=False)
            if bin_path is not None:
                command = c
                break

        if bin_path is None:
            raise EnvironmentError(msg='Unable to find any of the supported commands in PATH: {0}'.format(", ".join(sorted(commands_map))))


        args = commands_map[command]['args']
        rc, stdout, stderr = module.run_command([bin_path] + args)
        if rc == 0:
            parse_func = commands_map[command]['parse_func']
            results = parse_func(stdout)

            # time to merge
            merged = {}

            for pkginfodict in results:
              for k, v in pkginfodict.items():
                    join = {

                        k: v,

                    }
                    merged.update(join)

            result['ansible_facts'][dictname + '_pkg'].append(merged)
    except (KeyError, EnvironmentError) as e:
        module.fail_json(msg=to_native(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
