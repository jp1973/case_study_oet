#The code

In order to run the code, do the following:

1) make sure that Docker is installed on local machine
2) clone repo
3) run following command to build docker
      "sudo docker build -t pyspark-example:dev ."

4) run following command to run the code
      "sudo docker run --mount type=bind,source="$(pwd)",target=/opt/application pyspark-example:dev driver local:///opt/application/main.py "


#The delivery pipeline
Just as I familiar with AWS, I decided to use AWS ECS(AWS docker environemnt) to run this application 

For the sake of cloud-agnosticism delivery pipeline is build around Github actions, which allows to maintain muti-cloud application. There is a set of ready gitgub actions which allwos to deploy docker application to AWS ECS. More could be found on this link
https://docs.github.com/en/actions/deployment/deploying-to-your-cloud-provider/deploying-to-amazon-elastic-container-service

See the diagram above
