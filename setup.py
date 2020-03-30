import setuptools


# You can see about deploy, publishing and building packages here: https://github.com/Hedgehogues/templar/


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open("README.md", "r") as fh:
    long_description = fh.read()

install_reqs = parse_requirements('./requirements.txt')
print(install_reqs)

setuptools.setup(
    name="covid19",
    version="0.2.0",
    author="Dmitry Sergeyev, Sviatoslav Kovalyov, Anton Repushko, Egor Urvanov, AI-max",
    author_email="sergeyev.d.a@yandex.ru, iggisv9t@gmail.com, repushko.a@gmail.com, hedgehogues@bk.ru",
    description="This is short readme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hedgehogues/docker-compose-deploy",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=install_reqs,
)
