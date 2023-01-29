The code

In order to run the code, do the following:

1) make sure that Docker is installed on local machine
2) clone repo
3) run following command to build docker
      sudo docker build -t pyspark-example:dev .

4) run following command to run the code
      sudo docker run --mount type=bind,source="$(pwd)",target=/opt/application pyspark-example:dev driver local:///opt/application/main.py 


The delivery pipeline

For the sake of cloud-agnosticism delivery pipeline is build around Github actions, which allows to maintain muti-cloud application. The set of 
