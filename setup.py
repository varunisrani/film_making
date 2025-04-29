from setuptools import setup, find_packages

setup(
    name="film_making",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "pydantic",
        "python-multipart",
        "aiofiles",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-dateutil",
        "requests",
    ],
    python_requires=">=3.8",
) 