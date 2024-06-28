from curby.core import (
    request
)

response = request("https://www.billboard.com/charts/hot-100/", header={
    "User-Agent": "Chrome/120.0.0.0"
})