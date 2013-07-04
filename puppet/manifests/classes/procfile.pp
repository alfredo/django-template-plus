class procfile ($project_path, $project_name) {

  $packages = [
               'thor',
               'dotenv',
               'foreman',
               ]

  package { $packages:
    ensure => 'latest',
    provider => 'gem',
  }

  exec { 'install-upstart':
    cwd => "$project_path",
    command => "foreman export -a $project_name -p 8000 upstart /etc/init -u vagrant -f $project_path/Procfile.local",
    require => Package[$packages],
    creates => ['/etc/init/$project_name.conf'],
    environment => "HOME=/home/vagrant",
  }

  service { $project_name:
    ensure => running,
    enable => true,
    provider => upstart,
    subscribe => Exec['install-upstart'],
  }

}
