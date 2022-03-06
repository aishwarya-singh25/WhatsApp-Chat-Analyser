class Chat:
  def __init__(authors, first_timestamp, last_timestamp, number_of_messages, sentiment):
    self.authors = authors
    self.number_of_messages = number_of_messages
    self.sentiment = sentiment
    self.first_timestamp = first_timestamp
    self.last_timestamp = last_timestamp

  def get_authors:
  	return self._authors

  def get_first_timestamp:
  	return self._first_timestamp

  def get_last_timestamp:
  	return self._last_timestamp

  def get_number_of_messages:
  	return self._number_of_messages 

  def get_sentiment:
  	return self._sentiment
   
  def word_cloud:
    return vis.word_cloud(self)
