import "classes/*.pp"

Exec {
  path => "/usr/local/bin:/usr/bin:/usr/sbin:/sbin:/bin",
}

class dev {
  class {
    init: ;
    memcached: ;
    locales: ;
  }
  class { "versioning":
    require => [Class[init], Class[locales]],
  }
  class { "postsql":
    require => Class[versioning],
    username => $username,
    password => $password,
    project_name => $project_name;
  }
  class { "python":
    require => Class[postsql],
    project_path => $project_path;
  }
  class { "nginx":
    require => Class[python],
    server_name => $server_name,
    project_name => $project_name,
    project_path => $project_path;
  }
  class { "application":
    require => Class[nginx],
    project_path => $project_path,
    project_name => $project_name,
  }
  class { "procfile":
    require => Class[application],
    project_name => $project_name,
    project_path => $project_path;
  }
  class { "custom":
    require => Class[procfile],
    project_path => $project_path,
    project_name => $project_name;
  }
}

include dev
