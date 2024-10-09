from app.core import Session


class UnitOfWork:
    def __init__(self):
        self.session = Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()
