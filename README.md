# harmonica_l12_node

```shell
poetry export --without-hashes -o requirements.txt
```

```shell
docker build -t harmonica_l12_node .

docker run --rm --env-file ./.env harmonica_l12_node
```
