pipeline {
    agent any
    stages {
        stage('Checkout SCM') {
      steps {
        checkout([$class: 'GitSCM', branches: [
          [name: '*/master']
        ], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [
          [credentialsId: 'Github_creds', url: 'https://github.com/madhusudhan7492/Opstree-task.git']
        ]])
      }
    }

        stage('Run Python script') {
            steps {
                withAWS(credentials: 'aws-creds', region: 'us-east-1') {
                    sh '/usr/bin/python3 script.py'
                }
            }
        }
    }
}