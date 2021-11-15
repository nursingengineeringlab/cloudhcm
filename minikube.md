## Minikube and docker-compose

```
minikube start --insecure-registry "10.0.0.0/24"

minikube dashboard

minikube addons enable registry

docker-compose run api python manage.py migrate

docker-compose run api python care_api/manage.py createsuperuser

```