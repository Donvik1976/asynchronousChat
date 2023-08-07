from setuptools import setup, find_packages

setup(name="my_proj_mess_server",
      version="0.0.1",
      description="my_proj_mess_server",
      author="Viktor Donets",
      author_email="vdonets76@mail.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome']
      )
