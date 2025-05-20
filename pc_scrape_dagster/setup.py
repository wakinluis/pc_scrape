from setuptools import find_packages, setup

setup(
    name="pc_scrape_dagster",
    packages=find_packages(exclude=["pc_scrape_dagster_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
