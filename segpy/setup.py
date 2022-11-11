import setuptools

setuptools.setup(
    # Needed to silence warnings
    name='segpy',
    url='https://github.com/neurobioinfo/segregation',
    author='Neuro Bioinformatics Core',
    maintainer='Saeid Amiri',
    author_email='saeid.amiri@mcgill.ca',
    # Needed to actually package something
    packages=setuptools.find_packages(),
    # Needed for dependencies
    install_requires=['numpy', 'pandas', 'hail==0.2.81'],
    # *strongly* suggested for sharing
    version='0.1',
    license='MIT',
    description=' A package for Segregation Analysis',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.rst').read(),
    # if there are any scripts
    scripts=['hello.py'],
)
