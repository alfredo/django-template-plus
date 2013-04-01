class procfile ($project_path, $project_name) {
  package { 'foreman':
    ensure   => 'installed',
    provider => 'gem',
  }

  exec { 'force-upstart':
    cwd => "/etc/init",
    command => "rm -rf /etc/init/$project_name*",
    require => Package['foreman'],
  }

  exec { 'install-upstart':
    cwd => "$project_path",
    command => "foreman export -a $project_name -p 8000 upstart /etc/init -u vagrant -f $project_path/Procfile.local",
    require => Exec['force-upstart'],
    path => ["/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/opt/vagrant_ruby/bin"],
  }

  service { $project_name:
    ensure => running,
    enable => true,
    provider => upstart,
    subscribe => [Package['foreman'], Exec['install-upstart']],
  }

}
