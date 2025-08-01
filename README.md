## AWS-CICD-Deployment-with-Github-Actions

1. Login to AWS console.
2. Create IAM user for deployment
#with specific access

1. EC2 access : It is virtual machine

2. ECR: Elastic Container registry to save your docker image in aws

        ECR URI: 869935080204.dkr.ecr.ap-south-1.amazonaws.com/myawslanggrapgh

        runs-on: self-hosted

### Description: About the deployment

1. Build docker image of the source code

2. Push your docker image to ECR

3. Launch Your EC2 

4. Pull Your image from ECR in EC2

5. Lauch your docker image in EC2

### Policy:

1. AmazonEC2ContainerRegistryFullAccess

2. AmazonEC2FullAccess
3. Create ECR repo to store/save docker image
    - Save the URI: 315865595366.dkr.ecr.us-east-1.amazonaws.com/ecr-repo-name
4. Create EC2 machine (Ubuntu)
5. Open EC2 and Install docker in EC2 Machine:

### Run the below commands on ec2 server

- sudo apt-get update -y

- sudo apt-get upgrade

#required

- curl -fsSL https://get.docker.com -o get-docker.sh

- sudo sh get-docker.sh

- sudo usermod -aG docker ubuntu

- newgrp docker

6. Configure EC2 as self-hosted runner:
setting>actions>runner>new self hosted runner> choose os> then run command one by one

7. Setup github secrets:

AWS_ACCESS_KEY_ID=

AWS_SECRET_ACCESS_KEY=

AWS_REGION = us-east-1

AWS_ECR_LOGIN_URI = demo>>  566373416292.dkr.ecr.ap-south-1.amazonaws.com

ECR_REPOSITORY_NAME = myawslanggrapgh

[![Deploy Application Docker Image to EC2 instance](https://github.com/SachinMishra-ux/AWS_langgrapgh_deployment/actions/workflows/cicd.yaml/badge.svg)](https://github.com/SachinMishra-ux/AWS_langgrapgh_deployment/actions/workflows/cicd.yaml)



## Remove the spaces from server

```docker system prune -a --volumes -f```

## docker images

```docker images```

## docker ps
## docker ps -a

### To check the running conatiners

```docker ps -a```


## To install aws-cli on ec2 machine:

```

curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip -y
unzip awscliv2.zip
sudo ./aws/install

```


## checke it

```aws --version```

## pull the image

```
docker pull 869935080204.dkr.ecr.ap-south-1.amazonaws.com/myawslanggrapgh:latest

```

## Run the image

```
docker run -d   --env-file .env   -p 8000:8000   869935080204.dkr.ecr.ap-south-1.amazonaws.com/myawslanggrapgh:latest
```


## docker ps -a --> to get conatiner id 
## docker logs conatiner-id


### to check the conatiner logs
```docker logs conatiner-id```
