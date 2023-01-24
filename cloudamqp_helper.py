import os
from typing import Callable
import pika
# from pika.exchange_type import ExchangeType
from dotenv import load_dotenv


# Load the .env file
load_dotenv()


class CloudAMQPHelper:
    """ The interface between this project and CloudAMQP """

    QUEUE_NAME = "get_me_hired_queue"
  
    def __init__(self) -> None:
        """ Sets up a connection and a channel when this class is instantiated """

        url = os.environ["CLOUDAMQP_URL"]
        params = pika.URLParameters(url)

        self.__connection = pika.BlockingConnection(params) # Connect to CloudAMQP
  
    def __create_channel(self) -> pika.BlockingConnection:
        channel = self.__connection.channel() # start a channel
        return channel
      
    def __create_queue(self) -> None:
        """ Declares a queue - always good to create the same queue 
            from the consumer side as well since the action is idempotent
        """
        # Get channel
        channel = self.__create_channel()
   
        # Create a queue
        channel.queue_declare(queue=self.QUEUE_NAME)

    def consume_message(self, callback: Callable) -> None:
        """ Reads a message published to a queue it's bound to """
        self.__create_queue()

        # Get channel
        channel = self.__create_channel()

        channel.basic_consume(
            self.QUEUE_NAME,
            callback,
            auto_ack=True
        )

        # start consuming (blocks)
        channel.start_consuming()
        self.connection.close()


# Create an instance
cloudamqp: CloudAMQPHelper = CloudAMQPHelper()