[group: 'uv']
build PACKAGE:
    # Build a package before pushing it into code artifactory
    uv build --package {{PACKAGE}}

[group: 'uv']
@publish PACKAGE: (build PACKAGE)
    #!/bin/bash
    set -euxo pipefail
    # Artifactory username
    export UV_PUBLISH_USERNAME=aws
    # AWS code artifactory token
    export AWS_CODEARTIFACT_TOKEN="$(aws codeartifact get-authorization-token \
        --domain cognism --domain-owner 463470983643 \
        --region eu-west-1 --query authorizationToken \
        --output text \
        --profile cognism-data-mlops-dev
    )"
    # Artifactory password
    export UV_PUBLISH_PASSWORD=$AWS_CODEARTIFACT_TOKEN
    # Url for the repository
    export UV_PUBLISH_URL=https://cognism-463470983643.d.codeartifact.eu-west-1.amazonaws.com/pypi/Sciops/
    # Publish the built package
    uv publish

[group: 'package']
run-tests DIR:
    # Run tests for all packages
    uv run pytest {{DIR}}/ -v

[group: 'repo']
delete-dirs:
    # Delete some directories
    rm -rf dist .venv
