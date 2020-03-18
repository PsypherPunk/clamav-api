import connexion
from connexion.resolver import RestyResolver

app = connexion.App(__name__, specification_dir="swagger/",)

app.add_api(
    "swagger.yaml", resolver=RestyResolver("clamav"), strict_validation=True,
)


if __name__ == "__main__":
    app.run()
