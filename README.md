# Run with docker

1. Build docker images (only once time):
    ```bash
     docker compose build
    ```
2. After build (only once time):
    ```bash
     docker compose up
    ```
3. To stop containers: 
    ```bash
     docker compose stop
    ```
3. To restart stopped containers:
    ```bash
     docker compose start
    ```

## Pgadmin credentials

* user: ```admin@uniandes.edu.co```
* password: ```miso4204```


## Postgres credentials

* user: ```admin```
* password: ```miso4204```

## Considerations to deploy API and batch on gcp:

1. Install docker and docker compose on the vm: 
    ```bash
     sudo apt-get update
    ```
    ```bash
     sudo apt-get install -y docker.io
    ```
    ```bash
     sudo apt-get install docker-compose
    ```
2. Map the VM nfs folder for storage: 
    ```bash
     sudo mount 10.138.0.4:/var/nfs/general /nfs/general
    ```
    ```bash
     sudo mount 10.138.0.4:/home /nfs/home
    ```
