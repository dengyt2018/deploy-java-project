
###### deploy jar file to server with jrebel

how set hosts see: <https://docs.ansible.com/ansible/latest/user_guide/intro_patterns.html>

hosts example: /etc/ansible/hosts

```conf
[localhost]
127.0.0.1 ansible_connection=local ansible_python_interpreter="{{ ansible_playbook_python }}"

[dev]
192.168.1.100
```

pip3 install --user ansible ansible-runner

`python3 deploy.py -K` run a full deploy

`python3 deploy.py -K [playbook name file].yaml` run step deploy

`python3 deploy.py upload.yaml -K` upload maven package jar file, jar file information come from pom.xml and restart service

`python3 deploy.py jrebel.yaml` upload JRebel and active JRebel

`python3 deploy.py firewalld -K` enable the port where the port come from config.yaml file

`config.yaml` define some variables

Download JRebel

```sh
cd roles/jrebel/tasks/files && curl -O https://dl.zeroturnaround.com/jrebel-stable-nosetup.zip
unzip jrebel-stable-nosetup.zip
cd -
```