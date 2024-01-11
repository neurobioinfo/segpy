import setuptools

setuptools.setup(
    # Needed to silence warnings
    name='segpy',
    url='https://github.com/neurobioinfo/segpy',
    author='Saeid Amiri',
    maintainer='Saeid Amiri',
    author_email='saeid.amiri@mcgill.ca',
    # Needed to actually package something
    packages=setuptools.find_packages(),
    # Needed for dependencies
    install_requires=['numpy', 'pandas', 'hail'],
    # *strongly* suggested for sharing
    version='0.2.2.0',
    license='MIT',
    description='Segpy: A pipline for segregation analysis',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.rst').read(),
    # if there are any scripts
    scripts=['hello.py'],
)

