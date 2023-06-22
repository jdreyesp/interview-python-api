# interview-python-API ⛅

---

## Motivation

In `Airport` company, within its data platform, customers must send metadata information that is needed for them to define certain
parts of the operations, configuration, etc. that the platform need to be aware of so that it's triggering the right components, and making the 
right operations so that the customer is having their expected results. 

For that we need to create an API that will manage metadata, coming from different sources in the company.


## Description 

The MetadataAPI will manage metadata with a certain schema (see below), and it will serve these endpoints:

| endpoint      | Method | Description                                                                                                                                                    |
|---------------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /metadata     | GET    | Expected: 200 (OK) Errors:  404 (Not found) -> When metadata is not found in DB 500 (Internal Server Error) -> When something wrong happens                      |
| /metadata/{id} | GET    | Expected: 200 (OK) Errors:  404 (Not found) -> When metadata is not found in DB 500 (Internal Server Error) -> When something wrong happens                      |
| /metadata      | POST   | JSON Body:  {   'name': <metadata_name>   'payload': <metadata_payload> }  Expected: 200 (OK) Errors:  500 (Internal Server Error) -> When something wrong happens |
| /metadata/{id} | DELETE | Expected: 200 (OK) Errors:  404 (Not found) -> When metadata is not found in DB 500 (Internal Server Error) -> When something wrong happens                      |

Data structure:

| name          | type      | description                                         |
|---------------|-----------|-----------------------------------------------------|
| id            | UUID      | Autogenerated UUID of the metadata                  |
| registered_on | Timestamp | Time that the metadata was registered in the system |
| name          | String    | Name of the metadata                                |
| payload       | String    | JSON text with the metadata                       |

Assumptions:

- Metadata schema has this format:

```json
{
    "sourceName": "my-flights",
    "jobCluster": {
      "min_workers": 1
    },
    "partitioning": "--partitioning=logic=partitionByEventTimestamp"
}
```

## User stories to be done 

### Metadata API User story

Me as a data platform data producer, I want to have an API that manages metadata, so that I can create, delete and retrieve
metadata configuration.

- Description:
  - Given parts:
    - API solution (build and run locally: `docker build --tag metadata-demo . ; docker run --publish 3100:3100 metadata-demo`)
    
  - To do:
    - Fill the gaps on `` and `` (test // bug fixing)
    
- Acceptance criteria:
  - API should give all methods with the corresponding result types and errors
  - The solution should be deployed in a Docker container, and a real call should be done so that we prove it works 

### Automate Metadata API  

Me as a data platform provider, I need to automate the build, test, and deployment of the metadata API solution, so that we
adopt CI/CD distribution method.

- Description
  - Set up a new Azure DevOps organization / project or use an existing one. To create a new one, click [here](https://go.microsoft.com/fwlink/?LinkId=2014579&campaign=acom~azure~pipelines~pricing~hero&projectVisibility=Everyone&githubsi=true&clcid=0x409)
  - You can set up an Azure free account. That should get you all needed resources for free during a period (check [this page](https://azure.microsoft.com/en-us/pricing/free-services) for more info)
  - Set up a container registry manually from the Azure Portal or from the Azure CLI (see tips)
  - Create a DevOps pipeline and do:
    - run `pytest` tests from the project source folder
    - build the artifact
    - publish artifact to Azure Container Registry
  
  - Tips:
    - You could follow [this guide](https://learn.microsoft.com/en-us/azure/developer/python/tutorial-containerize-simple-web-app-for-app-service?tabs=web-app-fastapi#create-a-resource-group-and-azure-container-registry)
- Acceptance criteria:
  - A pipeline YAML file should be in the project code under `cicd` folder.
  - That pipeline should test and deploy the artifact to ACR

- Questions:
  - How the infra could be automatically created from the pipeline?
  
### Deploy the metadata API to Azure App service

Me as a data platform provider, I need to use Azure resources to deploy the metadata API, so that we use cloud services.

- Description
  - See requirements from `Automate Metadata API`
  - Create ARM template or terraform (your choice) for the Azure Container Registry and App Service
  - Deploy the infra from the previous pipeline. If you did not manage to complete the `Automate Metadata API` user story, you could create the code for deploying infra and manually run it.
  - Deploy the image to a container registry and use it from the Azure service app 

Tips: 

- Set up Azure CLI from local to access your resources and run commands


Acceptance criteria:
    - API is deployed in an app service that we can consume
    - A call will be made to the app service, serving the same features as the previous user story

### (Bonus) Performance test the solution

//TODO

## Tips

- Keep it simple and clean
- Solution components and integrations needs to be tested accordingly.
- Use types
- Use a `venv` to handle your dependencies