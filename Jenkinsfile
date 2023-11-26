pipeline {
  agent any
  stages {
    stage('Pull from Github') {
      steps {
        git(url: 'https://github.com/piotrsuchy/jenkins-ci-results-website', branch: 'main')
      }
    }

    stage('Restart ci_monitor_tool service') {
      steps {
        sh '''#!/bin/bash

echo "Trying to restart a service ci_monitor_tool.service"
./home/piotr/jenkins-ci-results-website/scripts/restart_service.sh
echo "Restarted the service sucessfully"'''
      }
    }

  }
}