<meta name="author" content="Marco Noce">
<meta name="description" content="Gathers facts about Solaris pkg info attributes for a specific pkg by pkginfo on Solaris 10 and pkg info on Solaris 11.">
<meta name="copyright" content="Marco Noce 2024">
<meta name="keywords" content="ansible, module, solaris, pkg, pkginfo, attribute">

<div align="center">

![Ansible Custom Module][ansible-shield]
![Oracle Solaris][solaris-shield]
![python][python-shield]
![license][license-shield]

</div>


### pkginfo_facts ansible custom module
#### Gathers facts about Solaris pkg info attributes for a specific pkg.

#### Description :

<b>pkginfo_facts</b> is a custom module for ansible that creates an ansible_facts containing the attribute list of specific pkg on a SunOS/Oracle Solaris 10/11 host.

#### Repo files:

```
├── /library                
│   └── pkginfo_facts.py     ##<-- python custom module
├── sol10_pkg.yml            ##<-- ansible playbook example for Solaris 10 release
└── sol11_pkg.yml            ##<-- ansible playbook example for Solaris 11 release
```

#### Requirements :

*  This module supports SunOS/Oracle Solaris 10/11 only
*  The pkg info are gathered from the [pkginfo] "-l" command on Solaris 10.x
*  The pkg info are gathered from the [pkg] command on Solaris 11.x


#### Parameters :

|Parameter|Type  |Required|Sample                      |Comment                                                                                                                 |
|---------|------|--------|----------------------------|------------------------------------------------------------------------------------------------------------------------|
|pkgname  |string|True    |"SUNWzoneu" ( Solaris 10.x ) "service/network/smtp/sendmail" ( Solaris 11.x ) | The pkg name                                                         |
|alias    |string|True    |"sendmail"                  |Pkg alias, a name of your choice which will then be automatically assigned to the dict object name ( sendmail_pkg )     |

#### Attributes :

|Attribute |Support|Description                                                                         |
|----------|-------|------------------------------------------------------------------------------------|
|check_mode|full   |Can run in check_mode and return changed status prediction without modifying target.|
|facts     |full   |Action returns an ansible_facts dictionary that will update existing host facts.    |

#### Examples :

#### Solaris 10.x Tasks
```yaml
---
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
```
#### Solaris 11.x Tasks
```yaml
---
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
```
#### Solaris 10.x 'alias'_pkg facts:
```json
  "ansible_facts": {
    "zone_pkg": [
      {
        "CATEGORY": "system",
        "STATUS": "completely installed",
        "VENDOR": "Oracle Corporation",
        "NAME": "Solaris Zones (Usr)",
        "PKGINST": "SUNWzoneu",
        "BASEDIR": "/",
        "VERSION": "11.10.0,REV=2005.01.21.15.53",
        "HOTLINE": "Please contact your local service provider",
        "INSTDATE": "Aug 05 2016 18:57",
        "PSTAMP": "on10-patch20131219093000",
        "ARCH": "sparc",
        "DESC": "Solaris Zones Configuration and Administration"
      }
    ]
  },
```
#### Solaris 11.x 'alias'_pkg facts:
```json
  "ansible_facts": {
    "sendmail_pkg": [
      {
        "Name": "service/network/smtp/sendmail",
        "Summary": "Sendmail utilities",
        "Category": "System/Core",
        "State": "Installed",
        "Publisher": "solaris",
        "Version": "8.15.2",
        "Branch": "11.4.42.0.0.111.0",
        "Packaging Date": "December  3, 2021 at  8:56:48 PM",
        "Last Install Time": "December  4, 2021 at  6:34:57 AM",
        "Size": "2.93 MB",
        "FMRI": "pkg://solaris/service/network/smtp/sendmail@8.15.2-11.4.42.0.0.111.0:20211203T205648Z",
        "Project Contact": "Sendmail community",
        "Project URL": "http://www.sendmail.org/"
      }
    ]
  },
```
#### debug output from example :
```
TASK [print SUNWzoneu pkg status and version] *****************************************
ok: [sol10host] => {
    "msg": "zone pkg is completely installed. Version : 11.10.0,REV=2005.01.21.15.53 "
}
```
```
TASK [print sendmail pkg state and version] *****************************************
ok: [sol11host] => {
    "msg": "sendmail pkg is Installed. Version : 8.15.2 "
}
```
#### Returned Facts :

*  Facts returned by this module are added/updated in the hostvars host facts and can be referenced by name just like any other host fact. They do not need to be registered in order to use them.
*  Attributes change according to the Solaris Major Release and pkg selected.

|Key              |Type                  |Description                        |Returned       |Sample                                                                                 |
|-----------------|----------------------|-----------------------------------|---------------|---------------------------------------------------------------------------------------|
|'alias'_pkg      |list / elements=string|Pkg attribute list.                |               |                                                                                       |
|CATEGORY         |string                |The pkg category.                  |if Solaris 10.x|"system"                                                                               |
|STATUS           |string                |The pkg installation status.       |if Solaris 10.x|"completely installed"                                                                 |
|VENDOR           |string                |The pkg vendor                     |if Solaris 10.x|"Oracle Corporation"                                                                   |
|NAME             |string                |The pkg extended name.             |if Solaris 10.x|"Solaris Zones (Usr)"                                                                  |
|PKGINST          |string                |The installed pkg name             |if Solaris 10.x|"SUNWzoneu"                                                                            |
|BASEDIR          |string                |The pkg base directory.            |if Solaris 10.x|"/"                                                                                    |
|VERSION          |string                |The pkg version.                   |if Solaris 10.x|"11.10.0,REV=2005.01.21.15.53"                                                         |
|HOTLINE          |string                |The pkg hotline.                   |if Solaris 10.x|"Please contact your local service provider"                                           |
|INSTDATE         |string                |The pkg installation date and time.|if Solaris 10.x|"Aug 05 2016 18:57"                                                                    |
|PSTAMP           |string                |The pkg production stamp.          |if Solaris 10.x|"on10-patch20131219093000"                                                             |
|ARCH             |string                |The pkg architecture supported.    |if Solaris 10.x|"sparc"                                                                                |
|DESC             |string                |The pkg short description.         |if Solaris 10.x|"Solaris Zones Configuration and Administration"                                       |
|Name             |string                |The pkg name.                      |if Solaris 11.x|"service/network/smtp/sendmail"                                                        |
|Summary          |string                |The pkg summary.                   |if Solaris 11.x|"Sendmail utilities"                                                                   |
|Category         |string                |The pkg category.                  |if Solaris 11.x|"System/Core"                                                                          |
|State            |string                |The pkg installation state.        |if Solaris 11.x|"Installed"                                                                            |
|Publisher        |string                |The pkg publisher.                 |if Solaris 11.x|"solaris"                                                                              |
|Version          |string                |The pkg version.                   |if Solaris 11.x|"8.15.2"                                                                               |
|Branch           |string                |The pkg branch.                    |if Solaris 11.x|"11.4.42.0.0.111.0"                                                                    |
|Packaging Date   |string                |The pkg Date.                      |if Solaris 11.x|"December  3, 2021 at  8:56:48 PM"                                                     |
|Last Install Time|string                |The pkg last install date and time.|if Solaris 11.x|"December  4, 2021 at  6:34:57 AM"                                                     |
|Size             |string                |The pkg size.                      |if Solaris 11.x|"2.93 MB"                                                                              |
|FMRI             |string                |The pkg FMRI.                      |if Solaris 11.x|"pkg://solaris/service/network/smtp/sendmail@8.15.2-11.4.42.0.0.111.0:20211203T205648Z"|
|Project Contact  |string                |The pkg project contact.           |if Solaris 11.x|"Sendmail community"                                                                   |
|Project URL      |string                |The pkg project url.               |if Solaris 11.x|"http://www.sendmail.org/"                                                             |

## SANITY TEST

* Ansible sanity test is available in [SANITY.md] file

## Integration

1. Assuming you are in the root folder of your ansible project.

Specify a module path in your ansible configuration file.

```shell
$ vim ansible.cfg
```
```ini
[defaults]
...
library = ./library
...
```

Create the directory and copy the python modules into that directory

```shell
$ mkdir library
$ cp path/to/module library
```

2. If you use Ansible AWX and have no way to edit the control node, you can add the /library directory to the same directory as the playbook .yml file

```
├── root repository
│   ├── playbooks
│   │    ├── /library                
│   │    │   └── pkginfo_facts.py        ##<-- python custom module
│   │    └── your_playbook.yml           ##<-- you playbook
```   

[ansible-shield]: https://img.shields.io/badge/Ansible-custom%20module-blue?style=for-the-badge&logo=ansible&logoColor=lightgrey
[solaris-shield]: https://img.shields.io/badge/oracle-solaris-red?style=for-the-badge&logo=oracle&logoColor=red
[python-shield]: https://img.shields.io/badge/python-blue?style=for-the-badge&logo=python&logoColor=yellow
[license-shield]: https://img.shields.io/github/license/nomakcooper/svcs_attr_facts?style=for-the-badge&label=LICENSE


[pkginfo]: https://docs.oracle.com/cd/E19455-01/805-6338/ch4verifypkg-36/index.html
[pkg]: https://docs.oracle.com/cd/E23824_01/html/821-1451/gkunu.html#:~:text=The%20pkg%20info%20command%20displays,installed%20in%20the%20current%20image.
[SANITY.md]: SANITY.md
