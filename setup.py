import os


req_file = "requirements.txt"

with open(os.path.join(os.path.dirname(__file__), req_file)) as f:
    requires = list(f.readlines())
print(f"{requires}")

from setuptools import setup

setup(name="passe-passe",
      version='0.0.1',
      packages=['passe-passe'],
      author="Thierry Jean",
      description="".join("""
          Commandline tool to encrypt credentials
      """.strip().split('\n')),
      install_requires=requires)
