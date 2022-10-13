job("linter") {
    startOn {
        gitPush { enabled = true }
    }
    container(image="python:3.10.5-slim-bullseye") {
        shellScript {
            content = """
                apt update
                apt install apt-transport-https ca-certificates curl software-properties-common
                curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
                add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu `lsb_release -cs` test"
                apt update
                apt install docker.io -y
                pip install invoke rich docker-compose docker-compose
                bash ./.git-hooks/pre-push
            """
        }
    }
}
