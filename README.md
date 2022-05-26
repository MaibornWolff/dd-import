# dd-import

> A utility to (re-)import findings and language data into [DefectDojo](https://www.defectdojo.org/)

Findings and languages can be imported into DefectDojo via an [API](https://defectdojo.github.io/django-DefectDojo/integrations/api-v2-docs/). To make automated build and deploy pipelines easier to implement, `dd-import` provides some convenience functions:

- Products, engagements and tests will be created if they are not existing. This avoids manual preparation in DefectDojo or complicated steps within the pipeline.
- Product types, products, engagements and tests are referenced by name. This make pipelines more readable than using IDs.
- Build information for `build_id`, `commit_hash` and `branch_tag` can be updated when uploading findings.
- No need to deal with `curl` and its syntax within the pipeline. This makes pipelines shorter and better readable.
- All parameters are provided via environment variables, which works well with pipeline definitions like GitHub Actions or GitLab CI.

## User guide

### Installation and commands

**Python**

`dd-import` can be installed with pip. Only Python 3.8 and up is suported.

```bash
pip install dd-import
```

The command `dd-reimport-findings` re-imports findings into DefectDojo. Even though the name suggests otherwise, you do not need to do an initial import first. 

The command `dd-import-languages` imports languages data that have been gathered with the tool [cloc](https://github.com/AlDanial/cloc), see [Languages and lines of code](https://defectdojo.github.io/django-DefectDojo/integrations/languages/) for more details.


**Docker**

Docker images can be found in https://hub.docker.com/r/maibornwolff/dd-import.

A re-import of findings can be started with 

```bash
docker run --rm dd-import:latest dd-reimport-findings.sh
```

Importing languages data can be started with


```bash
docker run --rm dd-import:latest dd-import-languages.sh
```

Please note you have to set the environment variables as described below and mount a folder containing the file with scan results when running the docker container.

`/usr/local/dd-import` is the working directory of the docker image, all commands are located in the `/usr/local/dd-import/bin` folder.

### Parameters

All parameters need to be provided as environment variables

| Parameter             | Re-import findings | Import languages | Remark |
|-----------------------|:------------------:|:----------------:|--------|
| DD_URL                | Mandatory          | Mandatory        | Base URL of the DefectDojo instance |
| DD_API_KEY            | Mandatory          | Mandatory        | Shall be defined as a secret, eg. a protected variable in GitLab or an encrypted secret in GitHub |
| DD_PRODUCT_TYPE_NAME  | Mandatory          | Mandatory        | A product type with this name must exist |
| DD_PRODUCT_NAME       | Mandatory          | Mandatory        | If a product with this name does not exist, it will be created |
| DD_ENGAGEMENT_NAME    | Mandatory          | -                | If an engagement with this name does not exist for the given product, it will be created |
| DD_TEST_NAME          | Mandatory          | -                | If a test with this name does not exist for the given engagement, it will be created |
| DD_TEST_TYPE_NAME     | Mandatory          | -                | From DefectDojo's list of test types, eg. `Trivy Scan` | 
| DD_FILE_NAME          | Optional           | Mandatory        | |
| DD_ACTIVE             | Optional           | -                | Default: `true` |
| DD_VERIFIED           | Optional           | -                | Default: `true` |
| DD_MINIMUM_SEVERITY   | Optional           | -                | |
| DD_PUSH_TO_JIRA       | Optional           | -                | Default: `false` |
| DD_CLOSE_OLD_FINDINGS | Optional           | -                | Default: `true` |
| DD_VERSION            | Optional           | -                | |
| DD_ENDPOINT_ID        | Optional           | -                | |
| DD_SERVICE            | Optional           | -                | |
| DD_BUILD_ID           | Optional           | -                | |
| DD_COMMIT_HASH        | Optional           | -                | |
| DD_BRANCH_TAG         | Optional           | -                | |
| DD_API_SCAN_CONFIGURATION_ID | Optional    | -                | Id of the API scan configuration for API based parsers, e.g. SonarQube |
| DD_SSL_VERIFY         | Optional           | Optional         | Disable SSL verification by setting to `false` or `0`. Default: `true` |

### Usage

This snippet from a [GitLab CI pipeline](.gitlab-ci.yml) serves as an example how `dd-import` can be integrated to upload data during build and deploy using the docker image:

```yaml
variables:
  DD_PRODUCT_TYPE_NAME: "Showcase"
  DD_PRODUCT_NAME: "DefectDojo Importer"
  DD_ENGAGEMENT_NAME: "GitLab"

...

trivy:
  stage: test
  tags:
    - build
  variables:
    GIT_STRATEGY: none
  before_script:
    - export TRIVY_VERSION=$(wget -qO - "https://api.github.com/repos/aquasecurity/trivy/releases/latest" | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/')
    - echo $TRIVY_VERSION
    - wget --no-verbose https://github.com/aquasecurity/trivy/releases/download/v${TRIVY_VERSION}/trivy_${TRIVY_VERSION}_Linux-64bit.tar.gz -O - | tar -zxvf -
  allow_failure: true
  script:
    - ./trivy --exit-code 0 --no-progress -f json -o trivy.json maibornwolff/dd-import:latest
  artifacts:
    paths:
    - trivy.json
    when: always
    expire_in: 1 day

cloc:
  stage: test
  image: node:16
  tags:
    - build
  before_script:
    - npm install -g cloc
  script:
    - cloc src --json -out cloc.json
  artifacts:
    paths:
    - cloc.json
    when: always
    expire_in: 1 day

upload_trivy:
  stage: upload
  image: maibornwolff/dd-import:latest
  needs:
    - job: trivy
      artifacts: true  
  variables:
    GIT_STRATEGY: none
    DD_TEST_NAME: "Trivy"
    DD_TEST_TYPE_NAME: "Trivy Scan"
    DD_FILE_NAME: "trivy.json"
  script:
    - dd-reimport-findings.sh

upload-cloc:
  image: maibornwolff/dd-import:latest
  needs:
    - job: cloc
      artifacts: true  
  stage: upload
  tags:
    - build
  variables:
    DD_FILE_NAME: "cloc.json"
  script:
    - dd-import-languages.sh
```

- ***variables*** - Definition of some environment variables that will be used for several uploads. `DD_URL` and `DD_API_KEY` are not defined here because they are protected variables for the GitLab project.
- ***trivy*** - Example for a vulnerability scan with [trivy](https://github.com/aquasecurity/trivy). Output will be stored in JSON format (`trivy.json`).
- ***cloc*** - Example how to calculate the lines of code with [cloc](https://github.com/AlDanial/cloc). Output will be stored in JSON format (`cloc.json`).
- ***upload_trivy*** - This step will be executed after the `trivy` step, gets its output file and sets some variables specific for this step. Then the script to import the findings from this scan is executed.
- ***upload_cloc*** - This step will be executed after the `cloc` step, gets its output file and sets some variables specific for this step. Then the script to import the language data is executed.

Another example, showing how to use `dd-import` within a GitHub Action, can be found in [dd-import_example.yml](.github/workflows/dd-import_example.yml).

## Developer guide

### Testing

`./bin/runUnitTests.sh` - Runs the unit tests and reports the test coverage. 

`./bin/runDockerUnitTests.sh` - First creates the docker image and then starts a docker container in which the unit tests are executed.

## License

Licensed under the [3-Clause BSD License](LICENSE.txt)
