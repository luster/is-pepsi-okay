# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"

  # ubuntu dist
  config.vm.box = "virtualbox"
  config.vm.box_url = "https://vagrantcloud.com/ubuntu/trusty64/version/1/provider/virtualbox.box"

  # share folder
  config.vm.synced_folder ".", "/home/vagrant/is-pepsi-okay/"

  # install requirements
  config.vm.provision "shell", path: "bootstrap.sh"

  # newtork
  config.vm.network :private_network, ip: "33.33.33.33"

  # forward ports
  config.vm.network :forwarded_port, guest: 5000, host: 5000

  # gui for debug
  #config.vm.provider :virtualbox do |vb|
  #  vb.gui = true
  #end

end
