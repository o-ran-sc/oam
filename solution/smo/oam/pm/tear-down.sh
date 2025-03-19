echo "Stop and remove all containers in the project"

docker compose -p influx -f docker-compose-influxdb_gen.yaml down
docker compose -p pm -f docker-compose_gen.yaml down

echo "Removing influxdb2 config..."
rm -rf ./config/influxdb2

unset $(grep -v '^#' .env | awk 'BEGIN { FS = "=" } ; { print $1 }')
echo "All clear now!"
