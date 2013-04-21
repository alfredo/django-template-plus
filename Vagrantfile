require "yaml"

# Load up our vagrant config files -- vagrantconfig.yaml
_config = YAML.load(File.open(File.join(File.dirname(__FILE__), "vagrantconfig.yaml"), File::RDONLY).read)

CONF = _config
MOUNT_POINT = CONF['mount_point']


Vagrant.configure("2") do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  if CONF['gui'] == true
    config.vm.boot_mode = :gui
  end

  config.ssh.max_tries = 50
  config.ssh.timeout   = 300

  # Virtualbox has issues with a large amount of shared files,
  # So it is recommended to be mounted as NFS
  config.vm.provider :virtualbox do |vb|
    if CONF['nfs'] == false or RUBY_PLATFORM =~ /mswin(32|64)/
      config.vm.synced_folder ".", MOUNT_POINT, id: "vagrant-root"
    else
      config.vm.synced_folder ".", MOUNT_POINT, :nfs => true, id: "vagrant-root"
    end
  end

  config.vm.provider :vmware_fusion do |vb|
    config.vm.synced_folder ".", MOUNT_POINT, id: "vagrant-root"
    vb.vmx["memsize"] = "512"
    vb.vmx["numvcpus"] = "1"
    vb.vmx["displayName"] = CONF['server_name']
    vb.vmx["annotation"] = CONF['server_name']
  end


  # Add to /etc/hosts
  config.vm.network :private_network, ip: CONF['server_ip']
  config.vm.network :forwarded_port, guest: 80, host: 8000

  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/manifests"
    puppet.module_path = "puppet/modules"
    puppet.manifest_file  = "vagrant.pp"
    if CONF['debug'] == true
      puppet.options = "--verbose --debug"
    end
    puppet.facter = [
                     ['username', CONF['username']],
                     ['password', CONF['password']],
                     ['project_path', MOUNT_POINT],
                     ['project_name', CONF['project_name']],
                     ['server_name', CONF['server_name']],
                    ]
  end
end
