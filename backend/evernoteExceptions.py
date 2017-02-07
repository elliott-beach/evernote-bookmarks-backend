class EvernoteError(Exception):
    """Base class for Evernote Exceptions."""


class NoteBookNotFoundError(EvernoteError):
    """ Trying to retrieve non-existent notebook. """

