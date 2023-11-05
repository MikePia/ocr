# Using a postgress docker container

/opt/minituts/docker/docker_postgres/postgres_inacan/docker-compose.yml

May have to stop a postgres instance to use this one
## Starting from scratch using postgres docker instructions

```docker pull postgres:14.5```
```docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=s3cr3tp4ssw0rd -d postgres```
Connect in dbeaver run SQL ```SELECT now()```
```bash
docker stop some-postgres
docker start some-postgres
```


```bash
docker run -p 5432:5432 -d \
    --name some-postgress \
    -e POSTGRES_PASSWORD=s3cr3tp4ssw0rd \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_DB=company \
    -v pgdata:/var/lib/postgresql/data  \
    postgres

# dbeaver new connection -- no tables yet

psql company -h localhost -U postgres

docker exec -it [id] psql -U postgres company

```

