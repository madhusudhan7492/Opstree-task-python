pipeline {
  agent any
  stages {
    stage('Checkout SCM') {
      steps {
        checkout([$class: 'GitSCM', branches: [
          [name: '*/master']
        ], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [
          [credentialsId: 'Github_creds', url: 'https://github.com/madhusudhan7492/Opstree-task-python.git']
        ]])
      }
    }

    stage('Run Start and Change Instance Type script') {
      steps {

        withCredentials([
          [$class: 'UsernamePasswordMultiBinding', credentialsId: 'aws-creds', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY']
        ]) {
          sh '/usr/bin/python3 -u startAndChangeInstance.py'
        }

      }
    }

    stage('Run ansible playbook') {
      steps {
        //here main.yml file is in the cloned repository
        ansiblePlaybook credentialsId: 'ansadmin', disableHostKeyChecking: true, installation: 'ansible', playbook: 'main.yml'
      }
    }

     stage('Run flipback and start instance script') {
      steps {

        withCredentials([
          [$class: 'UsernamePasswordMultiBinding', credentialsId: 'aws-creds', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY']
        ]) {
          sh '/usr/bin/python3 -u flipbackAndStartInstance.py'
        }

      }
    }

  }
}