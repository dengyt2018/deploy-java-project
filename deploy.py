#!/usr/bin/env python3

from pathlib import Path
import yaml
import xml.etree.ElementTree
import ansible_runner
import sys

pompath = Path("../pom.xml")

project_path = pompath.resolve().parent

with open(pompath, "r") as f:
    data = xml.etree.ElementTree.parse(f)

root = data.getroot()


def get_jarfile(r):
    for x in r:
        v = x.text if str(x.tag).endswith("version") else None
        n = x.text if str(x.tag).endswith("name") else None
        d = x.text if str(x.tag).endswith("description") else None
        if v:
            vv = v
        if n:
            nn = n
        if d:
            dd = d
    return nn, vv.strip(), dd


name, version, description = get_jarfile(root)
target_name = "{}-{}.jar".format(name, version)

extravars = {
    "hosts_name": "rockymark",  # ansible hosts name which one or group to deploy
    "project_port": "9080/tcp", # PORT-PORT/PROTOCOL for port ranges.
    "project_path": str(project_path),  # pom.xml path
    "dest_path": "/root/jartest",       # deploy on dest server path
    "jarfile": "{}.jar".format(name),   # deploy on dest server file name
    "target_name": target_name, # maven package name
    "project_name": name,       # pom.xml name
    "description": description  # pom.xml description
}

def load_config_yaml():
    config_yaml_file = Path("config.yaml").resolve().absolute()
    with open(config_yaml_file, 'r', encoding='UTF-8') as f:
        config_yaml = yaml.load(f, Loader=yaml.FullLoader)

    if config_yaml:
        for k,v in config_yaml.items():
            extravars[k] = v
            if "user_name".__eq__(k):
                extravars["systemd_user"]  = "User={}".format(v)
            if "group_name".__eq__(k):
                extravars["systemd_group"] = "Group={}".format(v)

def simple_parser_argv():
    argvs = sys.argv[1:]
    for idx, x in enumerate(argvs):
        if x.endswith(".yaml"):
            playbook = str(Path(x).resolve().absolute())
            argvs.pop(idx)
            return playbook, ' '.join(argvs)
    
    return 'complete.yaml', ' '.join(argvs)


def runner(extravars):
    extravars = '{}'.format(' '.join(["{}={}".format(x, y) for x, y in extravars.items()]))
    playbook, argvs = simple_parser_argv()
    cmdline = [playbook,
                '-e',
                extravars,
                argvs]

    ansible_runner.run_command(
        executable_cmd="ansible-playbook",
        cmdline_args=cmdline,
        input_fd=sys.stdin,
        output_fd=sys.stdout,
        error_fd=sys.stderr
        )
    
if __name__ == "__main__":
    load_config_yaml()
    runner(extravars)