# add themes to solution
- copy `org.keycloak.keycloak-themes-XX.Y.Z.jar` from image and unzip 
- copy keycloak themes into directory a themes subdirectory directory with 
- modify css and resources (see dev resoures in keycloak)
- use `- KEYCLOAK_EXTRA_ARGS="--log-level=DEBUG --spi-theme-static-max-age=-1 --spi-theme-cache-themes=false --spi-theme-cache-templates=false"` for online development
- add  `KEYCLOAK_EXTRA_ARGS="--spi-theme-default=5gberlin"` to as environment in docker-compose.yml for identity to select as default theme