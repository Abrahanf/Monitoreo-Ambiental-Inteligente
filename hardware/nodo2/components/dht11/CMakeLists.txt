idf_component_register(
    SRCS "dht11.c"
    INCLUDE_DIRS "include"
    INCLUDE_DIRS "."
    REQUIRES driver
    REQUIRES driver esp_timer
)