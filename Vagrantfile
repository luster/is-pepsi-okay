# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"

  # ubuntu dist
  config.vm.box = "precise32"

  # share folder
  config.vm.synced_folder ".", "/home/vagrant/is-pepsi-okay/"

  # install requirements
  config.vm.provision "shell", path: "bootstrap.sh"

  # newtork
  config.vm.network :private_network, ip: "33.33.33.33"

  # forward ports
  #config.vm.network :forwarded_port, guest: 3306, host: 33066
  #config.vm.network :forwarded_port, guest: 80, host: 8080
  #config.vm.network :forwarded_port, guest: 443, host: 4403

end
