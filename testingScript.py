from RPA.Robocloud.Secrets import Secrets

secrets = Secrets()
user_details = secrets.get_secret("vault")
print(str(user_details))