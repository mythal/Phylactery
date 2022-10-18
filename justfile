V := env_var("V")
app := env_var("APP")
repo := env_var("REPO")

all: build

build: echo
    #!/usr/bin/env bash
    set -euxo pipefail
    buildah build --format docker -t {{repo}}/{{app}}:{{V}}

push: echo
    #!/usr/bin/env bash
    set -euxo pipefail
    podman push {{repo}}/{{app}}:{{V}}

deploy: echo
    #!/usr/bin/env bash
    set -euxo pipefail
    gcloud run deploy {{app}} --image {{repo}}/{{app}}:{{V}}

echo:
    #!/usr/bin/env bash
    set -euxo pipefail
    echo app := {{app}}
    echo ver := {{V}}
    echo repo := {{repo}}
