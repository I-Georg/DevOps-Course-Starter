
Vagrant.configure("2") do |config|
  
  config.vm.box = "hashicorp/bionic64"

   config.vm.network "forwarded_port", guest: 5000, host: 5000
 
  config.vm.provision "shell", privileged: false, inline: <<-SHELL    
  sudo apt-get update -y
  sudo apt-get upgrade -y  
 
  # TODO: Install pyenv prerequisites 
  sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git 

  
rm -rf ~/.pyenv
  # TODO: Install pyenv  
  
  git clone https://github.com/pyenv/pyenv.git ~/.pyenv
  
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
  echo -e 'if command -v pyenv 1>/dev/null 2>&1; 
  pyenv install 3.8.3
  pyenv global  3.8.3
  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
  
  exec "$SHELL"
  
  SHELL

  config.trigger.after :up do |trigger|   
     trigger.name = "Launching App"    
     trigger.info = "Running the TODO app setup script"    
     
   trigger.run_remote = {privileged: false,name:"SCRIIPT", inline: "  
   
   
  
   sudo apt-get install -y python3-pip
  
   sudo pip3 install --upgrade keyrings.alt 
   sudo pip3 install -U pip
   sudo pip install ansicolors
   sudo python3 -m pip install poetry
   sudo poetry --version
    cd /vagrant  
   #install poetry and run app
   poetry install
   poetry run flask run --host=0.0.0.0
 

   
   "}
  end
end
