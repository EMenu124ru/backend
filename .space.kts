job("Run npm test and publish") {

  failOn {
    //testFailed { enabled = false }
    //nonZeroExitCode { enabled = false }
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
      val spaceRepo = "${"$"}SPACE_REPO/nginx"
      tags {
        +"$spaceRepo:1.0.${"$"}JB_SPACE_EXECUTION_NUMBER"
        +"$spaceRepo:latest"
      }
    }

    // Django
    dockerBuildPush {
      file = "server/Dockerfile"
      val spaceRepo = "${"$"}SPACE_REPO/django"
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
          ls -lrt
          chmod +x pull-run.sh 
          sshpass -p "${"$"}SSH_PASS" ssh -o StrictHostKeyChecking=no root@${"$"}SSH_IP "cd ~/EMenuBackend; ./pull-run.sh"
        """
      }
  }
}
