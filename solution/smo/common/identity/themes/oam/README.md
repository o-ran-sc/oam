# create custom theme

A detailed description of the theme creation can be found in the [keycloak documentation](https://www.keycloak.org/docs/latest/server_development/#_themes).
It's not necessary to create a new theme from scratch. You can inherit from a base theme and override only the necessary 
parts.

- use `- KEYCLOAK_EXTRA_ARGS="--log-level=DEBUG --spi-theme-static-max-age=-1 --spi-theme-cache-themes=false --spi-theme-cache-templates=false"` for theme development

# add themes to solution

After creating the theme, you can add it to the solution. The following steps are necessary:

- mount the themes directory into the keycloak container
  - target directory: `/opt/bitnami/keycloak/themes/[custom-theme-name]`
- add  `KEYCLOAK_EXTRA_ARGS="--spi-theme-default=[custom-theme-name]"` to the environment section in docker-compose.yml 
  for identity to select as default theme