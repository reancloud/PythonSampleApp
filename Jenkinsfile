pipeline {
  agent {
    node {
      label 'master'
    }
  }

  environment {
     }

  stages {
    stage('Prepare Build Environment') {
      steps {
        echo "\u001B[34m\u001B[1mPreparing build environment\u001B[0m"
        script {
          ansiColor('xterm') {
           withPythonEnv('python') {  
                stage('Code Style Linting') {
                  echo "\u001B[34m\u001B[1mCode Style Linting\u001B[0m"
                  try {
                    sh '''
                          #!/bin/bash
                          set -e
                          pycodestyle conftest.py
                          pycodestyle deploy/
                    '''
                  }
                  catch (Exception e) {
                    println "\u001B[31mCode style linting failed. Please fix the issues\u001B[0m"
                    sh "exit 1"
                  }
                }
            }
           }  
          }
        }
      }
    }
  }
  post {
/*    success {
      mail to: "${emailIDs}",
      subject: 'REAN-Assess Build Successfull',
      body: "Download Docx report at: ${artifactDownloadURL}"
    }
*/    
    always {
      deleteDir()
    }
  }
}

