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
docker exec -it 81af49 psql -U postgres company
```

### Backing up the database
Had to do this in the container because my local psql version refused to run on the the version in the container

psql (PostgreSQL) 14.9 (Ubuntu 14.9-0ubuntu0.22.04.1)
psql (PostgreSQL) 16.0 (Debian 16.0-1.pgdg120+1)
```bash
docker exec -it 81af49 bash
pg_dump -U postgres -W -F t company > backup_company.tar
```
Used the download command in the vscode docker extension to retrieve it

### alembic migrations
#### setup
pip install alembic
alembic init alembic
<!-- in alembic.ini -->
sqlalchemy.url = driver://user:pass@localhost/dbname
<!-- in alembic/env.py -->
from myapp.models import Base  # Replace with your actual import
target_metadata = Base.metadata

#### And here is the ongoing process
alembic revision --autogenerate -m "Add cascade delete"
alembic upgrade head



<a href="https://www.flaticon.com/free-icons/confetti" title="confetti icons">Confetti icons created by pongsakornRed - Flaticon</a>