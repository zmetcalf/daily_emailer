from setuptools import setup

setup(name='daily_emailer',
      version='alpha',
      description='Django implementation of sending an email a day.',
      author='Zach Metcalf',
      author_email='zachery.metcalf@gmail.com',
      url='http://github.com/zmetcalf/daily_emailer',
      install_requires=['django>=1.6.2', 'sendgrid>=0.3.5'],
     )
