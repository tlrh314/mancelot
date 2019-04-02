#!/usr/bin/env bash
mkdir -p /root/.docker
cat > /root/.docker/config.json <<- "EOF"
{
        "auths": {
                "https://index.docker.io/v1/": {
                        "auth": "docker_hub_credentials"
                }
        }
}
EOF
sed -i 's/docker_hub_credentials/'"$docker_hub_credentials"'/g' /root/.docker/config.json
docker pull registry.gitlab.com/psono/psono-postgres:latest
docker tag registry.gitlab.com/psono/psono-postgres:latest psono/psono-postgres:latest
docker push psono/psono-postgres:latest
curl -X POST curl https://hooks.microbadger.com/images/psono/psono-postgres/xRhAhJHIdhJfxPT0WEBBSwjUH7c=