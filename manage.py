import time
import logging

from manager import Manager

manager = Manager()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(filename)-20s %(message)s')


@manager.command
def runserver():
    """
    Runs server
    """
    from app.main import runserver

    runserver()


@manager.command
def test(recreate=False):
    """
    Runs tests in docker environment
    pass --recreate to recreate docker environment
    """

    from subprocess import run as run_process

    if recreate:
        recreate_commands = (
            'docker-compose down',
            'docker-compose build',
            'docker-compose up -d',
            'docker-compose ps'
        )

        run_process(" && ".join(recreate_commands),
                    shell=True)

    # small hook to assure that contatiners built
    time.sleep(3)

    run_process('docker-compose exec api pytest', shell=True)

    if recreate:
        run_process('docker-compose down', shell=True)


if __name__ == '__main__':
    manager.main()
