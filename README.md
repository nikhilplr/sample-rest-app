# GitHub Action: Leverage the power or release in Github 

  This repository contains small python rest api along with a GitHub Actions workflow that builds and promote a Docker image to Google Artifact Registry when a draft release tag is created. This workflow is triggered on the release event specifically for draft releases, allowing for automated deployment workflows as part of the release process.

  Once the artifact is create that will be automatically deployed to the Kubernetes cluster.

## What's release in GitHub
A release in GitHub is a feature provided to package & document specific version of codebase. GitHub releases provide a snapshot of the code and offer additional metadata, allowing developers to share versions of the software with specific milestones or improvements.

![alt text](image.png)

## Benefits of Using Release
- Distribution: Releases are a convenient way to distribute software. We can create a release from existing tag or new tag. In this example I'm creating a new release tag.
- Documentation: Release notes improve transparency and communication by documenting what’s changed in each version. We can auto populate the release npotes from previous release easily. 
- Stability: By tagging specific commits as releases, developers can ensure that they’re distributing stable, tested versions.
- Automation: Releases integrate well with CI/CD pipelines, enabling automated builds and deployments based on release events. This could be a better approach to create a build and test in preproduction along with other sets of operation inslucing automated QA , Security scanning etc. 

## Workflow Overview
This GitHub Actions workflow does the following:

- Triggers on the creation of a draft release.
- Builds a Docker image using the code in the repository.
- Tags the Docker image based on the release version.
- Pushes the image to Google Artifact Registry, making it ready for deployment.
- Deploy the new images to kubernetes cluster using kubectl command. 


## Prerequisites
To use this workflow, you need:

A Google Cloud project with Google Artifact Registry enabled.
A Google Cloud project with Google Kubernetes cluster with a namespace created.
A Google Cloud service account with permission to push images to your Artifact Registry.
A Google Cloud service account with permission to deploy images kuberntes cluster.
A JSON key for the service account stored as a GitHub secret (GCP_KEY).
A GitHub secret for the Google Cloud Project ID (GCP_PROJECT_ID).


## Example Workflow

Below is an example workflow configuration, found in .github/workflows/deploy-draft-release.yml
```
name: Build and Deploy from Draft Release

on:
  release:
    types: [prereleased]

jobs:
  build:
    runs-on: ubuntu-latest 
    

    steps:
      - name: Check Out Repository
        uses: actions/checkout@v3 

      - name: Set Up Google Cloud SDK
        uses: 'google-github-actions/auth@v2'
        with:
          version: 'latest'
          credentials_json: ${{ secrets.GCP_KEY }} 

      - name: Authenticate Docker to GCR
        run: |
          gcloud auth configure-docker  us-central1-docker.pkg.dev

      - name: Tagging
        run: |
          
          TAG_NAME=${{ github.event.release.tag_name }} 
          echo "${TAG_NAME}" 
          echo "TAG_NAME=${TAG_NAME}" >> $GITHUB_ENV 

      - name: Build Docker Image
        run: |
          IMAGE_NAME="us-central1-docker.pkg.dev/${{ secrets.GCP_PROJECT_ID }}/my-app-ms-repository/pyappapi"
          docker build -t ${IMAGE_NAME}:${{ env.TAG_NAME }} . 
      
      - name: Push Docker Image to GCR
        run: | 
          IMAGE_NAME="us-central1-docker.pkg.dev/${{ secrets.GCP_PROJECT_ID }}/my-app-ms-repository/pyappapi"
          docker push ${IMAGE_NAME}:${{ env.TAG_NAME }}
```

## Workflow Details
Triggers on Draft Release Creation: The workflow is triggered when a new draft release is created, capturing the tag name.
Docker Build and Push: The Docker image is built and tagged with the release version, then pushed to Google Artifact Registry.

### Setting Up the GitHub Secrets

To enable this workflow, create the following secrets in your GitHub repository:

GCP_KEY: The JSON key for the Google Cloud service account.
GCP_PROJECT_ID: Your Google Cloud project ID.

### How to Use
Create a draft release with a tag (e.g., v1.0.0).
Once the release is created, this workflow will automatically:
Build a Docker image from the code in the repository.
Tag the Docker image with the release tag.
Push the Docker image to Google Artifact Registry.

### Notes
Ensure that the Google Cloud service account used in GCP_KEY has the artifactregistry.repositories.uploadArtifacts permission.
To trigger the workflow on a published release instead of a draft, change the on event to types: [prereleased] under the release trigger.