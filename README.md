# FetchHTTPEndpointCheck
This repository handles the implementation of a program to perform the health check of a set of provided HTTP endpoints through an input yaml file.

## Required Packages
- Following is the list of required packages
    - PyYAML: 6.0.1
    - requests: 2.31.0
    - urllib3: 2.1.0
- To install these packages, make sure you have the [requirements.txt](https://github.com/armenon299/FetchHTTPEndpointCheck/blob/main/requirements.txt) file on your local machine. Downloading the whole repository will ensure it is there on the machine.
- Execute the following command on your terminal from the folder where the repository is downloaded locally:    
    `pip install -r requirements.txt`

## Design Elements
- Implemented the program using threads to allow parallel check of the endpoints in case of a larger set of input HTTP Endpoints.
- Implemented exception checks for specific cases for better user experience
- Implemented the parameters in a config file for better handling in future

## How To Execute
- Download this repository
- Make sure you install the [Required Packages](https://github.com/armenon299/FetchHTTPEndpointCheck/blob/main/README.md#required-packages) as per the instructions.
- The config.py is also needed to run the program.
- To run the program, execute the following command:   
    `python http_health_checker.py <path to input yaml file`   
    Example: `python http_health_checker.py sample_sites.yaml`


