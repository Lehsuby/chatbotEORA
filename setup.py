from setuptools import setup, find_packages
from os.path import join, dirname

setup(name='chatboteora',
        version='0.2',
        description='Chatbot',
        long_description=open(join(dirname(__file__), 'README.txt')).read(),
        classifiers=[
        'Programming Language :: Python :: 3.5'
        ],
        url='https://github.com/Lehsuby/chatbotEORA',
        author='Lehsuby',
        packages=find_packages(),
        test_suite='tests',
        install_requires=[
            'absl-py',
            'astor',
            'Click',
            'exception',
            'Flask',
            'gast',
            'grpcio',
            'h5py',
            'itsdangerous',
            'Jinja2',
            'Keras-Applications',
            'Keras-Preprocessing',
            'MarkupSafe',
            'numpy',
            'pg8000',
            'protobuf',
            'psycopg',
            'py',
            'requests',
            'scramp',
            'six',
            'SQLAlchemy',
            'tensorboard',
            'tensorflow',
            'tensorflow-estimator',
            'termcolor',
            'testing.common.database',
            'testing.postgresql',
            'urllib3',
            'Werkzeug',
            'wrapt'
        ],
        entry_points={
          'console_scripts': [
              'start = my_app: main',
          ]
        },
        include_package_data=True)