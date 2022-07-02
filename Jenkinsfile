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

    stage('Run python script') {
      steps {

        withCredentials([
          [$class: 'UsernamePasswordMultiBinding', credentialsId: 'aws-creds', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY']
        ]) {
          sh '/usr/bin/python3 main.py'
        }

      }
    }

  }
}