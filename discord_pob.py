import logging
from pob_bot import client


def initialize_logging():
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='discord_pob.log',
                        filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s | %(name)-5s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)


if __name__ == '__main__':
    token = "NDE4Nzc3Mjk1NzEzNzMwNTcw.DXmgaQ.E-oww8jXRxcKdEemh-ZWGvabliU"  # todo: load token
    server = "12023"
    initialize_logging()
    logging.info("Starting pob discord bot on server={}".format(server))
    client.run(token)

