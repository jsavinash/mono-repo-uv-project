## Commands
1. uv init 
uv init services/api-service --app
uv init services/api-gateway --app
uv init services/config-server --app
uv init services/service-discovery --app
uv init services/user --app
uv init services/item --app
uv init services/item-management --app
uv init services/product --app
uv init services/review-and-ratings --app
uv init services/inventory --app
uv init services/recommendations --app
uv init services/offers --app
uv init services/cart --app
uv init services/order --app
uv init services/archival --app
uv init services/notification --app
uv init services/serviceability --app
uv init services/payment --app

uv init libs/shared --lib
uv init packages/core --package

uv add shared-utils --package api-service