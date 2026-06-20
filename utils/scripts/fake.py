from faker import Faker
from os import environ
fake = Faker()
# the module is set as an environment variable
module = environ["ESPANSO_MODULE"]
print(getattr(fake, module)())