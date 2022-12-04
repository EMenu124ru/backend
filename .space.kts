job("Run npm test and publish") {

  failOn {
    testFailed { enabled = false }
    nonZeroExitCode { enabled = false }
  }

  startOn {
    gitPush {
      branchFilter {
        +"main"
      }
      //pathFilter {
      //  +"src/**"
      //}
    }
  }


  host("Build artifacts and a Docker image") {

    env["HUB_USER"] = Params("dockerhub_user")
    env["HUB_TOKEN"] = Secrets("dockerhub_token")
    env["SSH_PASS"] = Secrets("ssh_password")
    env["SSH_IP"] = Params("ssh_ip")
    env["SPACE_REPO"] = "ikit-ki20-161-b.registry.jetbrains.space/p/team-course-project-2022-2023/backend"

    shellScript {
      // login to Docker Hub
      content = """
                    docker login ${'$'}SPACE_REPO -u ${'$'}HUB_USER --password "${'$'}HUB_TOKEN"
                  """
    }

    // Nginx
    dockerBuildPush {
      file = "nginx/Dockerfile"
      // Docker context, by default, project root
      file = "Dockerfile"
      val spaceRepo = "${"$"}SPACE_REPO/nginx"
      tags {
        +"$spaceRepo:1.0.${"$"}JB_SPACE_EXECUTION_NUMBER"
        +"$spaceRepo:latest"
      }
    }
    
    // Django
    dockerBuildPush {
      file = "server/compose/production/django/Dockerfile"
      // Docker context, by default, project root
      file = "Dockerfile"
      val spaceRepo = "${"$"}SPACE_REPO/django"
      tags {
        +"$spaceRepo:1.0.${"$"}JB_SPACE_EXECUTION_NUMBER"
        +"$spaceRepo:latest"
      }
    }
    
    // postgres
    dockerBuildPush {
      file = "server/compose/production/postgres/Dockerfile"
      // Docker context, by default, project root
      file = "Dockerfile"
      val spaceRepo = "${"$"}SPACE_REPO/postgres"
      tags {
        +"$spaceRepo:1.0.${"$"}JB_SPACE_EXECUTION_NUMBER"
        +"$spaceRepo:latest"
      }
    }
    
  }
   container(displayName = "Run myscript", image = "rastasheep/ubuntu-sshd") {
       env["SSH_IP"] = Params("ssh_ip")
       env["SSH_PASS"] = Secrets("ssh_password")
       env["SPACE_REPO"] = "ikit-ki20-161-b.registry.jetbrains.space/p/team-course-project-2022-2023/frontend-client"
        shellScript {
          content = """
          				apt update
          				apt install -y sshpass
                        apt update
          				sshpass -p "${"$"}SSH_PASS" ssh -o StrictHostKeyChecking=no root@${"$"}SSH_IP "cd ~/EMenuBackend ls"
                    """
        }
    }
}

