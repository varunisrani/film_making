from setuptools import setup, find_packages

setup(
    name="film_making",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-multipart",
        "python-dotenv",
        # Add other dependencies as needed
    ],
) 