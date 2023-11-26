pipeline {
  agent any
  stages {
    stage('Pull from Github') {
      steps {
        git(url: 'https://github.com/piotrsuchy/jenkins-ci-results-website', branch: 'main')
      }
    }

  }
}